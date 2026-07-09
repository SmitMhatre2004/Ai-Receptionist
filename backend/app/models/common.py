"""Shared mixins used by every model, so each table gets a consistent
UUID primary key and created_at/updated_at pair without repeating the
column definitions everywhere.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPrimaryKeyMixin:
    """UUID primary keys instead of auto-increment ints.

    Chosen deliberately: appointment/patient IDs will eventually be exposed
    in URLs, WhatsApp deep links, and calendar event metadata — UUIDs avoid
    leaking sequential counts (e.g. "how many patients does this clinic
    have") and make merging data across clinics (multi-tenant future)
    conflict-free.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
