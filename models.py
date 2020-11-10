from time import time

from sqlalchemy import (Column, DateTime, Integer, String, and_, create_engine,
                        or_)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import mytoken as mt

DATABASE_URL = mt.database_url()

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class AmongusPlans(Base):
    __tablename__ = 'amongus_plans'

    id = Column(Integer, primary_key=True)
    guild_id = Column(String)
    channel_id = Column(String)
    author_id = Column(String)
    message_id = Column(String)
    epoch_time = Column(Integer, nullable=False)


class AmongusReactions(Base):
    __tablename__ = 'amongus_reactions'

    id = Column(Integer, primary_key=True)
    message_id = Column(String)
    user_id = Column(String)
    stump = Column(String)
    epoch_time = Column(Integer, nullable=False)


class AmongusUserRanks(Base):
    __tablename__ = 'amongus_userranks'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    time_counts = Column(Integer, server_default = "0")
    epoch_time = Column(Integer, nullable=False)


Base.metadata.create_all(engine)

# CRUD
# - Create
# - Read
# - Update
# - Delete

def create_amongus_plan(guild_id, channel_id, author_id, message_id, epoch_time):
    session = sessionmaker(engine)()
    plan = AmongusPlans(guild_id=guild_id, channel_id=channel_id, author_id=author_id, message_id=message_id, epoch_time=epoch_time)
    session.add(plan)
    session.commit()
    session.close()

def read_amongus_plans():
    session = sessionmaker(engine)()
    plans = session.query(AmongusPlans).all()
    session.close()
    return plans

def create_amongus_reaction(message_id, user_id, stump, epoch_time):
    session = sessionmaker(engine)()
    reaction = AmongusReactions(message_id=message_id, user_id=user_id, stump=stump, epoch_time=epoch_time)
    session.add(reaction)
    session.commit()
    session.close()

def read_amongus_reactions():
    session = sessionmaker(engine)()
    reactions = session.query(AmongusReactions).all()
    session.close()
    return reactions

def update_amongus_reaction(message_id, user_id, stump):
    session = sessionmaker(engine)()
    reaction = session.query(AmongusReactions).filter(
        and_(AmongusReactions.message_id==message_id, AmongusReactions.user_id==user_id
        )).first()
    reaction.stump = stump
    session.commit()
    session.close()

def create_amongus_user_rank(user_id):
    session = sessionmaker(engine)()
    user_rank = AmongusUserRanks(user_id=user_id, epoch_time=0)
    session.add(user_rank)
    session.commit()
    session.close()

def read_amongus_user_ranks():
    session = sessionmaker(engine)()
    user_ranks = session.query(AmongusUserRanks).all()
    session.close()
    return user_ranks

def update_amongus_user_ranks(user_id, time_count):
    session = sessionmaker(engine)()
    user_rank = session.query(AmongusUserRanks).filter(
        and_(AmongusUserRanks.user_id==user_id
        )).first()
    user_rank.time_counts += time_count
    session.commit()
    session.close()