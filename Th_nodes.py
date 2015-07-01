#Madison Soden
#6/19/15
from tkFont import names
from CodeWarrior.Standard_Suite import lines
import networkx as nx
import math

def oppositenodes(C,cnode1,cnode2):
    oppnodes=False;
    cyc1=nx.get_edge_attributes(C, "cycles")[cnode1]
    cyc2=nx.get_edge_attributes(C, "cycles")[cnode2]
    
    return oppnodes;

# "TH_node_names" is written NodNumber \t NodName \n
f=open("TH_node_names", "r")
name=f.read()
fadf=open("TH_adjacency list", "r")
#num_lines = sum(1 for line in open('TH_node_names'))
adjlist=[]
fad=fadf.read().split("\n")
fadf.close()
for line in fad:
    adjlist.append(line.split("\t"))
#print num_lines

#add a loop function in here when you're less bored

f.close()


names=name.split('\n')
lines=[]
for line in names:
    lines.append(line.split("\t"))    
'''    
lines0 = names[0].split('\t')
lines1 = names[1].split('\t')
lines2 = names[2].split('\t')
lines3 = names[3].split('\t')
lines4 = names[4].split('\t')
lines5 = names[5].split('\t')
lines6 = names[6].split('\t')
lines7 = names[7].split('\t')
lines8 = names[8].split('\t')
lines9 = names[9].split('\t')
lines10 = names[10].split('\t')
lines11 = names[11].split('\t')
lines12 = names[12].split('\t')
lines13 = names[13].split('\t')
lines14 = names[14].split('\t')
lines15 = names[15].split('\t')
lines16 = names[16].split('\t')
lines17 = names[17].split('\t')
lines18 = names[18].split('\t')
lines19 = names[19].split('\t')
lines20 = names[20].split('\t')
lines21 = names[21].split('\t')
lines22 = names[22].split('\t')
lines23 = names[23].split('\t')
lines24 = names[24].split('\t')
lines25 = names[25].split('\t')
lines26 = names[26].split('\t')
lines27 = names[27].split('\t')
lines28 = names[28].split('\t')
lines29 = names[29].split('\t')
lines30 = names[30].split('\t')
lines31 = names[31].split('\t')
lines32 = names[32].split('\t')
lines33 = names[33].split('\t')
lines34 = names[34].split('\t')
lines35 = names[35].split('\t')
lines36 = names[36].split('\t')
lines37 = names[37].split('\t')
lines38 = names[38].split('\t')
lines39 = names[39].split('\t')
lines40 = names[40].split('\t')
lines41 = names[41].split('\t')
lines42 = names[42].split('\t')
lines43 = names[43].split('\t')
lines44 = names[44].split('\t')
lines45 = names[45].split('\t')
lines46 = names[46].split('\t')
lines47 = names[47].split('\t')
lines48 = names[48].split('\t')
lines49 = names[49].split('\t')
lines50 = names[50].split('\t')
lines51 = names[51].split('\t')
lines52 = names[52].split('\t')
lines53 = names[53].split('\t')
lines54 = names[54].split('\t')
lines55 = names[55].split('\t')
lines56 = names[56].split('\t')
lines57 = names[57].split('\t')
lines58 = names[58].split('\t')
lines59 = names[59].split('\t')
lines60 = names[60].split('\t')
lines61 = names[61].split('\t')
lines62 = names[62].split('\t')
lines63 = names[63].split('\t')
lines64 = names[64].split('\t')
lines65 = names[65].split('\t')
lines66 = names[66].split('\t')
lines67 = names[67].split('\t')
lines68 = names[68].split('\t')
lines69 = names[69].split('\t')
'''

G=nx.DiGraph()
#for c in range(num_lines) : 
#    G.add_node(names[c].split('\t')[0], nodname = names[c].split('\t')[1])

for line in lines:
    G.add_node(line[0],nodname=line[1])

for line in adjlist:
    for i in range(len(line)-1):
        G.add_edge(line[0], line[i+1])
        
#for g in G.nodes():
    #print g, nx.get_node_attributes(G, 'nodname')[g]

for g in G.nodes():
    if(float(g)!=math.floor(float(g))):
        innod=G.in_edges(g)
        
nx.write_gml(G, "th_nodeNetwork.gml")

fcy=open("ThNetwork_cycles", "r")
cycles=fcy.read()
fcy.close()

lines=[]
for line in cycles.split('\n'):
    lines.append(line.split("\t"))

C=nx.Graph()

for line in lines:
    node=line[0]
    cycle=line
    cycle.remove(node)
    C.add_node(node, cycles = line)

dic={}

for c in C.nodes():
    #print c, nx.get_node_attributes(C, 'cycles')[c]
    for expnode in nx.get_node_attributes(C, 'cycles')[c]:
        if(float(expnode)!=int(float(expnode))):
            dic[expnode]=[]

for c in C.nodes():
    #print c, nx.get_node_attributes(C, 'cycles')[c]
    for expnode in nx.get_node_attributes(C, 'cycles')[c]:
        if(float(expnode)!=int(float(expnode))):
            current=dic[expnode]
            current.append(c)
            dic[expnode]=current

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

edgesremove=[]
for e in C.edges():
    if():
        edgesremove.append(e)
C.remove_edges_from(edgesremove)