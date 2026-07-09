import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import MessageSender


class Message(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True
    )

    sender: Mapped[MessageSender] = mapped_column(SAEnum(MessageSender, name="message_sender"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # JSON-encoded record of which tool(s) the agent called for this turn
    # (e.g. {"tool": "check_availability", "args": {...}, "result": {...}}).
    # Populated once the Core AI Agent phase lands; nullable until then.
    tool_calls: Mapped[str | None] = mapped_column(Text, nullable=True)

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message {self.id} ({self.sender})>"
