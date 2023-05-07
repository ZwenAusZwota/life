from gene_node import NodeGene
import random

class ConnectionGene(object):

    def __init__(self, inNodeId:int, outNodeId:int, weight:float, expressed:bool, innovation:int):
        self.inNodeId = inNodeId
        self.outNodeId = outNodeId
        self.weight = weight
        self.expressed = expressed
        self.innovation = innovation

    def disable(self):
        self.expressed = False

    def randomWeight(self):
        self.weight = random.random()*2-1 #0..1

    def pertubWeight(self):
        self.weight += (random.random()-0.5)*0.5

    def isExpressed(self):
        return self.expressed
    
    def getId(self):
        return self.innovation