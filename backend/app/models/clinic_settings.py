from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.common import TimestampMixin, UUIDPrimaryKeyMixin


class ClinicSettings(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """One row per clinic. Today this project runs one clinic, so there will
    only ever be a single row — but keeping it as a table (not hardcoded
    config) is what makes the "adapt this for dentists/salons/vets later"
    goal in your original spec actually possible: a future multi-tenant
    version just adds a tenant_id column here instead of restructuring.
    """

    __tablename__ = "clinic_settings"

    clinic_name: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(100), nullable=False, default="Asia/Kolkata")
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)

    working_hours: Mapped[str | None] = mapped_column(String(1000), nullable=True)  # JSON-encoded weekly schedule
    booking_policy: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    cancellation_policy: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    whatsapp_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    voice_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<ClinicSettings {self.clinic_name}>"
