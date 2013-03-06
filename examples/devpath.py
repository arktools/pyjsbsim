import  sys, os
curdir = os.path.dirname(os.path.abspath(__file__))
pardir = os.path.abspath(os.path.join(curdir,os.path.pardir))
sys.path.insert(0,curdir)
sys.path.insert(0,pardir)
del curdir, pardir
