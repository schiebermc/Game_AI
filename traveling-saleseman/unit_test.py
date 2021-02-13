from solvers import *
from random import randint
from collections import defaultdict

# mostly for testing my graph classes to get the Christofides algo working 

def test_reachableFromHere1():

    # tests a triangle (one component)
    mg = MultiGraph(3)
    mg.addUndirectedEdge(0, 1, 1)
    mg.addUndirectedEdge(0, 2, 1)
    mg.addUndirectedEdge(1, 2, 1)

    val1 = mg.reachableFromHere(0) 
    val2 = mg.reachableFromHere(1) 
    val3 = mg.reachableFromHere(2) 

    assert all([val == 3 for val in [val1, val2, val3]])

    # remove edges, test again
    mg.removeAnEdge(0, 1)
    mg.removeAnEdge(0, 2)

    val1 = mg.reachableFromHere(0) 
    val2 = mg.reachableFromHere(1) 
    val3 = mg.reachableFromHere(2) 
   
    assert val1 == 1 and val2 == 2 and val3 == 2 


def test_reachableFromHere2():

    # tests a line
    n_nodes = 10
    mg = MultiGraph(n_nodes)

    for node1 in range(n_nodes - 1):
        
        # iteratively add edges to form a line
        val1 = mg.reachableFromHere(node1)
        val2 = mg.reachableFromHere(node1+1)
        
        # current node is connected to all prev nodes
        assert val1 == node1 + 1

        # next node is by itself
        assert val2 == 1    
    
        # add the edge
        mg.addUndirectedEdge(node1, node1+1, randint(1, 10))
   
    # scan all nodes again
    for node in range(n_nodes):
        assert mg.reachableFromHere(node) == n_nodes 

    # invert step 1, iteratively remove edges
    for node1 in range(n_nodes - 1):
        
        mg.removeAnEdge(node1, node1+1)
        
        val1 = mg.reachableFromHere(node1)
        val2 = mg.reachableFromHere(node1+1)

        assert val1 == 1
        assert val2 == n_nodes - (node1 + 1)


def test_isBridge1():

    # tests a triangle (no bridges)
    mg = MultiGraph(3)
    mg.addUndirectedEdge(0, 1, 1)
    mg.addUndirectedEdge(0, 2, 1)
    mg.addUndirectedEdge(1, 2, 1)

    val1 = mg.isBridge(0, 1) 
    val2 = mg.isBridge(0, 2) 
    val3 = mg.isBridge(1, 2)

    assert all([not val for val in [val1, val2, val3]])


def test_isBridge2():

    # tests a line (all bridges)
    mg = MultiGraph(3)
    mg.addUndirectedEdge(0, 1, 1)
    mg.addUndirectedEdge(0, 2, 1)

    val1 = mg.isBridge(0, 1) 
    val2 = mg.isBridge(0, 2) 

    assert val1 and val2  


def test_isBridge3():

    # tests a line with duplicate edges (no bridges)
    mg = MultiGraph(3)
    mg.addUndirectedEdge(0, 1, 1)
    mg.addUndirectedEdge(0, 1, 1)
    mg.addUndirectedEdge(0, 2, 1)
    mg.addUndirectedEdge(0, 2, 1)

    val1 = mg.isBridge(0, 1) 
    val2 = mg.isBridge(0, 2) 

    assert not val1 and not val2  

    # now, remove one of the edges, and test again
    mg.removeAnEdge(0, 1)

    val1 = mg.isBridge(0, 1) 
    val2 = mg.isBridge(0, 2) 
    
    assert val1 and not val2


def test_isBridge4():

    # tests a line with a ton of duplicates. iteratively removes and tests
    n_nodes = 10
    
    mg = MultiGraph(n_nodes)
    
    # also a line, but incrementally add more edges by:
    # number of edges = node1_index + node2_index
    for node1 in range(n_nodes - 1):
        for edges in range(node1 + 1):
            mg.addUndirectedEdge(node1, node1 + 1, randint(1, 10))

    # keep track of how many edges we deleted
    d = {i : defaultdict(int) for i in range(n_nodes - 1)}

    # scan a square matrix of removals (although our edges form a triangle)        
    for removals in range(n_nodes):
        for node1 in range(n_nodes - 1):
            if d[node1][node1+1] >= node1:
                # if we deleted all but the last edge, this is a bridge
                assert mg.isBridge(node1, node1+1)
            else:
                # otherwise, it is not a bridge
                assert not mg.isBridge(node1, node1+1)

                # and delete one of the edges until it is
                d[node1][node1+1] += 1
                mg.removeAnEdge(node1, node1+1)




