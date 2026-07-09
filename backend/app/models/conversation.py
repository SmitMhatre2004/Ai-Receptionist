import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ConversationChannel


class Conversation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """One conversation thread, regardless of channel. A returning patient's
    memory (Memory phase) works by looking up past Conversations by
    patient_id and summarizing them back into context.
    """

    __tablename__ = "conversations"

    patient_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("patients.id", ondelete="SET NULL"), nullable=True, index=True
    )

    channel: Mapped[ConversationChannel] = mapped_column(
        SAEnum(ConversationChannel, name="conversation_channel"), nullable=False
    )
    # WhatsApp number, Vapi call id, or web session id — whatever the channel
    # uses to identify "this same thread" before we've matched it to a patient.
    external_thread_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    summary: Mapped[str | None] = mapped_column(String(4000), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    patient: Mapped["Patient | None"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at"
    )

    def __repr__(self) -> str:
        return f"<Conversation {self.id} ({self.channel})>"
