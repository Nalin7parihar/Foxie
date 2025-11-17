from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models with automatic table name and timestamps."""

    # All models will automatically get an 'id' primary key using new syntax
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # All models will get created_at and updated_at timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
