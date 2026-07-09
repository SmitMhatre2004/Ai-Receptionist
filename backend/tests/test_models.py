import pytest
import pytest_asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import engine
from app.models.user import User
from app.models.enums import (
    UserRole,
    AppointmentStatus,
    ConversationChannel,
    MessageSender,
    DocumentStatus,
    NotificationType,
    NotificationChannel,
    NotificationStatus,
)
from app.models.clinic_settings import ClinicSettings
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.knowledge_document import KnowledgeDocument
from app.models.embedding import Embedding
from app.models.notification import Notification

@pytest_asyncio.fixture
async def db_session():
    """Fixture that runs each test in a transaction and rolls back at the end."""
    connection = await engine.connect()
    transaction = await connection.begin()
    
    session = AsyncSession(bind=connection, expire_on_commit=False)
    
    yield session
    
    await session.close()
    await transaction.rollback()
    await connection.close()
    await engine.dispose()  # Prevent pool connections reuse on closed loop


@pytest.mark.asyncio
async def test_user_crud(db_session: AsyncSession):
    # Create
    new_user = User(
        full_name="Dr. Jane Doe",
        email="jane.doe@example.com",
        hashed_password="securepasswordhash",
        role=UserRole.ADMIN,
        is_active=True,
    )
    db_session.add(new_user)
    await db_session.flush()

    # Read
    stmt = select(User).where(User.email == "jane.doe@example.com")
    result = await db_session.execute(stmt)
    db_user = result.scalar_one_or_none()
    assert db_user is not None
    assert db_user.full_name == "Dr. Jane Doe"
    assert db_user.role == UserRole.ADMIN

    # Update
    db_user.full_name = "Dr. Jane Smith"
    await db_session.flush()

    result = await db_session.execute(stmt)
    updated_user = result.scalar_one()
    assert updated_user.full_name == "Dr. Jane Smith"

    # Delete
    await db_session.delete(updated_user)
    await db_session.flush()

    result = await db_session.execute(stmt)
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_clinic_settings_crud(db_session: AsyncSession):
    # Create
    settings = ClinicSettings(
        clinic_name="Back in Motion Physio",
        timezone="Asia/Kolkata",
        address="123 Health Ave, Mumbai",
        phone="+919876543210",
        working_hours='{"mon": "09:00-17:00"}',
        booking_policy="Book 24h in advance",
        cancellation_policy="24h cancellation notice required",
        whatsapp_enabled=True,
        voice_enabled=True,
    )
    db_session.add(settings)
    await db_session.flush()

    # Read
    stmt = select(ClinicSettings).where(ClinicSettings.clinic_name == "Back in Motion Physio")
    result = await db_session.execute(stmt)
    db_settings = result.scalar_one_or_none()
    assert db_settings is not None
    assert db_settings.timezone == "Asia/Kolkata"
    assert db_settings.whatsapp_enabled is True


@pytest.mark.asyncio
async def test_patient_doctor_appointment_relationship(db_session: AsyncSession):
    # 1. Create Patient
    patient = Patient(
        full_name="John Patient",
        age=34,
        phone="+919999988888",
        email="john.patient@example.com",
        pain_area="Lower Back",
        pain_severity="7/10",
        pain_duration="2 weeks",
    )
    db_session.add(patient)

    # 2. Create Doctor
    doctor = Doctor(
        full_name="Dr. Sarah Specialist",
        specialty="Spine & Lower Back Rehab",
        email="sarah.doc@example.com",
        phone="+918888877777",
        google_calendar_id="cal_sarah@example.com",
    )
    db_session.add(doctor)
    await db_session.flush()

    # 3. Create Appointment
    start = datetime.now(timezone.utc) + timedelta(days=2)
    end = start + timedelta(hours=1)
    appointment = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        start_time=start,
        end_time=end,
        status=AppointmentStatus.SCHEDULED,
        reason="Severe lower back pain stiffness",
        notes="First consultation intake",
    )
    db_session.add(appointment)
    await db_session.flush()

    # Verify relations with selectinload to avoid MissingGreenlet
    stmt = (
        select(Appointment)
        .options(
            selectinload(Appointment.patient).selectinload(Patient.appointments),
            selectinload(Appointment.doctor),
        )
        .where(Appointment.id == appointment.id)
    )
    result = await db_session.execute(stmt)
    db_appointment = result.scalar_one()

    # Check back-populated relations
    assert db_appointment.patient.full_name == "John Patient"
    assert db_appointment.doctor.full_name == "Dr. Sarah Specialist"
    assert len(db_appointment.patient.appointments) == 1


