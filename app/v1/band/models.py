from sqlalchemy import Column, Integer, String, CheckConstraint
from ..config import Base

class Band(Base):
    """
    SQLAlchemy model for the 'band' table.
    """
    __tablename__ = "band"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    image = Column(String(255), nullable=True)
