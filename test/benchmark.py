<<<<<<< HEAD
""" Usage: python benchmark.py ["database backend list" | backend1] [backend2]

Import the backend (anydbm, sqlite by default) and run some performance
tests. Example:

test default anypy and sqlite backends

  python benchmark.py

test mysql and sqlite backends

  python benchmark.py mysql sqlite

or

  python benchmark.py "mysql sqlite"

test all backends

  python benchmark.py anydbm mysql postgresql sqlite


"""
from __future__ import print_function
import sys, os, time
import importlib, signal, shutil

# --- patch sys.path to make sure 'import roundup' finds correct version
import os.path as osp
thisdir = osp.dirname(osp.abspath(__file__))
rootdir = osp.dirname(thisdir)
if (osp.exists(thisdir + '/benchmark.py') and
        osp.exists(rootdir + '/roundup/__init__.py')):
    # the script is located inside roundup source code
    sys.path.insert(0, rootdir)
=======
from __future__ import print_function
import sys, os, time
>>>>>>> main

from roundup.hyperdb import String, Password, Link, Multilink, Date, \
    Interval, DatabaseError, Boolean, Number
from roundup import date, password

<<<<<<< HEAD
from test.db_test_base import config

# global for the default signal hander so
# my signal handler can reset before it raises signal.
int_sig_default_handler = None
=======
from .db_test_base import config
>>>>>>> main

def setupSchema(db, module):
    status = module.Class(db, "status", name=String())
    status.setkey("name")
    user = module.Class(db, "user", username=String(), password=Password(),
        assignable=Boolean(), age=Number(), roles=String())
    user.setkey("username")
    file = module.FileClass(db, "file", name=String(), type=String(),
        comment=String(indexme="yes"))
    issue = module.IssueClass(db, "issue", title=String(indexme="yes"),
        status=Link("status"), nosy=Multilink("user"), deadline=Date(),
        foo=Interval(), files=Multilink("file"), assignedto=Link('user'))
    session = module.Class(db, 'session', title=String())
    session.disableJournalling()
    db.post_init()
    db.commit()

<<<<<<< HEAD
def rm_db_on_signal(sig, frame):
    print("removing incomplete database %s due to interruption." %
          config.DATABASE)

    shutil.rmtree(config.DATABASE)

    signal.signal(signal.SIGINT, int_sig_default_handler)
    # re-raise the signal so the normal signal handling runs.
    signal.raise_signal(signal.SIGTERM)

def main(backendname, time=time.time, numissues=10):
    global int_sig_default_handler

    try:
        backend = importlib.import_module("roundup.backends.back_%s" %
                                          backendname)
    except ImportError:
        print("Unable to import %s backend." % backendname)
=======
def main(backendname, time=time.time, numissues=10):
    try:
        exec('from roundup.backends import %s as backend'%backendname)
    except ImportError:
>>>>>>> main
        return

    times = []

    config.DATABASE = os.path.join('_benchmark', '%s-%s'%(backendname,
        numissues))
<<<<<<< HEAD

    config.RDBMS_NAME = "rounduptest_%s" % numissues

    if not os.path.exists(config.DATABASE):
        int_sig_default_handler = signal.signal(signal.SIGINT, rm_db_on_signal)
        db = backend.Database(config, 'admin')
        setupSchema(db, backend)

        # if we are re-initializing, delete any existing db
        db.clear()
        db.commit()

        # create a whole bunch of stuff
        db.user.create(**{'username': 'admin', 'roles': 'Admin'})
=======
    if not os.path.exists(config.DATABASE):
        db = backend.Database(config, 'admin')
        setupSchema(db, backend)
        # create a whole bunch of stuff
        db.user.create(**{'username': 'admin'})
>>>>>>> main
        db.status.create(name="unread")
        db.status.create(name="in-progress")
        db.status.create(name="testing")
        db.status.create(name="resolved")
        pc = -1
        for i in range(numissues):
<<<<<<< HEAD
            db.user.create(**{'username': 'user %s'%i, 'roles': 'User'})
=======
            db.user.create(**{'username': 'user %s'%i})
