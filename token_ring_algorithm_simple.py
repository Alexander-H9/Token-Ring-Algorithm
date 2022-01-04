import random
import time

class Node:
    def __init__(self, number, nextNode=None):
        self.number = number
        self.hasToken = False
        self.nextNode = nextNode
        self.importance = 0
    
    def activity(self):
        if self.hasToken == True:
            print("Node " +  str(self.number) + " has the token and can use the resource")
            self.importance -= random.randint(0, 8)
        else:
            self.importance += random.randint(1, 10)

    def calcImportance(self, nodeList):

        importance = 0
        for node in nodeList:
            importance += node.importance
        importance = importance / len(nodeList)

        if self. importance < importance:
            self.hasToken = False
            self.nextNode.hasToken = True
           
n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)
n5 = Node(5)

n1.nextNode = n2
n2.nextNode = n3
n3.nextNode = n4
n4.nextNode = n5
n5.nextNode = n1

n1.hasToken = True

nodeList = [n1, n2, n3, n4, n5]

while True:
    for node in nodeList:
        node.activity()
        if node.hasToken == True:
            node.calcImportance(nodeList)
    time.sleep(2)