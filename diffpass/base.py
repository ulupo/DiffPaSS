# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/base.ipynb.

# %% auto 0
__all__ = ['INGROUP_IDX_DTYPE', 'BootstrapList', 'GradientDescentList', 'GroupByGroupList', 'IndexPair', 'IndexPairsInGroup',
           'IndexPairsInGroups', 'dccn', 'make_pbar', 'DiffPaSSResults', 'DiffPaSSModel']

# %% ../nbs/base.ipynb 4
# Stdlib imports
from copy import deepcopy
from typing import Optional, Any, Sequence, Union
from dataclasses import fields, dataclass, replace

# Progress bars
from tqdm import tqdm

# NumPy
import numpy as np

# PyTorch
import torch
from torch.nn import Module

# DiffPaSS imports
from diffpass.model import (
    GeneralizedPermutation,
    Blosum62Similarities,
    HammingSimilarities,
    BestHits,
)

# Constants
INGROUP_IDX_DTYPE = np.int16

# Type aliases
BootstrapList = list  # List indexed by bootstrap iteration
GradientDescentList = list  # List indexed by gradient descent iteration
GroupByGroupList = list  # List indexed by group index

IndexPair = tuple[int, int]  # Pair of indices
IndexPairsInGroup = list[IndexPair]  # Pairs of indices in a group of sequences
IndexPairsInGroups = list[IndexPairsInGroup]  # Pairs of indices in groups of sequences

# %% ../nbs/base.ipynb 6
def dccn(x: torch.Tensor) -> np.ndarray:
    return x.detach().clone().cpu().numpy()


def make_pbar(epochs: int, show_pbar: bool) -> Any:
    if show_pbar:
        return tqdm(range(epochs + 1))
    return range(epochs + 1)


@dataclass
class DiffPaSSResults:
    """Container for results of DiffPaSS fits."""

    # Optionally, log-alphas for fine-grained information
    log_alphas: Optional[
        Union[
            GradientDescentList[GroupByGroupList[np.ndarray]],
            BootstrapList[GradientDescentList[GroupByGroupList[np.ndarray]]],
        ]
    ]
    # Soft permutations
    soft_perms: Optional[
        Union[
            GradientDescentList[GroupByGroupList[np.ndarray]],
            BootstrapList[GradientDescentList[GroupByGroupList[np.ndarray]]],
        ]
    ]
    # Hard permutations
    hard_perms: Union[
        GradientDescentList[GroupByGroupList[np.ndarray]],
        BootstrapList[GradientDescentList[GroupByGroupList[np.ndarray]]],
    ]
    # Hard losses
    hard_losses: Union[
        GradientDescentList[float],
        GradientDescentList[np.ndarray],
        BootstrapList[GradientDescentList[float]],
    ]
    # Soft losses
    soft_losses: Optional[
        Union[
            GradientDescentList[float],
            BootstrapList[GradientDescentList[float]],
        ]
    ]


