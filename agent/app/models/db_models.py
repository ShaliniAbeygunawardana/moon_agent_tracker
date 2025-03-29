from sqlalchemy import Column, String, Integer, ForeignKey, Text, DECIMAL, Enum, TIMESTAMP, func, CHAR
from sqlalchemy.orm import relationship, declarative_base
import uuid
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class Branch(Base):
    __tablename__ = "branch"

    branch_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    branch_name = Column(String(255), nullable=False, unique=True)
    location = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    agents = relationship("Agent", back_populates="branch")


class Agent(Base):
    __tablename__ = "agent"

    agent_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_code = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    branch_id = Column(CHAR(36), ForeignKey("branch.branch_id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    branch = relationship("Branch", back_populates="agents")
    products = relationship("ProductPermission", back_populates="agent")


class Product(Base):
    __tablename__ = "product"

    product_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class ProductPermission(Base):
    __tablename__ = "product_permission"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(CHAR(36), ForeignKey("agent.agent_id"), nullable=False)
    product_id = Column(CHAR(36), ForeignKey("product.product_id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    agent = relationship("Agent", back_populates="products")
    product = relationship("Product")


class SalesTransaction(Base):
    __tablename__ = "sales_transaction"

    transaction_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(CHAR(36), ForeignKey("agent.agent_id"), nullable=False)
    product_id = Column(CHAR(36), ForeignKey("product.product_id"), nullable=False)
    sale_amount = Column(DECIMAL(10, 2), nullable=False)
    sale_date = Column(TIMESTAMP, server_default=func.now())
    core_reference_id = Column(String(100), unique=True, nullable=False)

    agent = relationship("Agent")
    product = relationship("Product")


class Notification(Base):
    __tablename__ = "notification"

    notification_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(CHAR(36), ForeignKey("agent.agent_id"), nullable=True)
    recipient_email = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum("PENDING", "SENT", "FAILED", name="notification_status"), default="PENDING")
    created_at = Column(TIMESTAMP, server_default=func.now())

    agent = relationship("Agent", foreign_keys=[agent_id])


def init_db(engine):
    try:
        Base.metadata.create_all(engine)
        logger.info("Tables created")
    except Exception as e:
        logger.error("Error while creating tables")
        logger.error(e)
        raise e
