#!/usr/bin/python
from sqlalchemy import create_engine
import orm

def load(user = "root", engine = None):
    if engine == None:
        engine = create_engine('mysql://{0}@localhost'.format(user))
    orm.Base.metadata.create_all(engine)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: load_db.py <user>"
        exit()
    load(sys.argv[1])
