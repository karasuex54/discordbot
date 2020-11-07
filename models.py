from time import time

import psycopg2
from sqlalchemy import (Column, DateTime, Integer, String, and_, create_engine,
                        or_)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import mytoken as mt

DATABASE_URL = mt.database_url()

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Notices(Base):
    __tablename__ = 'notices'

    id = Column(Integer, primary_key=True)
    guild_id = Column(String)
    channel_id = Column(String)
    epoch_time = Column(Integer, nullable=False)

class Plans(Base):
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    channel_id = Column(String)
    message_id = Column(String)
    epoch_time = Column(Integer, nullable=False)


class Reactions(Base):
    __tablename__ = 'reactions'

    id = Column(Integer, primary_key=True)
    stump = Column(String)
    user_id = Column(String)
    channel_id = Column(String)
    message_id = Column(String)
    epoch_time = Column(Integer, nullable=False)


class TimeCounts(Base):
    __tablename__ = 'timecounts'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    time_counts = Column(Integer, server_default = "0")
    epoch_time = Column(Integer, nullable=False)



Base.metadata.create_all(engine)

# CRUD
# - Create
# - Read
# - Update
# - Destory

def create_notice(guild_id, channel_id):
    session = sessionmaker(engine)()
    notice = Notices(guild_id=guild_id, channel_id=channel_id, epoch_time=int(time()))
    session.add(notice)
    session.commit()
    session.close()

def read_notices():
    session = sessionmaker(engine)()
    notices = session.query(Notices).all()
    session.close()
    return notices

def update_notice(guild_id, channel_id):
    session = sessionmaker(engine)()
    notice = session.query(Notices).filter(Notices.guild_id==guild_id).first()
    notice.channel_id = channel_id
    session.commit()
    session.close()

def create_plan(user_id, channel_id, message_id):
    session = sessionmaker(engine)()
    plan = Plans(user_id=user_id, channel_id=channel_id, message_id=message_id, epoch_time=int(time()))
    session.add(plan)
    session.commit()
    session.close()

def read_plans():
    session = sessionmaker(engine)()
    plans = session.query(Plans).all()
    session.close()
    return plans

def create_reaction(stump, user_id, channel_id, message_id):
    session = sessionmaker(engine)()
    reaction = Reactions(stump=stump, user_id=user_id, channel_id=channel_id, message_id=message_id, epoch_time=int(time()))
    session.add(reaction)
    session.commit()
    session.close()

def read_reactions():
    session = sessionmaker(engine)()
    reactions = session.query(Reactions).all()
    session.close()
    return reactions

def update_reaction(stump, user_id, channel_id, message_id):
    session = sessionmaker(engine)()
    reaction = session.query(Reactions).filter(
        and_(Reactions.user_id==user_id, Reactions.channel_id==channel_id, Reactions.message_id==message_id
        )).first()
    reaction.stump = stump
    session.commit()
    session.close()

def create_timecounts(user_id):
    session = sessionmaker(engine)()
    timecounts = TimeCounts(user_id=user_id, epoch_time=int(time()))
    session.add(timecounts)
    session.commit()
    session.close()

def read_timecounts():
    session = sessionmaker(engine)()
    timecounts = session.query(TimeCounts).all()
    session.close()
    return timecounts

def update_timecounts(user_id, time_count):
    session = sessionmaker(engine)()
    timecounts = session.query(TimeCounts).filter(
        and_(TimeCounts.user_id==user_id
        )).first()
    timecounts.time_counts += time_count
    session.commit()
    session.close()
