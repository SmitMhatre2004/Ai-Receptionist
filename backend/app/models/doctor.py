from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin, UUIDPrimaryKeyMixin


class Doctor(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A physiotherapist who can be booked for appointments."""

    __tablename__ = "doctors"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    specialty: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Which Google Calendar this doctor's availability/bookings live in —
    # used by the Appointment Management phase.
    google_calendar_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    appointments: Mapped[list["Appointment"]] = relationship(back_populates="doctor")

    def __repr__(self) -> str:
        return f"<Doctor {self.full_name}>"
