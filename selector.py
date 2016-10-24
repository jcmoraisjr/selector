#!/usr/bin/env python2
from argparse import ArgumentParser
from lib.clusters import Clusters
from lib.locks import Locks
from lib.server import Server

parser = ArgumentParser()
parser.add_argument("--clusters-file", default="")
parser.add_argument("--clusters-inline", default="")
parser.add_argument("--locks", default="locks.json")
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()

clusters = Clusters(args.clusters_file, args.clusters_inline)
locks = Locks(args.locks)
server = Server(clusters, locks)

print "Listening :{0}".format(args.port)
server.listen(args.port)
