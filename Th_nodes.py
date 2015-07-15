#Madison Soden
#6/19/15 created
#Notation Updates and oppositenodes function added 7/07/15
#7/13/15  corrections w/ Jorge
#7/14/15 added inputCNodes function, deleted the semicolons I keep putting every where for continuitys sake, and added opposite coposit node removal for cycle network

# Optional print data checks are commented using '''
# Explantiroy comments are comented with #

# On Notation:
# Node IDs are recorded as strings of numbers: 
# - normal nodes are integers with their negations being represented as the negative of the Node ID
#                                 i.e. nodes V and ~V could be represented as 1 and -1 respectivly
# - composit node IDs are represented as decimal #s that do not corrispond to the Node IDs of their parent Nodes
#                  i.e. node A's ID could be 1 and nodee B's ID could be 2 with composit node AB's ID being 12.5
# - composite node IDs  are only ever positive decimal #s

import networkx as nx
import math

# in progress function to identifie opposit nodes in cycle networks
def oppositenodes(C,cnode1,cnode2):
    oppnodes=False;
    cyc1=nx.get_node_attributes(C, "cycles")[cnode1]
    cyc2=nx.get_node_attributes(C, "cycles")[cnode2]
    for n in cyc1:
        #if int(n) == float(n): ?
        for m in cyc2:
             #if int(m) == float(m): ?  do I have to check for compossite nodes
            if float(n) == (-1*float(m)):
                oppnodes=True
                break
        if oppnodes: break
    return oppnodes


#finds inputs of a composit nodes, inode is a list of incoming edges
def inputCNodes(C,g):
   # for g in G.nodes():
        if(float(g)!=math.floor(float(g))):
            innod=C.in_edges(g)
            return innod



def opositeCnodes(C,cnode1, cnode2):
    oppnodes=False;
    cyc1=nx.get_node_attributes(C, "cycles")[cnode1]
    cyc2=nx.get_node_attributes(C, "cycles")[cnode2]
    for n in cyc1:
        if(float(n)!=math.floor(float(n))):
            for m in cyc2:
                if(float(m)!=math.floor(float(m))):
                    inputn = inputCNodes(C,n)
                    inputm = inputCNodes(C,m)
                    #I'm sorry about this but it's late, I'll fix it 
                    if ( (float(inputn[0]) == (-1*float(inputm[0]))) or (float(inputn[1]) == (-1*float(inputm[0]))) or (float(inputn[1]) == (-1*float(inputm[1]))) or (float(inputn[0]) == (-1*float(inputm[0]))) ):
                        oppnodes=True
                        break
            if oppnodes: break
        return oppnodes
    
# "TH_node_names" is written NodNumber(i.e identifier) \t NodName(i.e. the actual protien or whatever) \n
# reading in "TH_node_names as a string name
f = open("TH_node_names", "r")
name=f.read()
f.close()

#creating a nodname list of the form names[NodNumber][protien name or whatever]
names=name.split('\n')
lines=[]
for line in names:
    lines.append(line.split("\t"))  
    
    
#"TH_adjacency list is written NodeNumber \t downstream NodNumbers (spererated by \t) \n
#creating a adjacency list adjlist[NodNumber][Downstreaam NodeNumbers]
fadf=open("TH_adjacency list", "r")
adjlist=[]
fad=fadf.read().split("\n")
fadf.close()
for line in fad:
    adjlist.append(line.split("\t"))
  
    
# creating a directed network G as the network of Nodes
G=nx.DiGraph()
'''for c in range(num_lines) : 
     G.add_node(names[c].split('\t')[0], nodname = names[c].split('\t')[1])'''
#creating Nodes in node network with string(node ID attribute) 
# and string(nodename atribute) 
for line in lines:
    G.add_node(line[0],nodname=line[1])

#for all node IDs in adjacencey list
for line in adjlist:
    # add each downstream connection to adjacent Node IDs
    for i in range(len(line)-1):
        G.add_edge(line[0], line[i+1])
        
'''for g in G.nodes():
    #print g, nx.get_node_attributes(G, 'nodname')[g]'''
        
nx.write_gml(G, "th_nodeNetwork.gml")


#end node network creation 
#start Cycle network creation


#Opens Cycle Network file, creats a list lines of line, line is in turn a list of strings 
# from the Cycle Network file where [0] is the cycle node name and [1:] are the unordered nodes contained w/i that cycle
fcy=open("ThNetwork_cycles", "r")
cycles=fcy.read()
fcy.close()

lines=[]
for line in cycles.split('\n'):
    lines.append(line.split("\t"))

# creates undirected cycle network
C=nx.Graph()

# declares a cycle node for each line in lines, delets the cycle node data from each line and then renames each line cycles 
# bc that is the data they still contain
for line in lines:
    node=line[0]
    cycle=line
    cycle.remove(node)
    #ands a cycle node with the attribute of having its list of network nodes
    C.add_node(node, cycles = line)

dic={}
#creates a dictionary for each expanded node in  each cycle node
for c in C.nodes():
    '''print c, nx.get_node_attributes(C, 'cycles')[c]'''
    for expnode in nx.get_node_attributes(C, 'cycles')[c]:
        if(float(expnode)!=int(float(expnode))):
            dic[expnode]=[]

# assigns a cycle node for each expanded node
for c in C.nodes():
    '''print c, nx.get_node_attributes(C, 'cycles')[c]'''
    for expnode in nx.get_node_attributes(C, 'cycles')[c]:
        if(float(expnode)!=int(float(expnode))):
            current=dic[expnode]
            current.append(c)
            dic[expnode]=current

#doing complicated stuff to print expanded node, it's inputs and then a list of cycles containg those inputs 
'''
for key in  dic.keys():
    cycnodes=dic[key]
    inputs=G.in_edges(key)
    print "INPUT",key,inputs
    for cnode1 in  range(len(cycnodes)):    
        cyc1=nx.get_node_attributes(C, 'cycles')[cycnodes[cnode1]]    
        for cnode2 in  range(len(cycnodes)):
            if(cnode2>cnode1):            
                cyc2=nx.get_node_attributes(C, 'cycles')[cycnodes[cnode2]]   
                print "cyc1",cycnodes[cnode1],cyc1
                print "cyc2",cycnodes[cnode2],cyc2            
                inters1=[]
                inters2=[]
                trueboth=True               
                for input in inputs:
                    true1=cyc1.__contains__(input[0])
                    true2=cyc2.__contains__(input[0])
                    if(true1): inters1.append(input[0])
                    if(true2): inters2.append(input[0])
                    trueboth=((true1 and true2) or (not true1 and not true2)) and trueboth
                if(len(inters1)!=len(inters2)): C.add_edge(cycnodes[cnode1], cycnodes[cnode2]); print "NODE",cycnodes[cnode2],cycnodes[cnode1]             
                elif(len(inters1)==len(inters2) and trueboth): C.add_edge(cycnodes[cnode1], cycnodes[cnode2]); print "NODE",cycnodes[cnode2],cycnodes[cnode1]
'''
#removing edges that connect cycles with opposite nodes            
edgesremove=[]
for e in C.edges():
    cnode1=e[0]
    cnode1=e[1]
    if oppositenodes(C,cnode1,cnode2):
        edgesremove.append(e)
C.remove_edges_from(edgesremove)

#removing edges that connect cycles with opposite composit nodes
edgesremove1=[]
for e in C.edges():
    cnode1=e[0]
    cnode2=e[1]
    if opositeCnodes(C,cnode1, cnode2):
        edgesremove1.append(e)
C.remove_edges_from(edgesremove1)

nx.write_gml(C, "th_cycleNetwork.gml")
    
 