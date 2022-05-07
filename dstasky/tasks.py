from __future__ import annotations

import uuid
import enum
import datetime
import time

from typing import NamedTuple
from typing import Sequence
from typing import Optional
from typing import Any

class ObjectType(enum.Enum):
    TASK = 'task'
    NOTE = 'note'
    EVENT = 'event'


class Status(enum.Enum):
    CREATED = 'created'
    CLOSED = 'closed'
    REOPENED = 'reopened'
    STARTED = 'started'
    RESUMED = 'resumed'
    PAUSED = 'paused'
    ARCHIVED = 'archived'


class Reason(enum.Enum):
    DUPLICATED = 'duplicated'
    WONTFIX = 'wontfix'
    BLOCKED = 'blocked'
    INVALID = 'invalid'


class ObjectEntry(NamedTuple):
    # Object metadata
    objuuid: uuid.UUID
    objtype: ObjectType

    title: str
    status: Status

    created: datetime.datetime
    modified: datetime.datetime

    # Custom metadata
    metadata: dict[str, str] | None = None

    description: str | None = None
    reason: Reason | None = None

    project: str | None = None
    priority: int | None = None
    tags: Sequence[str] | None = None

    subtasks: Sequence[uuid.UUID] | None = None
    dependencies: Sequence[uuid.UUID] | None = None
    references: Sequence[uuid.UUID] | None = None

    # Date/Time
    resolved: datetime.datetime | None = None
    started: datetime.datetime | None = None
    ended: datetime.datetime | None = None
    scheduled: datetime.datetime | None = None
    due: datetime.datetime | None = None

    def check(self) -> None:
        if self.modified < self.created:
            raise ValueError('Modified time is before created time')

    def to_dict(self) -> dict[str, Any]:
        dct = {
                'uuid': str(self.objuuid),
                'type': self.objtype.value,
                'title': self.title,
            }

        # normal fields
        for field_name in [
                    'description', 'metadata', 'project', 'priority', 'tags',
                ]:
            field: Optional[Any] = getattr(self, field_name)
            if field:
                dct[field_name] = field

        # enum fields
        for field_name in ['status', 'reason']:
            field: enum.Enum = getattr(self, field_name)
            if field:
                dct[field_name] = field.value

        # uuid list fields
        for field_name in ['subtasks', 'dependencies', 'references']:
            field: Sequence[uuid.UUID] | None = getattr(self, field_name)
            if field:
                dct[field_name] = [str(u) for u in field]

        # date fields
        for field_name in [
                    'created', 'modified', 'resolved', 'started', 'ended',
                    'scheduled', 'due',
                ]:
            field: datetime.datetime | None = getattr(self, field_name)
            if field:
                dct[field_name] = field.isoformat()

        return dct

    @classmethod
    def create_task(
            cls,
            *,
            title: str,
            objuuid: Optional[uuid.UUID] = None,
            created: Optional[datetime.datetime] = None,
            modified: Optional[datetime.datetime] = None,
            metadata: Optional[dict[str, str]] = None,
            description: Optional[str] = None,
            project: Optional[str] = None,
        ) -> ObjectEntry:

        if created:
            _created = created
        else:
            _created = datetime.datetime.now(datetime.timezone.utc)

        entry = cls(
                objuuid=(objuuid if objuuid else uuid.uuid4()),
                objtype=ObjectType.TASK,
                status=Status.CREATED,
                created=_created,
                modified=(modified if modified else _created),
                title=title,
                metadata=metadata,
                description=description,
                project=project,
            )

        entry.check()
        return entry
