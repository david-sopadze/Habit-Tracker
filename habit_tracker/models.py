from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Habit:
    name: str
    periodicity: str  # "daily" or "weekly"
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    completions: List[str] = field(default_factory=list)  # ISO datetime strings
    is_active: bool = True

    def add_completion(self, ts: Optional[datetime] = None) -> None:
        if ts is None:
            ts = datetime.now()
        self.completions.append(ts.isoformat())

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "periodicity": self.periodicity,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "completions": list(self.completions),
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Habit":
        created_raw = data.get("created_at")
        created_at = datetime.fromisoformat(created_raw) if created_raw else datetime.now()

        return cls(
            name=data["name"],
            periodicity=data["periodicity"],
            description=data.get("description", ""),
            created_at=created_at,
            completions=data.get("completions", []),
            is_active=data.get("is_active", True),
        )


@dataclass
class Task:

    title: str
    urgent: bool
    important: bool
    description: str = ""
    due_datetime: Optional[str] = None  # store as string, e.g., "DD/MM/YY 14:30" or ISO
    created_at: datetime = field(default_factory=datetime.now)
    completed: bool = False

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "urgent": self.urgent,
            "important": self.important,
            "description": self.description,
            "due_datetime": self.due_datetime,
            "created_at": self.created_at.isoformat(),
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        created_raw = data.get("created_at")
        created_at = datetime.fromisoformat(created_raw) if created_raw else datetime.now()

        return cls(
            title=data["title"],
            urgent=bool(data["urgent"]),
            important=bool(data["important"]),
            description=data.get("description", ""),
            due_datetime=data.get("due_datetime"),
            created_at=created_at,
            completed=bool(data.get("completed", False)),
        )