class DiffPaSSModel(Module):
    """Base class for DiffPaSS models."""

    allowed_permutation_cfg_keys = {
        "tau",
        "n_iter",
        "noise",
        "noise_factor",
        "noise_std",
    }
    allowed_information_measures = {"MI", "TwoBodyEntropy"}
    allowed_similarity_kinds = {"Hamming", "Blosum62"}
    allowed_similarities_cfg_keys = {
        "Hamming": {"use_dot", "p"},
        "Blosum62": {"use_dot", "p", "use_scoredist", "aa_to_int", "gaps_as_stars"},
    }
    allowed_best_hits_cfg_keys = {"tau", "reciprocal"}

    group_sizes: Sequence[int]
    fixed_pairings: Optional[IndexPairsInGroups]
    permutation_cfg: Optional[dict[str, Any]]
    effective_permutation_cfg_: dict[str, Any]
    information_measure: str
    similarity_kind: str
    similarities_cfg: Optional[dict[str, Any]]
    effective_similarities_cfg_: dict[str, Any]
    permutation: GeneralizedPermutation
    similarities: Union[Blosum62Similarities, HammingSimilarities]
    compute_in_group_best_hits: bool
    best_hits_cfg: Optional[dict[str, Any]]
    effective_best_hits_cfg_: dict[str, Any]
    best_hits: BestHits

    single_fit_default_cfg = {
        "epochs": 1,
        "optimizer_name": "SGD",
        "optimizer_kwargs": None,
        "mean_centering": False,
        "show_pbar": False,
        "compute_final_soft": False,
        "record_log_alphas": False,
        "record_soft_perms": False,
        "record_soft_losses": False,
    }

    @staticmethod
    def reduce_num_tokens(x: torch.Tensor) -> torch.Tensor:
        """Reduce the number of tokens in a one-hot encoded tensor."""
        used_tokens = x.clone()
        for _ in range(x.ndim - 1):
            used_tokens = used_tokens.any(-2)

        return x[..., used_tokens]

    def validate_permutation_cfg(self, permutation_cfg: Optional[dict]) -> None:
        if permutation_cfg is None:
            return
        if not set(permutation_cfg).issubset(self.allowed_permutation_cfg_keys):
            raise ValueError(
                f"Invalid keys in `permutation_cfg`: "
                f"{set(permutation_cfg) - self.allowed_permutation_cfg_keys}"
            )

    def validate_information_measure(self, information_measure: str) -> None:
        if information_measure not in self.allowed_information_measures:
            raise ValueError(
                f"Invalid information measure: {self.information_measure}. "
                f"Allowed values are: {self.allowed_information_measures}"
            )

    def validate_similarity_kind(self, similarity_kind: str) -> None:
        if similarity_kind not in self.allowed_similarity_kinds:
            raise ValueError(
                f"Invalid similarity kind: {self.similarity_kind}. "
                f"Allowed values are: {self.allowed_similarity_kinds}"
            )

    def validate_similarities_cfg(self, similarities_cfg: Optional[dict]) -> None:
        if similarities_cfg is None:
            return
        if not set(similarities_cfg).issubset(
            self.allowed_similarities_cfg_keys[self.similarity_kind]
        ):
            raise ValueError(
                f"Invalid keys in `similarities_cfg`: "
                f"{set(similarities_cfg) - self.allowed_similarities_cfg_keys[self.similarity_kind]}"
            )

    def validate_best_hits_cfg(self, best_hits_cfg: Optional[dict]) -> None:
        if best_hits_cfg is None:
            return
        if not set(best_hits_cfg).issubset(self.allowed_best_hits_cfg_keys):
            raise ValueError(
                f"Invalid keys in `best_hits_cfg`: "
                f"{set(best_hits_cfg) - self.allowed_best_hits_cfg_keys}"
            )

    def init_permutation(
        self,
        group_sizes: Sequence[int],
        fixed_pairings: Optional[IndexPairsInGroups] = None,
        permutation_cfg: Optional[dict[str, Any]] = None,
    ) -> None:
        self.group_sizes = tuple(s for s in group_sizes)
        self.fixed_pairings = fixed_pairings
        self.permutation_cfg = permutation_cfg

        # Validate GeneralizedPermutation config
        self.validate_permutation_cfg(permutation_cfg)
        if self.permutation_cfg is None:
            self.effective_permutation_cfg_ = {}
        else:
            self.effective_permutation_cfg_ = deepcopy(self.permutation_cfg)

        self.permutation = GeneralizedPermutation(
            group_sizes=self.group_sizes,
            fixed_pairings=self.fixed_pairings,
            mode="soft",
            **self.effective_permutation_cfg_,
        )

    def init_similarities(
        self, similarity_kind: str, similarities_cfg: Optional[dict[str, Any]] = None
    ) -> None:
        self.validate_similarity_kind(similarity_kind)
        self.similarity_kind = similarity_kind
        self.validate_similarities_cfg(similarities_cfg)
        self.similarities_cfg = similarities_cfg
        if self.similarities_cfg is None:
            self.effective_similarities_cfg_ = {}
        else:
            self.effective_similarities_cfg_ = deepcopy(self.similarities_cfg)
        if similarity_kind == "Blosum62":
            self.similarities = Blosum62Similarities(**self.effective_similarities_cfg_)
        elif similarity_kind == "Hamming":
            self.similarities = HammingSimilarities(**self.effective_similarities_cfg_)

    def init_best_hits(self, best_hits_cfg: Optional[dict[str, Any]] = None) -> None:
        self.validate_best_hits_cfg(best_hits_cfg)
        self.best_hits_cfg = best_hits_cfg
        if self.best_hits_cfg is None:
            self.effective_best_hits_cfg_ = {}
        else:
            self.effective_best_hits_cfg_ = deepcopy(self.best_hits_cfg)
        self.best_hits = BestHits(
            group_sizes=self.group_sizes if self.compute_in_group_best_hits else None,
            mode="soft",
            **self.effective_best_hits_cfg_,
        )

    def validate_inputs(
        self,
        x: torch.Tensor,
        y: torch.Tensor,
        *,
        check_same_alphabet_size: bool = True,
    ) -> None:
        """Validate input tensors representing aligned objects or (dis)similarity matrices."""
        size_x, size_y = x.shape[0], y.shape[0]
        if size_x != size_y:
            raise ValueError(f"Size mismatch between x ({size_x}) and y ({size_y}).")

        if self.are_inputs_msas:
            if x.ndim != 3 or y.ndim != 3:
                raise ValueError(
                    "Inputs must be 3D tensors of shape (n_samples, length, alphabet_size)."
                )
            _, alphabet_size_x = x.shape[1:]
            _, alphabet_size_y = y.shape[1:]
            if check_same_alphabet_size and (alphabet_size_x != alphabet_size_y):
                raise ValueError("Inputs must have the same alphabet size.")
        elif x.ndim != 2 or y.ndim != 2:
            raise ValueError(
                "Inputs must be 2D square tensors of shape (n_samples, n_samples)."
            )
        elif x.shape[1] != size_x or y.shape[1] != size_y:
            raise ValueError(
                "Inputs must be square tensors of shape (n_samples, n_samples)."
            )

        # Validate group_sizes attribute
        n_samples = sum(self.group_sizes)
        if size_x != n_samples:
            raise ValueError(
                f"Inputs have {n_samples} samples but `group_sizes` implies a total "
                f"of {n_samples} samples."
            )

    def create_optimizer(
        self,
        optimizer_name: Optional[str] = single_fit_default_cfg["optimizer_name"],
        optimizer_kwargs: Optional[dict[str, Any]] = single_fit_default_cfg[
            "optimizer_kwargs"
        ],
    ) -> torch.optim.Optimizer:
        optimizer_cls = getattr(torch.optim, optimizer_name)
        optimizer_kwargs = (
            {"lr": 1e-1} if optimizer_kwargs is None else deepcopy(optimizer_kwargs)
        )
        optimizer = optimizer_cls(self.parameters(), **optimizer_kwargs)
        optimizer.zero_grad()

        return optimizer

    def soft_(self) -> None:
        # Iterate through all child modules and call their soft_ method
        for module in self.children():
            if hasattr(module, "soft_"):
                module.soft_()

    def hard_(self) -> None:
        # Iterate through all child modules and call their hard_ method
        for module in self.children():
            if hasattr(module, "hard_"):
                module.hard_()

    def _hard_pass(
        self, x: torch.Tensor, y: Optional[torch.Tensor], *, results: DiffPaSSResults
    ) -> None:
        self.hard_()
        with torch.no_grad():
            out = self(x, y)
            perms = out["perms"]
            loss = out["loss"]
            results.hard_perms.append(
                [
                    dccn(perms_this_group).argmax(axis=-1).astype(INGROUP_IDX_DTYPE)
                    for perms_this_group in perms
                ]
            )
            results.hard_losses.append(
                dccn(loss) if self.permutation.batch_size is not None else loss.item()
            )

    def _soft_pass(
        self,
        x: torch.Tensor,
        y: torch.Tensor,
        *,
        results: DiffPaSSResults,
        record_soft_perms: bool = False,
        record_soft_losses: bool = False,
    ) -> torch.Tensor:
        self.soft_()
        out = self(x, y)
        perms = out["perms"]
        loss = out["loss"]
        if record_soft_perms:
            results.soft_perms.append(
                [dccn(perms_this_group) for perms_this_group in perms]
            )
        if record_soft_losses:
            results.soft_losses.append(loss.item())

        return loss

    def _record_current_log_alphas(self, results: DiffPaSSResults) -> None:
        results.log_alphas.append(
            [dccn(log_alpha) for log_alpha in self.permutation.log_alphas]
        )

    @staticmethod
    def _init_results(
        *,
        record_log_alphas: bool = single_fit_default_cfg["record_log_alphas"],
        record_soft_perms: bool = single_fit_default_cfg["record_soft_perms"],
        record_soft_losses: bool = single_fit_default_cfg["record_soft_losses"],
    ) -> DiffPaSSResults:
        """Initialize DiffPaSSResults object."""
        results = DiffPaSSResults(
            log_alphas=[] if record_log_alphas else None,
            soft_perms=[] if record_soft_perms else None,
            hard_perms=[],
            soft_losses=[] if record_soft_losses else None,
            hard_losses=[],
        )

        return results

    def check_can_optimize(self) -> bool:
        n_samples = sum(self.group_sizes)
        n_effectively_fixed = np.array(self.permutation._total_number_fixed_pairings)

        return np.all(n_effectively_fixed < n_samples)

    def mean_center_log_alphas(self) -> None:
        with torch.no_grad():
            for log_alpha in self.permutation.log_alphas:
                log_alpha[...] -= log_alpha.mean(dim=(-1, -2), keepdim=True)

    def _fit(
        self,
        x: torch.Tensor,
        y: torch.Tensor,
        *,
        results: DiffPaSSResults,
        epochs: int = single_fit_default_cfg["epochs"],
        optimizer_name: Optional[str] = single_fit_default_cfg["optimizer_name"],
        optimizer_kwargs: Optional[dict[str, Any]] = single_fit_default_cfg[
            "optimizer_kwargs"
        ],
        mean_centering: bool = single_fit_default_cfg["mean_centering"],
        show_pbar: bool = single_fit_default_cfg["show_pbar"],
        compute_final_soft: bool = single_fit_default_cfg["compute_final_soft"],
        record_log_alphas: bool = single_fit_default_cfg["record_log_alphas"],
        record_soft_perms: bool = single_fit_default_cfg["record_soft_perms"],
        record_soft_losses: bool = single_fit_default_cfg["record_soft_losses"],
    ) -> bool:
        can_optimize = self.check_can_optimize()
        if can_optimize:
            # Initialize optimizer
            optimizer = self.create_optimizer(optimizer_name, optimizer_kwargs)

            # ------------------------------------------------------------------------------------------
            ## Gradient descent
            # ------------------------------------------------------------------------------------------
            pbar = make_pbar(epochs, show_pbar)
            for i in pbar:
                # Record current log_alphas
                if record_log_alphas:
                    self._record_current_log_alphas(results)

                # Hard pass
                self._hard_pass(x, y, results=results)

                # Soft pass and backward step
                if i < epochs:
                    loss = self._soft_pass(
                        x,
                        y,
                        results=results,
                        record_soft_perms=record_soft_perms,
                        record_soft_losses=record_soft_losses,
                    )
                    loss.sum().backward()
                    optimizer.step()
                    optimizer.zero_grad()
                    if mean_centering:
                        self.mean_center_log_alphas()
                elif compute_final_soft:
                    with torch.no_grad():
                        self._soft_pass(
                            x,
                            y,
                            results=results,
                            record_soft_perms=record_soft_perms,
                            record_soft_losses=record_soft_losses,
                        )
        else:
            # Just optionally record current log_alphas and do a single hard pass
            if record_log_alphas:
                self._record_current_log_alphas(results)
            self._hard_pass(x, y, results=results)

        return can_optimize

    def fit(
        self,
        x: torch.Tensor,  # The object (MSA or adjacency matrix of graphs) to be permuted
        y: torch.Tensor,  # The target object (MSA or adjacency matrix of graphs), that the objects represented by `x` should be paired with. Not acted upon by soft/hard permutations
        *,
        epochs: int = single_fit_default_cfg[
            "epochs"
        ],  # Number of gradient descent steps
        optimizer_name: Optional[str] = single_fit_default_cfg[
            "optimizer_name"
        ],  # If not ``None``, name of the optimizer. Default: ``"SGD"``
        optimizer_kwargs: Optional[dict[str, Any]] = single_fit_default_cfg[
            "optimizer_kwargs"
        ],  # If not ``None``, keyword arguments for the optimizer. Default: ``None``
        mean_centering: bool = single_fit_default_cfg[
            "mean_centering"
        ],  # If ``True``, mean-center log-alphas (stopping gradients) after each gradient descent step. Default: ``False``
        show_pbar: bool = single_fit_default_cfg[
            "show_pbar"
        ],  # If ``True``, show progress bar. Default: ``False``
        compute_final_soft: bool = single_fit_default_cfg[
            "compute_final_soft"
        ],  # If ``True``, compute soft permutations and losses after the last gradient descent step. Default: ``False``
        record_log_alphas: bool = single_fit_default_cfg[
            "record_log_alphas"
        ],  # If ``True``, record log-alphas at each gradient descent step. Default: ``False``
        record_soft_perms: bool = single_fit_default_cfg[
            "record_soft_perms"
        ],  # If ``True``, record soft permutations at each gradient descent step. Default: ``False``
        record_soft_losses: bool = single_fit_default_cfg[
            "record_soft_losses"
        ],  # If ``True``, record soft losses at each gradient descent step. Default: ``False``
    ) -> (
        DiffPaSSResults
    ):  # `DiffPaSSResults` container for fit results. All attributes are lists indexed by gradient descent iteration
        """Fit permutations to data using gradient descent."""
        self.prepare_fit(x, y)

        # Initialize DiffPaSSResults object
        results = self._init_results(
            record_log_alphas=record_log_alphas,
            record_soft_perms=record_soft_perms,
            record_soft_losses=record_soft_losses,
        )

        self._fit(
            x,
            y,
            results=results,
            epochs=epochs,
            optimizer_name=optimizer_name,
            optimizer_kwargs=optimizer_kwargs,
            mean_centering=mean_centering,
            show_pbar=show_pbar,
            compute_final_soft=compute_final_soft,
            record_log_alphas=record_log_alphas,
            record_soft_perms=record_soft_perms,
            record_soft_losses=record_soft_losses,
        )

        return results

    def fit_bootstrap(
        self,
        x: torch.Tensor,  # The object (MSA or adjacency matrix of graphs) to be permuted
        y: torch.Tensor,  # The target object (MSA or adjacency matrix of graphs), that the objects represented by `x` should be paired with. Not acted upon by soft/hard permutations
        *,
        n_start: int = 1,  # Number of fixed pairings to choose among the pairs not already fixed by `self.fixed_pairings`, using the results of the first call to `fit`. Default: ``1``
        n_end: Optional[
            int
        ] = None,  # If ``None``, the bootstrap will end when all pairs are fixed. Otherwise, the bootstrap will end when `n_end` pairs are fixed. Default: ``None``
        step_size: int = 1,  # Difference between the number of fixed pairings chosen at consecutive bootstrap iterations. Default: ``1``
        n_repeats: int = 1,  # At each bootstrap iteration, `n_repeats` runs will be performed, and the run with the lowest loss will be chosen. Default: ``1``
        parallelize_repeats: bool = False,  # If ``True``, parallelize the `n_repeats` runs at each bootstrap iteration, by batching. Can cause OOM errors if `n_repeats` is large. Default: ``False``
        show_pbar: bool = True,  # If ``True``, show progress bar. Default: ``True``
        single_fit_cfg: Optional[
            dict
        ] = None,  # If not ``None``, custom configuration dictionary for gradient optimization in each bootstrap iteration (call to `fit`). See `fit` for details. ``None`` means using the default parameters of `fit`. Default: ``None``
    ) -> (
        DiffPaSSResults
    ):  # `DiffPaSSResults` container for fit results. All attributes are lists indexed by bootstrap iteration, containing lists indexed by gradient descent iteration as per `fit`
        """Fit permutations to data using the DiffPaSS bootstrap.

        The DiffPaSS bootstrap consists of a sequence of short gradient descent runs (default: one epoch per run).
        At the end of each run, a subset of the found pairings is chosen uniformly at random
        and fixed for the next run.
        The number of pairings fixed at each iteration ranges between `n_start` (default: 1) and `n_end` (default: total number of pairs), with a step size of `step_size`.
        """
        ########## Preparations ##########

        # Input validation
        self.prepare_fit(x, y)

        # Prepare variables for indexing
        n_samples = len(x)
        n_groups = len(self.group_sizes)
        cumsum_group_sizes = np.cumsum([0] + list(self.group_sizes))
        offsets = np.repeat(cumsum_group_sizes[:-1], repeats=self.group_sizes)
        group_idxs = np.repeat(np.arange(n_groups), repeats=self.group_sizes)

        # Initially fixed pairings as derived from the `fixed_pairings` attribute
        if self.fixed_pairings is None:
            initially_fixed_pairings = [[] for _ in self.group_sizes]
        else:
            initially_fixed_pairings = [list(fm) for fm in self.fixed_pairings]

        # *Effective* initially fixed pairings as global indices (not relative to group)
        # Used to exclude these pairs from the random sampling of new fixed pairings
        # and to determine when the bootstrap will end
        effective_initially_fixed_idxs = []
        for s, efmz in zip(
            cumsum_group_sizes, self.permutation._effective_fixed_pairings_zip
        ):
            if efmz:
                effective_initially_fixed_idxs += [
                    s + efmz_fixed for efmz_fixed in efmz[1]
                ]
        non_initially_fixed_idxs = np.setdiff1d(
            np.arange(n_samples), effective_initially_fixed_idxs
        )
        if n_end is None:
            n_end = n_samples - len(effective_initially_fixed_idxs) - 1
        # Bootstrap range and progress bar
        pbar = range(n_start, n_end, step_size)
        pbar = tqdm(pbar) if show_pbar else pbar

        ########## End preparations ##########

        ########## Closures ##########

        def make_new_fixed_pairings(
            mapped_idxs: np.ndarray, N: int
        ) -> IndexPairsInGroups:
            """Subroutine for randomly sampling new fixed pairings for the next bootstrap iteration."""
            rand_fixed_idxs = np.random.choice(
                non_initially_fixed_idxs, size=N, replace=False
            )
            rand_fixed_idxs = np.sort(rand_fixed_idxs)
            rand_mapped_idxs = mapped_idxs[rand_fixed_idxs]
            rand_group_idxs = group_idxs[rand_fixed_idxs]
            rand_fixed_rel_idxs = rand_fixed_idxs - offsets[rand_fixed_idxs]
            rand_mapped_rel_idxs = rand_mapped_idxs - offsets[rand_mapped_idxs]

            # Update fixed pairings
            fixed_pairings = [[] for _ in range(n_groups)]
            for rand_group_idx, mapped_rel_idx, fixed_rel_idx in zip(
                rand_group_idxs, rand_mapped_rel_idxs, rand_fixed_rel_idxs
            ):
                pair = (mapped_rel_idx, fixed_rel_idx)
                fixed_pairings[rand_group_idx].append(pair)
            fixed_pairings = [
                initially_fixed_pairings[k] + fixed_pairings[k] for k in range(n_groups)
            ]

            return fixed_pairings

        def init_diffpassresults() -> DiffPaSSResults:
            return self._init_results(
                record_log_alphas=single_fit_cfg["record_log_alphas"],
                record_soft_perms=single_fit_cfg["record_soft_perms"],
                record_soft_losses=single_fit_cfg["record_soft_losses"],
            )

        def extend_results_with_lowest_loss_repeat(
            results_this_iter: DiffPaSSResults,
            results: DiffPaSSResults,
            can_optimize: bool,
        ) -> None:
            """Extend the global optimization object `results` with the portion of
            `results_this_iter` (from the latest bootstrap iteration) corresponding to
            the repeat with the lowest hard loss."""
            if can_optimize:
                # Select run with lowest hard loss, discard the rest
                reshaped_hard_losses_this_repeat = np.asarray(
                    results_this_iter.hard_losses
                ).reshape(n_repeats, -1)
                min_loss_idx = np.argmin(reshaped_hard_losses_this_repeat[:, -1])
                size_each_repeat = reshaped_hard_losses_this_repeat.shape[1]
                # Record complete results of the run with the lowest loss
                slice_to_append = slice(
                    min_loss_idx * size_each_repeat,
                    (min_loss_idx + 1) * size_each_repeat,
                )
            else:
                slice_to_append = slice(None)
            [
                getattr(results, field_name).extend(
                    getattr(results_this_iter, field_name)[slice_to_append]
                )
                for field_name in available_fields
            ]

        postprocess_results_after_repeats = (
            extend_results_with_lowest_loss_repeat
            if n_repeats > 1
            else lambda *args: None
        )

        ########## End closures ##########

        # Configuration for each gradient descent run
        _single_fit_cfg = deepcopy(self.single_fit_default_cfg)
        if single_fit_cfg is not None:
            _single_fit_cfg.update(single_fit_cfg)
        if parallelize_repeats:
            # FIXME: This is just a temporary solution to limit memory usage
            _single_fit_cfg["record_log_alphas"] = False
            _single_fit_cfg["record_soft_perms"] = False
            _single_fit_cfg["record_soft_losses"] = False
        single_fit_cfg = _single_fit_cfg

        # Initialize DiffPaSSResults object
        results = init_diffpassresults()
        available_fields = [
            field.name
            for field in fields(results)
            if getattr(results, field.name) is not None
        ]
        field_to_length_so_far = {field_name: 0 for field_name in available_fields}

        ########## Optimization ##########

        # First fit with initially fixed pairings
        can_optimize = self._fit(x, y, results=results, **single_fit_cfg)
        n_iters_with_optimization = int(can_optimize)

        # DiffPaSSResults object for each bootstrap iteration:
        # new object if `n_repeats` > 1, else the existing `results`
        get_results_to_use_in_each_bootstrap_iter = (
            init_diffpassresults if n_repeats > 1 else lambda: results
        )

        # Subsequent bootstrap fits: at a given iteration we use fixed pairings chosen uniformly at
        # random from the results of the previous iteration (excluding the effective initially
        # fixed pairings)
        for N in pbar:
            latest_hard_perms = results.hard_perms[-1]
            mapped_idxs = offsets + np.concatenate(latest_hard_perms)

            field_to_length_so_far = {
                field_name: len(getattr(results, field_name))
                for field_name in available_fields
            }

            results_this_iter = (
                get_results_to_use_in_each_bootstrap_iter()
            )  # `results` alias if `n_repeats` == 1
            if not parallelize_repeats:
                for _ in range(n_repeats):
                    # Randomly sample N fixed pairings
                    fixed_pairings = make_new_fixed_pairings(mapped_idxs, N)
                    # Reinitialize permutation module with new fixed pairings
                    self.permutation.init_batch_size_fixed_pairings_and_log_alphas(
                        batch_size=None,
                        fixed_pairings=fixed_pairings,
                        device=x.device,
                    )
                    # Fit with gradient descent
                    can_optimize = self._fit(
                        x, y, results=results_this_iter, **single_fit_cfg
                    )
                    if not can_optimize:
                        # If we can't fit, we break the "repeats" loop
                        break
            else:
                # Randomly sample N fixed pairings
                fixed_pairings = [
                    make_new_fixed_pairings(mapped_idxs, N) for _ in range(n_repeats)
                ]
                # Reinitialize permutation module with new fixed pairings
                self.permutation.init_batch_size_fixed_pairings_and_log_alphas(
                    batch_size=n_repeats,
                    fixed_pairings=fixed_pairings,
                    device=x.device,
                )
                # Fit with gradient descent
                can_optimize = self._fit(
                    x, y, results=results_this_iter, **single_fit_cfg
                )
                results_this_iter.hard_perms = [
                    [perms_this_group[idx_rep] for perms_this_group in perms_this_epoch]
                    for idx_rep in range(n_repeats)
                    for perms_this_epoch in results_this_iter.hard_perms
                ]
                results_this_iter.hard_losses = [
                    losses_this_epoch[idx_rep]
                    for idx_rep in range(n_repeats)
                    for losses_this_epoch in results_this_iter.hard_losses
                ]

            postprocess_results_after_repeats(
                results_this_iter, results, can_optimize
            )  # Does nothing if `n_repeats` == 1

            if can_optimize:
                n_iters_with_optimization += 1
            else:
                # If we could not fit, terminate the bootstrap
                break

        ########## End optimization ##########

        ########## Post-processing ##########

        # Reshape results according to number of iterations performed
        reshaped_fields = {}
        for field_name in available_fields:
            results_this_field = getattr(results, field_name)
            n_optimized_results_this_field = (
                len(results_this_field)
                if can_optimize
                else field_to_length_so_far[field_name]
            )
            n_unoptimized_results_this_field = (
                len(results_this_field) - n_optimized_results_this_field
            )

            assert not n_optimized_results_this_field % n_iters_with_optimization
            n_in_each_optimized_iter = (
                n_optimized_results_this_field // n_iters_with_optimization
            )
            reshaped_fields[field_name] = [
                results_this_field[
                    j * n_in_each_optimized_iter : (j + 1) * n_in_each_optimized_iter
                ]
                for j in range(n_iters_with_optimization)
            ] + [results_this_field[n_optimized_results_this_field:]] * bool(
                n_unoptimized_results_this_field
            )
        results = replace(results, **reshaped_fields)

        ########## End post-processing ##########

        return results
