from genome import Genome
from gene_node import NodeGene, NodeGeneType
from gene_connection import ConnectionGene
from helper import SimConstants

class Node:

    def __init__(self,id:int):
        self.id = id
        self.value = 0.0
        self.inConnections = []
        self.outConnections = []

    def getId(self):
        return self.id
    
    def isReady(self):
        for con in self.inConnections:
            if con.getStatus() != True:
                return False
        return True

    def addInConnection(self, con):
        self.inConnections.append(con)
    
    def addOutConnection(self, con):
        self.outConnections.append(con)

    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = SimConstants.relu(value)

    def calculateValue(self):
        for con in self.inConnections:
            self.value += con.getValue()
        self.value = SimConstants.relu(self.value)

    def transmitValue(self):
        for con in self.outConnections:
            con.setValue(self.value)
        self.value = 0

class Connection:
    def __init__(self, inId:int, outId:int, weight:float):
        self.inNodeId = inId
        self.outNodeId = outId
        self.value = 0.0
        self.ready = False
        self.weight = weight

    def __init__(self, con:ConnectionGene):
        self.inNodeId = con.inNodeId
        self.outNodeId = con.outNodeId
        self.value = 0
        self.ready = False
        self.weight = con.weight
    
    def getValue(self):
        val = self.value
        ready = False
        self.value = 0
        return val * self.weight
    
    def setValue(self, val):
        self.value = val
        self.ready = True

    def getStatus(self):
        return self.ready
        

class NEAT:
    def __init__(self, genome:Genome):
        self.genome = genome
        self.nodes = {}
        self.nodeGenes = genome.getNodes()
        self.connectionGenes = genome.getConnections()
        self.inputNodes = []
        self.outputNodes= []
        self.hiddenNodes = []
        self.fitness = 0.0
        self.createNetwork()

    def createNetwork(self):
        for ng in self.nodeGenes:
            node = Node(ng.getId())
            if ng.type == NodeGeneType.INPUT:
                self.inputNodes.append(node)
            elif ng.type == NodeGeneType.OUTPUT:
                self.outputNodes.append(node)
            else:
                self.hiddenNodes.append(node)
            self.nodes[ng.getId()] = node

        for cg in self.connectionGenes.values():
            if cg.isExpressed():
                con = Connection(cg)
                self.nodes[con.inNodeId].addOutConnection(con)
                self.nodes[con.outNodeId].addInConnection(con)

    def getOutput(self, input):
        output = []
        for i in range(0,len(input)):
            self.inputNodes[i].setValue(input[i])
            self.inputNodes[i].transmitValue()

        copyList = self.hiddenNodes

        while len(copyList) != 0:
            removeNodes = []
            for node in copyList:
                if node.isReady():
                    node.calculateValue()
                    node.transmitValue()
                    removeNodes.append(node)

            for node in removeNodes:
                copyList.remove(node)

        for on in self.outputNodes:
            on.calculateValue()
            output.append(on.getValue())

        return output

    def fetGenome(self):
        return self.genome

    def getFitness(self):
        return self.fitness

    def setFitness(self, fit:float):
        self.fitness = fit

    def addFitness(self, fit:float):
        self.fitness += fit

    ###altes zeug
    def reset(self,inputSize, outputSize, clients):
        int: self.inputSize = inputSize
        int: self.outputSize = outputSize
        int: self.clients = clients

        float: self.C1
        float: self.C2
        float: self.C3

        self.allConnections = []
        self.allNodes = []
        for i in range(0,self.inputSize):
            n = self.getNode()
            n.X = 0.1
            n.Y = (i + 1.0) / (self.inputSize + 1.0)
        for i in range(0,self.outputSize):
            n = self.getNode()
            n.X = 0.9
            n.Y = (i + 1.0) / (self.outputSize + 1.0)

    def emptyGenome(self):
        g = Genome()
        for i in range(0, self.inputSize + self.outputSize):
            g.getNodes().append(self.getNode(i+1))

    def getNode(self):
        n =  NodeGene(len(self.allNodes)+1)
        self.allNodes.append(n)
        return n

    def getNode(self, id):
        if id <= len(self.allNodes):
            return self.allNodes[id - 1]
        return self.getNode()
    
    def getConnection(self, con: ConnectionGene):
        c = ConnectionGene(con.fromNode, con.toNode)
        c.innovationNumber = con.innovationNumber
        c.weight = con.weight
        c.enablde = con.enabled
        pass

    def getConnection(self, node1: NodeGene, node2: NodeGene):
        c = ConnectionGene(node1, node2)
        if c in self.allConnections:
            c.innovationNumber = self.allConnections.index(c)
            pass
        else:
            c.innovationNumber = len(self.allConnections) + 1
            self.allConnections.append(c)
