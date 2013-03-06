import devpath
from pyjsbsim.bada import BadaData
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

print pickle.load(open(args.file,"rb"))
