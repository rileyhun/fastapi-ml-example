from sqlalchemy import Float, Text, DateTime, Column, String
from sqlalchemy.sql import func
from app.models.database import Base

class PredictionMetrics(Base):

    __tablename__ = 'ml_model_results'

    job_id = Column(String(255))
    content_identifier = Column(String(50), nullable=False, primary_key=True)
    version = Column(String(5), nullable=False, primary_key=True)
    model_predict = Column(Float)
    model_proba = Column(Float)
    request_json = Column(Text)
    response_json = Column(Text)
    created_on = Column(DateTime, server_default=func.now())
    last_modified_on = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
