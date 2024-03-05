from sqlalchemy import create_engine, inspect, Column, Integer, String, Float, BigInteger, ForeignKey, DateTime, JSON, \
    UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

def get_model_fields(model):
    """Return a list of field names for a given SQLAlchemy model."""
    return [key for key in inspect(model).attrs.keys()]


class Validator(Base):
    __tablename__ = 'validators'

    id = Column(Integer, primary_key=True)
    operator_address = Column(String, unique=True, index=True)
    consensus_pubkey = Column(String)
    jailed = Column(Integer)  # 0 for false, 1 for true
    status = Column(String)
    tokens = Column(BigInteger)
    delegator_shares = Column(Float)
    moniker = Column(String)
    identity = Column(String)
    website = Column(String)
    security_contact = Column(String)
    details = Column(String)
    commission_rate = Column(Float)
    commission_max_rate = Column(Float)
    commission_max_change_rate = Column(Float)
    min_self_delegation = Column(BigInteger)
    delegators = relationship("Delegator", back_populates="validator")


class Delegator(Base):
    __tablename__ = 'delegators'

    id = Column(Integer, primary_key=True)
    delegator_address = Column(String, index=True)
    validator_address = Column(String, ForeignKey('validators.operator_address'))
    shares = Column(String)  # Storing shares as String due to its precision
    balance_amount = Column(BigInteger)
    balance_denom = Column(String)

    validator = relationship("Validator", back_populates="delegators")


class GovernanceProposal(Base):
    __tablename__ = 'governance_proposals'

    id = Column(Integer, primary_key=True)
    proposal_id = Column(String, nullable=False)
    chain_id = Column(String, nullable=False)
    title = Column(String)
    description = Column(String)
    proposal_type = Column(String)
    status = Column(String)
    yes_votes = Column(BigInteger)
    abstain_votes = Column(BigInteger)
    no_votes = Column(BigInteger)
    no_with_veto_votes = Column(BigInteger)
    submit_time = Column(DateTime)
    deposit_end_time = Column(DateTime)
    total_deposit = Column(JSON)
    voting_start_time = Column(DateTime)
    voting_end_time = Column(DateTime)

    __table_args__ = (UniqueConstraint('proposal_id', 'chain_id', name='_proposal_id_chain_id_uc'),)


# Setup database connection
engine = create_engine('sqlite:///chainsight.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
