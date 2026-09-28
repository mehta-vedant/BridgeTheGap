from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Project(Base):
    __tablename__ = "bridge_projects"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    division: Mapped[str] = mapped_column(String(100))
    estimate: Mapped[float] = mapped_column(Numeric(15, 2))
    status: Mapped[str] = mapped_column(String(40), default="NEED_IDENTIFIED")


class Tender(Base):
    __tablename__ = "tenders"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("bridge_projects.id"), unique=True)
    status: Mapped[str] = mapped_column(String(40), default="OPEN")
    contract_id: Mapped[str | None] = mapped_column(String(32), nullable=True)


class Bid(Base):
    __tablename__ = "tender_bids"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    tender_id: Mapped[str] = mapped_column(ForeignKey("tenders.id"))
    contractor: Mapped[str] = mapped_column(String(160))
    amount: Mapped[float] = mapped_column(Numeric(15, 2))


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(40), index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    contractor_name: Mapped[str | None] = mapped_column(String(160), nullable=True)


class Bridge(Base):
    __tablename__ = "bridges"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    service_status: Mapped[str] = mapped_column(String(40), default="IN_SERVICE")
    maintenance_status: Mapped[str] = mapped_column(String(40), default="NONE")
    next_inspection: Mapped[str] = mapped_column(String(16))


class WorkOrder(Base):
    __tablename__ = "work_orders"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    bridge_id: Mapped[str] = mapped_column(ForeignKey("bridges.id"))
    description: Mapped[str] = mapped_column(Text)
    contractor: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(40), default="APPROVED")


class LifecycleEvent(Base):
    __tablename__ = "lifecycle_events"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    bridge_id: Mapped[str] = mapped_column(ForeignKey("bridges.id"))
    actor: Mapped[str] = mapped_column(String(100))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
