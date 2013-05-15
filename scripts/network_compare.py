#!/usr/bin/env python

import sys
import networkx
import argparse
from pathway_tools import convert as network_convert

def log(msg):
    sys.stdout.write(msg + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src-paradigm', help="Source Paradigm File")
    parser.add_argument('--dst-paradigm', help="Dest Paradigm File")
    parser.add_argument('--src-xgmml', help="Source XGMML File")
    parser.add_argument('--dst-xgmml', help="Dest XGMML File")

    args = parser.parse_args()

    gr1 = None
    gr2 = None

    if args.src_paradigm:
        handle1 = open(args.src_paradigm)
        gr1 = network_convert.read_paradigm_graph(handle1, strict=False)
        handle1.close()
    if args.src_xgmml:
        handle1 = open(args.src_xgmml)
        gr1 = network_convert.read_xgmml(handle1)
        handle1.close()

    if args.dst_paradigm:      
        handle2 = open(args.dst_paradigm)
        gr2 = network_convert.read_paradigm_graph(handle2, strict=False)
        handle2.close()
    if args.src_xgmml:
        handle1 = open(args.dst_xgmml)
        gr2 = network_convert.read_xgmml(handle1)
        handle1.close()
    
    if gr1 is None or gr2 is None:
        sys.stderr.write("Select files for source and dst graphs\n")
        sys.exit(1)

    gr = networkx.MultiDiGraph()

    log("Node Counts %d %d" % (len(gr1.nodes()), len(gr2.nodes())))
    log("Edge Counts %d %d" % (len(gr1.edges()), len(gr2.edges())))

    for n in gr1.node:
        if n not in gr2.node:
            log( "Graph2 Missing Node:" + n )
            gr.add_node(n)
            gr.node[n] = gr1.node[n]
    for n in gr1.node:
        for t in gr1.edge[n]:
            for i in gr1.edge[n][t]:
                found = False 
                if n in gr2.node and t in gr2.edge[n]:
                    for j in gr2.edge[n][t]:
                        if gr2.edge[n][t][j] == gr1.edge[n][t][i]:
                            found = True

                if not found:
                    gr.add_edge(n,t, attr_dict=gr1.edge[n][t][i] )
                    log( "Graph2 Missing Edge:" + str((n,t)) + " " + str(gr1.edge[n][t][i]))
    for n in gr2.node:
        if n not in gr1.node:
            log( "Graph1 Missing Node:" + n )
        else:
            for t in gr2.edge[n]:
                if t not in gr1.edge[n]:
                    log( "Graph1 Missing Edge:" + str((n,t)))
    
    #network_convert.write_paradigm_graph(gr, sys.stdout)
    #network_convert.write_xgmml(gr, sys.stdout)
