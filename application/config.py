import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DIRECTORY = os.path.abspath(os.path.dirname(__file__))
GAMES_DIR = os.path.join(DIRECTORY, 'games')
USER_DIR = os.path.join(DIRECTORY, 'users')
for directory in [GAMES_DIR, USER_DIR]:
    if not os.path.exists(directory):
        os.path.mkdir(directory)
if not os.path.isfile(os.path.join(DIRECTORY, 'usertable.json')):
    with open(os.path.join(DIRECTORY, 'usertable.json'), 'w') as f:
        f.write('{}')


engine = create_engine('sqlite:///test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import User, Game
    Base.metadata.create_all(bind=engine)

if not os.path.isfile(os.path.join(DIRECTORY, 'test.db')):
    init_db()


# The secret key is needed for Flask to 
# enable the sessions environment. It is 
# recommended that you generate a new one
# by opening a python interpreter, then:
# >>>import os
# >>>os.urandom(24)
# 'Lcc\\\xef$\xc8vG\x12\xcc\x11\xbfKE5\x03\x98\xdc\xbc\xcc.JQ'
SECRET_KEY = '\x13\xf4\x95\xb3\x86p\xbf\x1b\xb6B\xc2b\xf4\x96\xf5\xa78;\x8a+\xf2\xdat\xc2'

def hashulate(password):
    """You can modify this function to change how passwords are saved."""
    return password+' hashulate is undefined'
