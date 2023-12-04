import uuid

from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Video(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    title = Column(String)
    description = Column(String)
    filename = Column(String)
    owner = relationship('User')
