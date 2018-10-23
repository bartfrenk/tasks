from typing import TypeVar, Any, List, Tuple

K = TypeVar("K")
V = TypeVar("V")
AList = List[Tuple[K, V]]


def update(alist: AList[K, Any], key: K, value: Any):
    for (i, (k, _)) in enumerate(alist):
        if key == k:
            alist[i] = (key, value)
