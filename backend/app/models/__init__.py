"""SQLAlchemy ORM models.

Every model must be imported here so Base.metadata is fully populated
before Alembic (or anything calling create_all) inspects it. Import order
doesn't matter for relationships — SQLAlchemy resolves those lazily via
the string references (e.g. Mapped["Patient"]).
"""

from app.models.appointment import Appointment
from app.models.clinic_settings import ClinicSettings
from app.models.conversation import Conversation
from app.models.doctor import Doctor
from app.models.embedding import Embedding
from app.models.knowledge_document import KnowledgeDocument
from app.models.message import Message
from app.models.notification import Notification
from app.models.patient import Patient
from app.models.user import User

__all__ = [
    "Appointment",
    "ClinicSettings",
    "Conversation",
    "Doctor",
    "Embedding",
    "KnowledgeDocument",
    "Message",
    "Notification",
    "Patient",
    "User",
]
