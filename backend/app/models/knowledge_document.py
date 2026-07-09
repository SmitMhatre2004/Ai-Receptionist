from sqlalchemy import String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.common import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import DocumentStatus


class KnowledgeDocument(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """An uploaded clinic document (brochure, FAQ, treatment guide) that
    feeds the RAG pipeline. Rows here track upload/processing state;
    the actual chunk text + vectors are in Embedding / ChromaDB
    (RAG System phase).
    """

    __tablename__ = "knowledge_documents"

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pdf | docx | txt
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)

    status: Mapped[DocumentStatus] = mapped_column(
        SAEnum(DocumentStatus, name="document_status"), default=DocumentStatus.PENDING, nullable=False
    )
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    chunks: Mapped[list["Embedding"]] = relationship(back_populates="document", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<KnowledgeDocument {self.filename}>"
