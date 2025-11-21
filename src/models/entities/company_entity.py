from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.settings.base import Base


class CompanyEntity(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=False)

    documents = relationship(
        "Document", back_populates="company", cascade="all, delete-orphan"
    )

    bids = relationship("Bid", back_populates="company", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Company(name={self.name}, tax_id={self.tax_id})>"
