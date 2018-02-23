from sqlalchemy import Column, Integer, Unicode, UniqueConstraint, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


SQLBase = declarative_base()
