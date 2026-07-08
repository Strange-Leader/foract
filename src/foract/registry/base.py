from __future__ import annotations

import builtins
from typing import Protocol, TypeVar  # noqa: UP035

from foract.exceptions import RegistryError


class Named(Protocol):
    name: str


T = TypeVar("T", bound=Named)


class Registry[T: Named]:
    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def register(self, item: T) -> None:
        if item.name in self._items:
            raise RegistryError(f"{item.name!r} is already registered.")
        self._items[item.name] = item

    def get(self, name: str) -> T:
        try:
            return self._items[name]
        except KeyError:
            raise RegistryError(f"{name!r} is not registered.") from None

    def exists(self, name: str) -> bool:
        return name in self._items

    def remove(self, name: str) -> None:
        if name not in self._items:
            raise RegistryError(f"{name!r} is not registered.")
        del self._items[name]

    def clear(self) -> None:
        self._items.clear()

    def list(self) -> list[T]:
        return list(self._items.values())

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, name: str) -> bool:
        return name in self._items

    def items(self) -> dict[str, T]:
        return self._items

    def names(self) -> builtins.list[str]:
        return list(self._items.keys())
