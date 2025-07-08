from sqlalchemy import Column, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    job_id = Column(String, primary_key=True, index=True)
    repo_url = Column(String, nullable=False)
    status = Column(String, default='pending')
    progress = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Summary(Base):
    __tablename__ = 'summaries'
    id = Column(String, primary_key=True, index=True)
    job_id = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    summary = Column(String, nullable=False)

class Diff(Base):
    __tablename__ = 'diffs'
    id = Column(String, primary_key=True, index=True)
    job_id = Column(String, nullable=False)
    commit_id = Column(String, nullable=False)
    diff_text = Column(JSON, nullable=False)  # store diff as JSON or text