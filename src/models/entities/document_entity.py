from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.settings.base import Base


class DocumentEntity(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    doc_type = Column(String(120), nullable=False)
    expiration_date = Column(Date, nullable=False)
    file_path = Column(String(255), nullable=True)

    company = relationship("Company", back_populates="documents")

    def __repr__(self):
        return f"<Document(type={self.doc_type}, expiration={self.expiration_date})>"