>>>>>>> main
            for j in range(10):
                db.user.set(str(i+1), assignable=1)
                db.user.set(str(i+1), assignable=0)
            db.issue.create(**{'title': 'issue %s'%i})
            for j in range(10):
                db.issue.set(str(i+1), status='2', assignedto='2', nosy=[])
                db.issue.set(str(i+1), status='1', assignedto='1',
                    nosy=['1','2'])
<<<<<<< HEAD
            if (i*100//numissues) != pc and 'INCI' not in os.environ:
=======
            if (i*100//numissues) != pc:
>>>>>>> main
                pc = (i*100//numissues)
                sys.stdout.write("%d%%\r"%pc)
                sys.stdout.flush()
            db.commit()
<<<<<<< HEAD
        signal.signal(signal.SIGINT, int_sig_default_handler)
=======
>>>>>>> main
    else:
        db = backend.Database(config, 'admin')
        setupSchema(db, backend)

<<<<<<< HEAD
    sys.stdout.write('%10s: %-6d'%(backendname[:10], numissues))
=======
    sys.stdout.write('%7s: %-6d'%(backendname, numissues))
>>>>>>> main
    sys.stdout.flush()

    times.append(('start', time()))

    # fetch
    db.clearCache()
    for i in db.issue.list():
        db.issue.get(i, 'title')
    times.append(('fetch', time()))

    # journals
    db.clearCache()
    for i in db.issue.list():
        db.issue.history(i)
    times.append(('journal', time()))

    # "calculated" props
    db.clearCache()
    for i in db.issue.list():
        db.issue.get(i, 'activity')
        db.issue.get(i, 'creator')
        db.issue.get(i, 'creation')
    times.append(('jprops', time()))

    # lookup
    db.clearCache()
    for i in range(numissues):
        db.user.lookup('user %s'%i)
    times.append(('lookup', time()))

    # filter
    db.clearCache()
    for i in range(100):
        db.issue.filter(None, {'assignedto': '1', 'title':'issue'},
            ('+', 'activity'), ('+', 'status'))
    times.append(('filter', time()))

    # filter with multilink
    db.clearCache()
    for i in range(100):
        db.issue.filter(None, {'nosy': ['1'], 'assignedto': '1',
            'title':'issue'}, ('+', 'activity'), ('+', 'status'))
    times.append(('filtml', time()))

    # results
    last = None
    for event, stamp in times:
        if last is None:
            first = stamp
        else:
            sys.stdout.write(' %-6.2f'%(stamp-last))
        last = stamp
    print(' %-6.2f'%(last-first))
    sys.stdout.flush()

if __name__ == '__main__':
<<<<<<< HEAD
    if len(sys.argv) == 2:
        test_databases = sys.argv[1].split()
    elif len(sys.argv) > 2:
        test_databases = sys.argv[1:]
    else:
        test_databases = ['anydbm', 'sqlite']

    #      0         1         2         3         4         5         6
    #      01234567890123456789012345678901234567890123456789012345678901234
    print('Test name         fetch  journl jprops lookup filter filtml TOTAL ')
    for name in test_databases:
        main(name)
    for name in test_databases:
        main(name, numissues=20)
    for name in test_databases:
        main(name, numissues=100)

    # don't even bother benchmarking the dbm backends > 100!
    try:
        test_databases.remove('anydbm')
    except ValueError:
        # anydbm not present; this is fine
        pass

    for name in test_databases:
        main(name, numissues=1000)

    for name in test_databases:
        main(name, numissues=10000)


=======
    #      0         1         2         3         4         5         6
    #      01234567890123456789012345678901234567890123456789012345678901234
    print('Test name       fetch  journl jprops lookup filter filtml TOTAL ')
    for name in 'anydbm metakit sqlite'.split():
        main(name)
    for name in 'anydbm metakit sqlite'.split():
        main(name, numissues=20)
    for name in 'anydbm metakit sqlite'.split():
        main(name, numissues=100)
    # don't even bother benchmarking the dbm backends > 100!
    for name in 'metakit sqlite'.split():
        main(name, numissues=1000)

>>>>>>> main
# vim: set et sts=4 sw=4 :
