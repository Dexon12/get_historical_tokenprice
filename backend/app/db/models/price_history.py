from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.database import Base
from backend.extra.network_slug import NetworkSlug


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Первичный ключ

    token: Mapped[str] = mapped_column(String(255), nullable=False) 
    token_in: Mapped[str] = mapped_column(String(255), nullable=False) 
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)  
    
    network: Mapped[NetworkSlug] = mapped_column(
        Enum(NetworkSlug), name="network", nullable=False
    )

    price: Mapped[int] = mapped_column(Integer, nullable=False)
    
    round_id: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        Index("ix_price_history_token", "token"),
        Index("ix_price_history_token_in", "token_in"),
        Index("ix_price_history_timestamp", "timestamp"),
        UniqueConstraint("token", "token_in", "network", "timestamp", name="uq_token_price_history"),
    )
