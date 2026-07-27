"""In-memory repository infrastructure for the Task Tracker application."""

from typing import Generic, TypeVar


ItemType = TypeVar("ItemType")


class InMemoryRepository(Generic[ItemType]):
    """Store application objects in memory using integer identifiers."""

    def __init__(self) -> None:
        """Initialize an empty repository."""

        self._items: dict[int, ItemType] = {}
        self._next_id: int = 1

    def clear(self) -> None:
        """Remove all stored objects and reset ID generation."""

        self._items.clear()
        self._next_id = 1