# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/base.ipynb.

# %% auto 0
__all__ = ['DiffPASSMixin', 'scalar_or_1d_tensor', 'EnsembleMixin']

# %% ../nbs/base.ipynb 2
# Stdlib imports
from collections.abc import Iterable, Sequence
from typing import Optional, Union, Any

# PyTorch
import torch

# %% ../nbs/base.ipynb 3
class DiffPASSMixin:
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
        "Blosum62": {"use_scoredist", "aa_to_int", "gaps_as_stars"},
    }
    allowed_best_hits_cfg_keys = {"tau", "reciprocal"}

    group_sizes: Iterable[int]
    information_measure: str
    similarity_kind: str

    @staticmethod
    def reduce_num_tokens(x: torch.Tensor) -> torch.Tensor:
        """Reduce the number of tokens in a one-hot encoded tensor."""
        used_tokens = x.clone()
        for _ in range(x.ndim - 1):
            used_tokens = used_tokens.any(-2)

        return x[..., used_tokens]

    def validate_permutation_cfg(self, permutation_cfg: dict) -> None:
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

    def validate_similarities_cfg(self, similarities_cfg: dict) -> None:
        if not set(similarities_cfg).issubset(
            self.allowed_similarities_cfg_keys[self.similarity_kind]
        ):
            raise ValueError(
                f"Invalid keys in `similarities_cfg`: "
                f"{set(similarities_cfg) - self.allowed_similarities_cfg_keys[self.similarity_kind]}"
            )

    def validate_best_hits_cfg(self, best_hits_cfg: dict) -> None:
        if not set(best_hits_cfg).issubset(self.allowed_best_hits_cfg_keys):
            raise ValueError(
                f"Invalid keys in `best_hits_cfg`: "
                f"{set(best_hits_cfg) - self.allowed_best_hits_cfg_keys}"
            )

    def validate_inputs(
        self, x: torch.Tensor, y: torch.Tensor, check_same_alphabet_size: bool = False
    ) -> None:
        """Validate input tensors representing aligned objects."""
        size_x, length_x, alphabet_size_x = x.shape
        size_y, length_y, alphabet_size_y = y.shape
        if size_x != size_x:
            raise ValueError(f"Size mismatch between x ({size_x}) and y ({size_y}).")
        if check_same_alphabet_size and (alphabet_size_x != alphabet_size_y):
            raise ValueError("Inputs must have the same alphabet size.")

        # Validate size attribute
        total_size = sum(self.group_sizes)
        if size_x != total_size:
            raise ValueError(
                f"Inputs have size {total_size} but `group_sizes` implies a total "
                f"size of {total_size}."
            )

    @staticmethod
    def check_can_optimize(n_effectively_fixed: int, n_available: int) -> None:
        if n_effectively_fixed == n_available:
            raise ValueError(
                "The number of effectively fixed matchings is equal to the number "
                "of sequences. No optimization can be performed."
            )
        elif n_effectively_fixed > n_available:
            raise ValueError(
                "The number of effectively fixed matchings is greater than the number "
                "of available sequences. Check your inputs."
            )

# %% ../nbs/base.ipynb 4
def scalar_or_1d_tensor(*, param: Any, param_name: str) -> torch.Tensor:
    if not isinstance(param, (int, float, torch.Tensor)):
        raise TypeError(f"`{param_name}` must be a scalar or a torch.Tensor.")
    if not isinstance(param, torch.Tensor):
        param = torch.tensor(param, dtype=torch.get_default_dtype())
    elif param.ndim > 1:
        raise ValueError(
            f"`{param_name}` must be a scalar or a tensor of dimension <= 1."
        )

    return param


class EnsembleMixin:
    def _validate_ensemble_param(
        self,
        *,
        param: Union[float, torch.Tensor],
        param_name: str,
        ensemble_shape: Sequence[int],
        dim_in_ensemble: Optional[int] = None,
        n_dims_per_instance: Optional[int] = None,
    ) -> torch.Tensor:
        param = scalar_or_1d_tensor(param=param, param_name=param_name)

        param = self._reshape_ensemble_param(
            param=param,
            ensemble_shape=ensemble_shape,
            dim_in_ensemble=dim_in_ensemble,
            n_dims_per_instance=n_dims_per_instance,
            param_name=param_name,
        )

        return param

    @staticmethod
    def _reshape_ensemble_param(
        *,
        param: torch.Tensor,
        ensemble_shape: Sequence[int],
        dim_in_ensemble: Optional[int],
        n_dims_per_instance: int,
        param_name: str,
    ) -> torch.Tensor:
        n_ensemble_dims = len(ensemble_shape)
        if param.ndim == 1:
            if dim_in_ensemble is None:
                raise ValueError(
                    f"`dim_in_ensemble` cannot be None if {param_name} is 1D."
                )
            param = param.to(torch.get_default_dtype())
            # If param is not a scalar, broadcast it along the `ensemble_dim`-th ensemble dimension
            if dim_in_ensemble >= n_ensemble_dims or dim_in_ensemble < -n_ensemble_dims:
                raise ValueError(
                    f"Ensemble dimension for {param_name} must be an available index "
                    f"in `ensemble_shape`."
                )
            elif len(param) != ensemble_shape[dim_in_ensemble]:
                raise ValueError(
                    f"Parameter `{param_name}` must have the same length as "
                    f"``ensemble_shape[dim_in_ensemble]`` = "
                    f"{ensemble_shape[dim_in_ensemble]}."
                )
            new_shape = (
                (1,) * dim_in_ensemble
                + param.shape
                + (1,) * (n_ensemble_dims - dim_in_ensemble - 1)
                + (1,) * n_dims_per_instance
            )
            param = param.view(*new_shape)

        return param