@pytest.mark.asyncio
async def test_conversation_and_messages(db_session: AsyncSession):
    patient = Patient(
        full_name="Jane Chat",
        phone="+917777766666",
    )
    db_session.add(patient)
    await db_session.flush()

    # Create Conversation
    conversation = Conversation(
        patient_id=patient.id,
        channel=ConversationChannel.WHATSAPP,
        external_thread_id="whatsapp_session_123",
        summary="Patient asking about clinic timings.",
    )
    db_session.add(conversation)
    await db_session.flush()

    # Create Messages
    msg1 = Message(
        conversation_id=conversation.id,
        sender=MessageSender.PATIENT,
        content="Hello, what are your opening hours?",
    )
    msg2 = Message(
        conversation_id=conversation.id,
        sender=MessageSender.AI,
        content="We are open Monday to Friday, 9:00 AM to 5:00 PM.",
    )
    db_session.add_all([msg1, msg2])
    await db_session.flush()

    # Query conversation with messages loaded eagerly
    stmt = (
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .where(Conversation.id == conversation.id)
    )
    result = await db_session.execute(stmt)
    db_conversation = result.scalar_one()

    assert len(db_conversation.messages) == 2
    assert db_conversation.messages[0].sender == MessageSender.PATIENT
    assert db_conversation.messages[1].sender == MessageSender.AI


@pytest.mark.asyncio
async def test_knowledge_document_and_embeddings(db_session: AsyncSession):
    # Create Doc
    doc = KnowledgeDocument(
        filename="faq.pdf",
        file_type="pdf",
        storage_path="/uploads/faq.pdf",
        status=DocumentStatus.READY,
    )
    db_session.add(doc)
    await db_session.flush()

    # Create Embeddings
    emb = Embedding(
        document_id=doc.id,
        chunk_index=0,
        chunk_text="Our clinic is located in Mumbai...",
        chroma_id="chroma_uuid_123",
    )
    db_session.add(emb)
    await db_session.flush()

    # Query doc with chunks loaded eagerly
    stmt = (
        select(KnowledgeDocument)
        .options(selectinload(KnowledgeDocument.chunks))
        .where(KnowledgeDocument.id == doc.id)
    )
    result = await db_session.execute(stmt)
    db_doc = result.scalar_one()

    assert len(db_doc.chunks) == 1
    assert db_doc.chunks[0].chroma_id == "chroma_uuid_123"


@pytest.mark.asyncio
async def test_notifications(db_session: AsyncSession):
    patient = Patient(
        full_name="Notification Test Patient",
        phone="+916666655555",
    )
    db_session.add(patient)
    await db_session.flush()

    # Create Notification
    notif = Notification(
        patient_id=patient.id,
        type=NotificationType.APPOINTMENT_REMINDER,
        channel=NotificationChannel.WHATSAPP,
        status=NotificationStatus.PENDING,
        scheduled_for=datetime.now(timezone.utc) + timedelta(hours=24),
        content="Reminder: You have an appointment tomorrow.",
    )
    db_session.add(notif)
    await db_session.flush()

    # Query with patient loaded eagerly
    stmt = (
        select(Notification)
        .options(selectinload(Notification.patient))
        .where(Notification.id == notif.id)
    )
    result = await db_session.execute(stmt)
    db_notif = result.scalar_one()

    assert db_notif.patient.full_name == "Notification Test Patient"
    assert db_notif.status == NotificationStatus.PENDING
