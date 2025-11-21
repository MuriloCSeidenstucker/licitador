import enum

from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.settings.base import Base


class BidResultEnum(enum.Enum):
    WON = "won"
    LOST = "lost"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"


class BidEntity(Base):

    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    agency = Column(String(200), nullable=False)
    subject = Column(String(300), nullable=False)
    opening_date = Column(Date, nullable=False)
    result = Column(Enum(BidResultEnum), nullable=True)
    awarded_value = Column(Float, nullable=True)

    company = relationship("Company", back_populates="bids")

    def __repr__(self):
        return f"<Bid(agency={self.agency}, result={self.result})>"
