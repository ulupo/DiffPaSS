# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/data_utils.ipynb.

# %% auto 0
__all__ = ['create_specieswise_dict', 'get_dataset_from_species', 'generate_dataset', 'get_single_and_paired_seqs',
           'msa_tokenizer', 'dataset_tokenizer']

# %% ../nbs/data_utils.ipynb 2
from collections import defaultdict
from collections.abc import Sequence
from typing import Optional, Union

import numpy as np
from numpy.random import default_rng

import torch

from .constants import DEFAULT_AA_TO_INT


def create_specieswise_dict(
    msa_data: list[list[tuple[str, str]]],
    species_name_func: callable,
    *,
    remove_species_with_one_seq: bool = True,
) -> list[dict[str, list[tuple[str, str]]]]:
    msa_data_species_by_species = []
    for msa_side in msa_data:
        msa_species_by_species_this_side = defaultdict(list)
        for rec in msa_side:
            species_name = species_name_func(rec[0])
            msa_species_by_species_this_side[species_name].append(rec)
        msa_data_species_by_species.append(msa_species_by_species_this_side)

    if remove_species_with_one_seq:
        for msa_data_species_by_species_this_side in msa_data_species_by_species:
            for species_name in list(msa_data_species_by_species_this_side.keys()):
                if len(msa_data_species_by_species_this_side[species_name]) < 2:
                    msa_data_species_by_species_this_side.pop(species_name)

    return msa_data_species_by_species


def get_dataset_from_species(
    msa_data_species_by_species: list[dict[str, list[tuple[str, str]]]],
    species: Sequence[str],
    *,
    pop_species: bool = False,
) -> dict:
    dataset = {"msa": {}, "positive_examples": None}
    group_sizes = {}
    for msa_side, side in zip(msa_data_species_by_species, ["left", "right"]):
        dataset["msa"][side] = []
        group_sizes[side] = []
        for species_name in species:
            recs = msa_side[species_name]
            dataset["msa"][side].extend(recs)
            group_sizes[side].append(len(recs))
            if pop_species:
                msa_side.pop(species_name)

    return {
        "dataset": dataset,
        "group_sizes_left": group_sizes["left"],
        "group_sizes_right": group_sizes["right"],
    }


def generate_dataset(
    parameters: dict,
    msa_data: list[list[tuple[str, str]]],
    species_name_func: callable,
    return_species: bool = False,
):
    """
    Function that given the two full paired MSAs of interacting sequences (seen as a list of tuples)
    creates the dataset (dictionary of MSAs, both "left" and "right" ones), made of:

    - "msa":   the MSA used to start the training of the permutation matrix.
    - "positive_examples":  MSA of correct pairs to use as context during the training. It can be None
                            if we don't want any context.

    We have to specify if we either want the list of blocks or the positive examples by setting the value of
    `generate_blocks` to True or False.

    We can also limit the depth of the MSA by changing `limit_depth`.
    Keep in mind that the maximum limit of sequences depends on the GPU memory.
    """
    assert len(msa_data[0]) == len(msa_data[1])
    dataset = {}

    # Set random generators
    rng = default_rng(seed=parameters["NUMPY_SEED"])
    rng_other = default_rng(seed=parameters["NUMPY_SEED_OTHER"])
    # Parameters of msa
    N_init = parameters["N"]
    max_size_init = parameters["max_size"]
    # Count species in full MSA
    species_l, inverse_l, sizes_l = np.unique(
        [species_name_func(rec[0]) for rec in msa_data[0]],
        return_inverse=True,
        return_counts=True,
    )
    species_r, inverse_r, sizes_r = np.unique(
        [species_name_func(rec[0]) for rec in msa_data[1]],
        return_inverse=True,
        return_counts=True,
    )
    assert set(species_l) == set(
        species_r
    ), "Species must be the same in the left and right MSA."
    # ----------------------------------------------------------------------------------------------
    # MAIN MSA
    # ----------------------------------------------------------------------------------------------
    # Set positive_examples to None
    dataset["positive_examples"] = None
    while True:
        # Iterate until we find a collection of sequences with total depth
        # 0.9 * N <= D <= 1.1 * N
        idxs_shuffled = np.arange(len(species_l))
        rng.shuffle(idxs_shuffled)
        cumsum_sizes_shuffled = np.cumsum(sizes_l[idxs_shuffled])
        idxs_in_range = np.flatnonzero(
            np.abs(cumsum_sizes_shuffled - N_init) <= N_init * 0.1
        )
        if len(idxs_in_range):
            num_species = rng.choice(idxs_in_range) + 1
            rand_species = np.sort(idxs_shuffled[:num_species])
            group_sizes = sizes_l[rand_species]
            if np.all(group_sizes > 1) and np.all(group_sizes <= max_size_init):
                break
    # Create msa by concatenating the selected sequences
    rand_idxs_l = []
    rand_idxs_r = []
    for unique_species_idx in rand_species:
        rand_idxs_l += [
            i for i, label in enumerate(inverse_l) if label == unique_species_idx
        ]
        rand_idxs_r += [
            i for i, label in enumerate(inverse_r) if label == unique_species_idx
        ]
    dataset["msa"] = {
        "left": [msa_data[0][i] for i in rand_idxs_l],
        "right": [msa_data[1][i] for i in rand_idxs_r],
    }
    # Print data
    print("Generated initial MSA")
    print("\tSpecies selected, total number of species selected:")
    print(species_l[rand_species])
    print(rand_species, ",", len(rand_species))
    print("\tPairs per species, total number of pairs:")
    print(group_sizes, ",", sum(group_sizes))
    # ----------------------------------------------------------------------------------------------
    # POSITIVE EXAMPLES
    # ----------------------------------------------------------------------------------------------
    if parameters["pos"]:
        while True:
            # Indices of species not used in msa
            unused_species_idxs = idxs_shuffled[num_species:].copy()
            rng_other.shuffle(unused_species_idxs)
            cumsum_sizes_shuffled = np.cumsum(sizes_l[unused_species_idxs])
            # Iterate until we find a collection of sequences with total depth
            # 0.9 * pos <= D <= 1.1 * pos
            idxs_in_range_pos = np.flatnonzero(
                np.abs(cumsum_sizes_shuffled - parameters["pos"])
                <= parameters["pos"] * 0.1
            )
            if len(idxs_in_range_pos):
                num_species_pos = rng.choice(idxs_in_range_pos) + 1
                rand_species_pos = np.sort(unused_species_idxs[:num_species_pos])
                group_sizes_pos = sizes_l[rand_species_pos]
                if np.all(group_sizes_pos > 1):
                    break
        # Create msa of positive examples by concatenating the selected sequences
        rand_idxs_pos_l = []
        rand_idxs_pos_r = []
        for unique_species_idx in rand_species_pos:
            rand_idxs_pos_l += [
                i for i, label in enumerate(inverse_l) if label == unique_species_idx
            ]
            rand_idxs_pos_r += [
                i for i, label in enumerate(inverse_r) if label == unique_species_idx
            ]
        dataset["positive_examples"] = {
            "left": [msa_data[0][i] for i in rand_idxs_pos_l],
            "right": [msa_data[1][i] for i in rand_idxs_pos_r],
        }
        # Print data
        print("\n\nGenerated positive examples")
        print("\tSpecies selected, total number of species selected:")
        print(species_l[rand_species_pos])
        print(rand_species_pos, ",", len(rand_species_pos))
        print("\tPairs per species, total number of pairs:")
        print(group_sizes_pos, ",", sum(group_sizes_pos))
    else:
        dataset["positive_examples"] = None

    if return_species:
        return dataset, group_sizes, species_l[rand_species]
    return dataset, group_sizes


