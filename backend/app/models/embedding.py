import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin, UUIDPrimaryKeyMixin


class Embedding(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Metadata for one chunk of a KnowledgeDocument.

    The actual vector lives in ChromaDB — `chroma_id` points to it there.
    Postgres just tracks which chunk belongs to which document and keeps
    the raw text, so the admin dashboard can list/search chunks without
    querying ChromaDB directly.
    """

    __tablename__ = "embeddings"

    document_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("knowledge_documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    chroma_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    document: Mapped["KnowledgeDocument"] = relationship(back_populates="chunks")

    def __repr__(self) -> str:
        return f"<Embedding doc={self.document_id} chunk={self.chunk_index}>"
