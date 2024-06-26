# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/sequence_similarity_ops.ipynb.

# %% auto 0
__all__ = ['smooth_hamming_similarities_cdist', 'smooth_hamming_similarities_dot',
           'smooth_substitution_matrix_similarities_cdist', 'smooth_substitution_matrix_similarities_dot',
           'soft_best_hits', 'hard_best_hits']

# %% ../nbs/sequence_similarity_ops.ipynb 3
# Stdlib imports
from collections.abc import Sequence
from typing import Optional, Union

# PyTorch
import torch
from torch.nn.functional import softmax


def smooth_hamming_similarities_cdist(x: torch.Tensor, p: float = 1.0) -> torch.Tensor:
    """Smooth extension of the normalized Hamming similarity between all pairs of sequences in `x`.
    `x` must have shape (..., N, L, R), and the result has shape (..., N, N)."""
    length = x.shape[-2]
    x = x.flatten(start_dim=-2)
    norm_similarities = 1 - (torch.cdist(x, x, p=p) ** p) / (2 * length)

    return norm_similarities


def smooth_hamming_similarities_dot(x: torch.Tensor) -> torch.Tensor:
    """Smooth extension of the normalized Hamming similarity between all pairs of sequences in `x`.
    `x` must have shape (..., N, L, R), and the result has shape (..., N, N)."""
    length = x.shape[-2]
    norm_similarities = torch.einsum("...mia,...nia->...mn", x, x) / length

    return norm_similarities


def smooth_substitution_matrix_similarities_cdist(
    x: torch.Tensor, subs_mat: torch.Tensor, p: float = 1.0
) -> torch.Tensor:
    """TODO."""
    x = torch.einsum("ab,...nib->...nia", subs_mat, x).flatten(start_dim=-2)
    scores = -torch.cdist(x, x, p=p) ** p

    return scores


def smooth_substitution_matrix_similarities_dot(
    x: torch.Tensor,
    subs_mat: torch.Tensor,
    use_scoredist: bool = False,
    expected_value: Optional[float] = None,
) -> torch.Tensor:
    """TODO."""
    length = x.shape[-2]
    scores = torch.einsum("...mia,ab,...nib->...mn", x, subs_mat, x)
    if use_scoredist:
        # ScoreDist: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-6-108
        expected_scores_null = expected_value * length
        scores_norm = torch.clamp(scores - expected_scores_null, min=1e-8)
        diagonal_scores = scores.diagonal(dim1=-2, dim2=-1)
        score_upper_bounds = (
            diagonal_scores.unsqueeze(-1) + diagonal_scores.unsqueeze(-2)
        ) / 2
        score_upper_bounds_norm = score_upper_bounds - expected_scores_null

        return torch.log(scores_norm / score_upper_bounds_norm)

    return scores


def _reciprocate_best_hits(best_hits: torch.Tensor) -> torch.Tensor:
    """Point-wise multiply best hits graphs with their transpose to obtain
    reciprocal best hits graphs. `best_hits` must have shape (..., N, N)."""
    return best_hits * best_hits.mT


def soft_best_hits(
    similarities: torch.Tensor,
    *,
    reciprocal: bool = False,
    group_slices: Sequence[slice],
    tau: Union[float, torch.Tensor] = 0.1,
) -> torch.Tensor:
    """Soft reciprocal best hits graphs from pairwise similarities.
    `similarities` must have shape (..., N, N). The main diagonal is
    excluded by setting its entries to minus infinity before softmax."""
    best_hits = torch.empty_like(similarities)
    inf_diag = torch.zeros(
        similarities.shape[-2:],
        device=similarities.device,
        dtype=similarities.dtype,
        layout=similarities.layout,
    )
    inf_diag.diagonal().fill_(torch.inf)
    similarities = similarities - inf_diag
    for sl in group_slices:
        best_hits[..., sl].copy_(softmax(similarities[..., sl] / tau, dim=-1))

    if reciprocal:
        best_hits = _reciprocate_best_hits(best_hits)

    return best_hits


def hard_best_hits(
    similarities: torch.Tensor,
    *,
    reciprocal: bool = False,
    group_slices: Sequence[slice],
) -> torch.Tensor:
    """Hard reciprocal best hits graphs from pairwise similarities.
    `similarities` must have shape (..., N, N). The main diagonal is
    excluded by setting its entries to minus infinity before argmax."""
    best_hits = torch.zeros_like(similarities, requires_grad=False)
    inf_diag = torch.zeros(
        similarities.shape[-2:],
        device=similarities.device,
        dtype=similarities.dtype,
        layout=similarities.layout,
    )
    inf_diag.diagonal().fill_(torch.inf)
    similarities = similarities - inf_diag
    for sl in group_slices:
        argmax = torch.argmax(similarities[..., sl], dim=-1, keepdim=True)
        best_hits[..., sl].scatter_(-1, argmax, 1.0)

    if reciprocal:
        best_hits = _reciprocate_best_hits(best_hits)

    return best_hits