def get_single_and_paired_seqs(
    msa_x: list[tuple[str, str]],
    msa_y: list[tuple[str, str]],
    *,
    group_sizes: Sequence[int],
) -> dict[str, Union[list[list[tuple]], list[dict[str, int]]]]:
    """Single and paired sequences from two MSAs. The paired sequences are returned as a list of
    dictionaries, where the keys are the concatenated sequences and the values are the number of
    times that pair appears in the concatenated MSA."""
    x_seqs_by_group = []
    y_seqs_by_group = []

    idx = 0
    xy_seqs_to_counts_by_group = []
    for s in group_sizes:
        x_seqs_this_group = list(zip(*msa_x[idx : s + idx]))[1]
        x_seqs_by_group.append(x_seqs_this_group)
        y_seqs_this_group = list(zip(*msa_y[idx : s + idx]))[1]
        y_seqs_by_group.append(y_seqs_this_group)
        xy_seqs_this_group = [
            f"{x_seq}:{y_seq}"
            for x_seq, y_seq in zip(x_seqs_this_group, y_seqs_this_group)
        ]
        unique_xy_this_group, counts_xy_this_group = np.unique(
            np.array(xy_seqs_this_group), return_counts=True
        )
        xy_seqs_to_counts_by_group.append(
            dict(zip(unique_xy_this_group, counts_xy_this_group))
        )
        idx += s

    return {
        "x_seqs_by_group": x_seqs_by_group,
        "y_seqs_by_group": y_seqs_by_group,
        "xy_seqs_to_counts_by_group": xy_seqs_to_counts_by_group,
    }


def msa_tokenizer(
    msa: list[tuple[str, str]],
    aa_to_int: Optional[dict[str, int]] = None,
    device: Optional[torch.device] = None,
) -> torch.Tensor:
    """
    Function that given an MSA (seen as a list of tuples) tokenizes it using the MSA Transformer
    tokenizer and transform the tokens into one-hot encodings.
    """
    if aa_to_int is None:
        aa_to_int = DEFAULT_AA_TO_INT

    tokenized_msa = []
    for header, seq in msa:
        tokenized_msa.append([aa_to_int[c] for c in seq])
    tokenized_msa = torch.tensor(tokenized_msa, device=device)

    tokenized_msa = torch.nn.functional.one_hot(tokenized_msa).to(torch.float32)

    return tokenized_msa


def dataset_tokenizer(dataset, device: Optional[torch.device] = None):
    """
    Function that given a dictionary `dataset` of MSAs (initial MSA, blocks, positive examples) tokenizes
    each MSA and return them in a dictionary with the same keys.
    """
    dataset_tokens = {}

    with torch.set_grad_enabled(False):
        # Tokenize initial MSA
        dataset_tokens["msa"] = {
            key: msa_tokenizer(dataset["msa"][key], device=device)
            for key in dataset["msa"].keys()
        }
        # Tokenize MSAs of positive examples and concatenate together the correct pairs, returns None
        # if there are no positive examples
        if dataset["positive_examples"] is None:
            dataset_tokens["positive_examples"] = None
        else:
            tmp_pos_examples = {
                key: msa_tokenizer(dataset["positive_examples"][key], device=device)
                for key in dataset["positive_examples"].keys()
            }
            dataset_tokens["positive_examples"] = torch.cat(
                (tmp_pos_examples["left"], tmp_pos_examples["right"][..., 1:, :]), dim=2
            )

        return dataset_tokens
