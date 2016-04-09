from config import config
import telepot, time, argparse, re, random, schedule

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import TEXT

Base = declarative_base()

class Subscriber(Base):
    __tablename__ = 'subscribers'
    id = Column(Integer, primary_key=True)
    tUserId = Column(Integer)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    msg = Column(TEXT)

def addMessage(msg):
    new_msg = Message(msg=msg)
    session.add(new_msg)
    session.commit()

def handle_message(msg):
    addMsg_check = re.compile('/addMsg\ (.*)',re.MULTILINE|re.DOTALL)
    if msg['text'] == '/subscribe':
        print "subscribing user " + msg['chat']['first_name'] + "with id" + str(msg['chat']['id'])
        new_subscriber = Subscriber(tUserId=msg['chat']['id'])
        session.add(new_subscriber)
        session.commit()
    elif re.match(addMsg_check,str(msg['text'])):
        result = re.search(addMsg_check,str(msg['text']))
        addMessage(result.group(1))

def sendMessageToAll(msg):
    subscribers = session.query(Subscriber).all()
    for subscriber in subscribers:
        print subscriber.tUserId
        bot.sendMessage(subscriber.tUserId, msg)

def getRandMsg():
    query = session.query(Message)
    rowCount = int(query.count())
    randomRow = query.offset(int(rowCount*random.random())).first()
    return randomRow.msg

def job():
    sendMessageToAll(getRandMsg())

engine = create_engine(config['db']['type']+"://"+config['db']['user']+":"+config['db']['password']+"@"+config['db']['host']+"/"+config['db']['name'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.metadata.create_all(engine)
bot = telepot.Bot(config['telegram']['token'])
print bot.getMe()
bot.notifyOnMessage(handle_message)
schedule.every().day.at("00:21").do(job)
while 1:
    schedule.run_pending()
    time.sleep(1)
