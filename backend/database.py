from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from datetime import datetime
import enum

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class StatusEnum(enum.Enum): # Python feature for creating a fixed set of named constants.
    draft = "draft"
    pending = "pending"
    published = "published"
    needs_changes = "needs-changes"
    
class ModeEnum(enum.Enum):
    in_person = "in_person"
    online = "online"
    hybrid = "hybrid"

class Hackathon(db.Model):
    __tablename__ = "hackathon"
    id: Mapped[str] = mapped_column(String,primary_key=True)
    name: Mapped[str] = mapped_column(String,nullable=False) #name REQUIRED
    description: Mapped[str] = mapped_column(String,nullable=True)
    url: Mapped[str] = mapped_column(String,nullable=False) #official link REQUIRED
    startDate: Mapped[datetime] = mapped_column(DateTime,nullable=True) # ISO 8601 date (des to meta)
    endDate: Mapped[datetime] = mapped_column(DateTime,nullable=True) # ISO 8601 date (des to meta)
    location: Mapped[str] = mapped_column(String,nullable=True)
    mode: Mapped[ModeEnum] = mapped_column(Enum(ModeEnum),nullable=True) # sqlalchemy's Enum(ModeEnum) restricts this column to only those values: in-person,online,hybrid
    organizer: Mapped[str] = mapped_column(String,nullable=True)
    hasPrize: Mapped[bool] = mapped_column(Boolean,nullable=True)
    prizeDetails: Mapped[str] = mapped_column(String,nullable=True)
    tags: Mapped[str] = mapped_column(String,nullable=True)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum),nullable=True) # sqlalchemy's Enum(StatusEnum) restricts this column to only those values: draft,pending,published,needs-change 
    submittedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),nullable=True)
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),nullable=True)
    interestCount: Mapped[int] = mapped_column(Integer,nullable=True)