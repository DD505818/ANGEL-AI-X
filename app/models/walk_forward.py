"""Walk-forward cross-validation utilities."""

from __future__ import annotations

from typing import Iterable, Iterator, Sequence, Tuple, TypeVar

T = TypeVar("T")


def walk_forward_split(data: Sequence[T], train_size: int, test_size: int) -> Iterator[Tuple[Sequence[T], Sequence[T]]]:
    """Yield rolling train/test splits for walk-forward analysis.

    Args:
        data: Ordered sequence of items.
        train_size: Number of items in each training window.
        test_size: Number of items in each test window.

    Yields:
        Tuples of (train_slice, test_slice).
    """

    if train_size <= 0 or test_size <= 0:
        raise ValueError("train_size and test_size must be positive")
    end = len(data)
    start = 0
    while start + train_size + test_size <= end:
        train = data[start : start + train_size]
        test = data[start + train_size : start + train_size + test_size]
        yield train, test
        start += test_size
