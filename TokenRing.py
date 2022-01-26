import random
import time
import multiprocessing

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Node:
    def __init__(self, number, nextNode=None):
        self.number = number
        self.hasToken = False
        self.nextNode = nextNode
        self.access = 1
        self.ringOpen = 0
        self.tokenArrived = 0

    def setNeighbour(self, inactive):
        """
        set the neighbours of the nodes
        """
        # when the process is the last, it neighbour will be the first to close the ring
        if len(inactive)-1 == self.number:
            self.nextNode = 0
        else:
            self.nextNode = (self.number + 1)

        print("Process " +  str(self.number) + " has the neighbour ", self.nextNode)
        

    def simulateCrash(self, inactive):
        """
        simulate the chance to kill a process
        """
        # exclude, that more then one process gets killed
        if sum(inactive) < 1:
            if random.randint(0, 65) < 1:
                inactive[self.number] = 1
                print("Process", self.number, f" {bcolors.WARNING}was killed{bcolors.ENDC}")
                return True

    def closeRing(self, inactive, token):
        """
        close the ring after a process died
        """
        # if only one process is left, quit
        if sum(inactive) == len(inactive) - 1:
            return False

        # check if the following nod is dead
        if inactive[self.nextNode] == 1:
            # idx starts at the position of the node.number
            for idx,nodes in enumerate(inactive, self.number):
                # if process is at last position, go to the start of the array
                if idx == len(inactive)-1:
                    print("idx at last position, change idx to first position")
                    idx = 0
                    # if the start is active
                    if inactive[idx] == 0:
                        # set it as new neighbour
                        self.nextNode = 0
                        print("Process ", self.number, f" {bcolors.OKGREEN}has closed the ring and points now to {bcolors.ENDC}", self.nextNode)
                        token.value = self.nextNode
                        self.ringOpen = 0
                        drawRing(token, inactive)
                        return True


                # if active node was found, set it as new neighbour
                if inactive[idx+1] == 0:
                    if self.nextNode != (idx+1):
                        self.nextNode = (idx+1)
                        print("Process ", self.number, f" {bcolors.OKGREEN}has closed the ring and points now to {bcolors.ENDC}", self.nextNode)
                        token.value = self.nextNode
                    self.ringOpen = 0
                    drawRing(token, inactive)
                    return True
        
        self.ringOpen = 0


    def activity(self, token, inactive):
        """
        use the ressource if the token is available
        """

        self.setNeighbour(inactive)

        while True:
            time.sleep(1.5)

            # check if process is still active. idx of process is its number - 1 
            if inactive[self.number] == 1:
                # simulate the dead process 
                break

            self.hasToken = False

            if token.value == self.number:
                self.hasToken = True
                self.tokenArrived = time.clock()

            if self.hasToken == True:
                print("Process " +  str(self.number) + " has the token and can use the ressource")

                f = open("log.txt", "a")
                f.write("Ich bin Prozess_" + str(self.number) + " und habe " + str(self.access) + " mal auf die Ressource zugegriffen\n")
                f.close()

                self.access += 1

                # give the token to the next process
                if random.randint(0, 9) > 4:
                    self.hasToken == False
                    token.value = self.nextNode 
                    print("Process", self.number, f"{bcolors.OKCYAN}has changed the token to: {bcolors.ENDC}", token.value, "\n\n")

            # simulate a dead process
            if self.simulateCrash(inactive) == True:
                break
            

            # check if token disapeard, triggers if token stays away for 10 seconds. Warning: large rings need more time
            if (self.tokenArrived + 10) < time.clock():
                self.ringOpen = 1

            # check if the ring is open
            if self.ringOpen == 1:
                # close it if possible
                if self.closeRing(inactive, token) == False:
                    print("No more Nodes left: Process ", self.number, " leaves the ring")
                    break
        
def drawRing(token, inactive):

    draw = ""

    for idx,process in enumerate(inactive):
        if process == 0:
            draw += str(idx) + " -> "

    # close the ring, so the last element points to the first 
    for idx,process in enumerate(inactive):
        if process == 0:
            draw += str(idx)
            break

    print(f"{bcolors.HEADER}Ring: {bcolors.ENDC}", draw)


f = open("log.txt", "w")
f.write("### Log-Datei fuer den Token-Ring-Algorithmus ### \n\n")
f.close()

if __name__ == "__main__":

    n = []
    for element in range(5):
        node = Node(element)
        n.append(node)

    # creating Value of int data type
    token = multiprocessing.Value('i', 1)

    # creating Array of int data type with space for len of nodes integers to simulate inactive processes
    inactive = multiprocessing.Array('i', len(n))
    print("len of nodes:", len(inactive))

    # initialise the array with 0. each process has its own idx, if the value is 1, the process will be shut down
    for idx in range(len(n)):
        inactive[idx] = 0

    processes = []
    for node in n:
        p = multiprocessing.Process(target=node.activity, args=(token, inactive))
        processes.append(p)

    for pr in processes:
        pr.start()
    
    # show the full ring
    drawRing(token, inactive)

    for pr in processes:
        pr.join()