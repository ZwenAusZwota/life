from gene_node import NodeGene, NodeGeneType
from gene_connection import ConnectionGene
import random
from helper import SimConstants
import jsonpickle

class Genome(object):

    def __init__(self, inputNodes:int, outputNodes:int): #Makes a basic genome with only input and output nodes
        self.connectionKeys = []
        self.nodeList = []
        self.connectionList = {}
        self.innovation = 0
        for i in range(0, inputNodes):
            self.nodeList.append(NodeGene(i, NodeGeneType.INPUT))
        for i in range(inputNodes , inputNodes + outputNodes):
            self.nodeList.append(NodeGene(i, NodeGeneType.OUTPUT))
            for j in range(0, inputNodes):
                weight = (float)((random.random() * 2) - 1)
                self.connectionList[self.innovation] = ConnectionGene(j, i, weight, True, self.innovation)
                self.connectionKeys.append(self.innovation)
                self.innovation += 1

    def getNodes(self):
        return self.nodeList
    
    def getConnections(self):
        return self.connectionList
    
    def Distance(self, g2):
        g1 = self
        highestInnovationGene1 = 0
        c1 = g1.getConnections()
        i1 = len(c1)
        if i1 > 0:
            highestInnovationGene1 = c1[i1 - 1]
        highestInnovationGene2 = 0
        c2 = g2.getConnections()
        i2 = len(c2)
        if 21 > 0:
            highestInnovationGene2 = c2[i2 - 1]
        if highestInnovationGene1 < highestInnovationGene2:
            g = g1
            g1 = g2
            g2 = g

        indexG1 = 0
        indexG2 = 0

        disjoint = 0
        excess = 0
        weightDiff = 0
        similar = 0

        while indexG1 < len(g1.getConnections()) and indexG2 < len(g2.getConnections()):
            gene1 = g1.getConnections(indexG1)
            gene2 = g2.getConnections(indexG2)

            innov1 = gene1.innovationNumber
            innov2 = gene2.innovationNumber

            if innov1 == innov2:
                similar += 1
                if gene1.weigth > gene2.weight:
                    weightDiff += gene1.weight - gene2.weigth
                if gene2.weigth > gene1.weight:
                    weightDiff += gene2.weight - gene2.weigth
            
            indexG1 += 1
            indexG2 += 1

            if innov1 > innov2:
                disjoint += 1
                innov2 += 1

            if innov2 > innov1:
                disjoint += 1
                innov1 += 1

            weightDiff /= similar
            excess = len(g1.getConnections()) - indexG1

            n = max(len(g1.getConnections()),len(g2.getConnections()))
            if n < 20:
                n = 1
            
            return (self.neat.C1 * disjoint/n) + (self.neat.C2 * excess / n) + self.neat.C3 * weightDiff
        
    def addConnection(self, con: ConnectionGene): #Connection hinzufügen
        self.connections.append(con) # geht das sO?
        

    def addNode(self,node: NodeGene): #Node zum Genom hinzufügen
        self.nodes.append(node)
        
    def mutate(self, randomChance:float):
        for con in self.connectionList.values():
            if random.random() < randomChance:
                con.randomWeight()
            else:
                con.pertubWeight()
    
    def addNodeMutation(self): #Node zwischen zwei anderen Nodes einfügen
        #irgend eine Verbindung wählen
        rindex = random.randint(0,len(self.connectionList)-1)
        try:
            conn = self.connectionList[rindex]
        except KeyError:
            return
        node1 = conn.inNodeId
        node2 = conn.outNodeId
        conn.disable()
        newNode = NodeGene(len(self.nodeList)+1,NodeGeneType.HIDDEN)
        self.nodeList.append(newNode)

        #dann werden hier 2 Innovationen gemacht
        # diese werden den connectionKeys zugewiesen
        ino1 = len(self.connectionList)+1

        self.connectionList[ino1] = ConnectionGene(node1,newNode.id,conn.weight,True, ino1)
        self.connectionKeys.append(ino1)
        ino2 = len(self.connectionList)+1
        self.connectionList[ino2] = ConnectionGene(newNode.id,node2,conn.weight,True,ino2)
        self.connectionKeys.append(ino2)

    def addConnectionMutation(self): #eine neue Verbindung zwischen zwei beliebigen Knoten einfügen
        #2 zufällige Knoten wählen
        node1 = self.nodeList[random.randint(0,len(self.nodeList)-1)]
        node2 = self.nodeList[random.randint(0,len(self.nodeList)-1)]

        if node1.type == node2.type and node1.type != NodeGeneType.HIDDEN: #unzulässige Verbindung, neu versuchen
            self.addConnectionMutation()
            return
        
        #prüfen, ob verbindung existiert
        for con in self.connectionList.values():
            if con.inNodeId == node1.id and con.outNodeId == node2.id or con.inNodeId == node2.id and con.outNodeId == node1.id:
                return
            
        #Knoten austauschen, falls sie verkehrt herum sind
        if node1.type == NodeGeneType.OUTPUT or node1.type == NodeGeneType.HIDDEN  and node2.type == NodeGeneType.INPUT:
            n = node1
            node1 = node2
            node2 = n

        ino = len(self.connectionList)+1
        self.connectionList[ino] = ConnectionGene(node1.id,node2.id,random.random(),True,ino)
        self.connectionKeys.append(ino)

    def toJSON(self):
        return jsonpickle.encode(self)


