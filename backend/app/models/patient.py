from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin, UUIDPrimaryKeyMixin


class Patient(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A clinic patient. Created the first time someone books or chats in —
    phone number is the natural dedup key across web chat / WhatsApp / voice.
    """

    __tablename__ = "patients"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    phone: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # --- Intake fields collected by the AI receptionist (Patient Intake phase) ---
    pain_area: Mapped[str | None] = mapped_column(String(255), nullable=True)
    pain_severity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    pain_duration: Mapped[str | None] = mapped_column(String(255), nullable=True)
    injury_history: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    previous_treatment: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    appointments: Mapped[list["Appointment"]] = relationship(back_populates="patient")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="patient")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="patient")

    def __repr__(self) -> str:
        return f"<Patient {self.full_name}>"
