import bada
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

print pickle.load(open(args.file,"rb"))
