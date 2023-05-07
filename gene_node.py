
class NodeGeneType:
    HIDDEN = 1
    INPUT = 2
    OUTPUT = 3

class NodeGene(object):

    def __init__(self,id:int, type:NodeGeneType):
        self.id = id
        self.type = type
    
    def getId(self):
        return self.id
    
    def getNodeType(self):
        return self.type