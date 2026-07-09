"""Enums shared across models. Kept in one place so `app/tools/` and
`app/services/` (later phases) can import the same vocabulary the DB uses,
instead of comparing against magic strings.
"""

import enum


class UserRole(str, enum.Enum):
    """Roles for dashboard/staff logins — not patients."""

    ADMIN = "admin"
    STAFF = "staff"
    DOCTOR = "doctor"


class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class ConversationChannel(str, enum.Enum):
    WEB_CHAT = "web_chat"
    WHATSAPP = "whatsapp"
    VOICE = "voice"


class MessageSender(str, enum.Enum):
    PATIENT = "patient"
    AI = "ai"
    STAFF = "staff"
    SYSTEM = "system"


class DocumentStatus(str, enum.Enum):
    """Lifecycle of an uploaded knowledge-base document through the RAG
    ingestion pipeline (chunking + embedding), built in the RAG phase.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class NotificationChannel(str, enum.Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    SMS = "sms"


class NotificationType(str, enum.Enum):
    APPOINTMENT_CONFIRMATION = "appointment_confirmation"
    APPOINTMENT_REMINDER = "appointment_reminder"
    APPOINTMENT_CANCELLATION = "appointment_cancellation"
    FOLLOW_UP = "follow_up"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
