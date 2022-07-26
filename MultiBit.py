import itertools
import timeit

STRIDE = 3


class MultibitNode(object):
    def __init__(self):
        self.children = {}

    def AddChild(self, prefix, path):

        if path == "":
            return

        if len(path) < STRIDE:  # if the path is shorter than the stride

            # Expand the combinations and insert them all as children
            for combination in GetCombinations(STRIDE - len(path)):
                self.children[path + combination] = (prefix, None)

        elif len(path) == STRIDE: # If it's exactly as long as the stride
            
            # Set the corresponding dictionary entry
            self.children[path] = (prefix, None)

        else:  # if it's longer than the stride
            
            first = path[:STRIDE]  # Take only the first STRIDE characters
            
            # If we don't have this value in the dictionary yet, make a new node with no prefix
            if first not in self.children:
                self.children[first] = ("", MultibitNode())
            # Otherwise keep the existing prefix and just create a child node
            elif self.children[first][1] is None:
                self.children[first] = (self.children[first][0], MultibitNode())

            self.children[first][1].AddChild(prefix, path[STRIDE:])

    def RecursiveLookup(self, address, backtrack=""):
        if len(address) < STRIDE:
            return backtrack

        first = address[:STRIDE]

        # If the child does not exist, return last valid prefix
        if len(address) < STRIDE or first not in self.children:
            return backtrack

        child = self.children[first]

        # We're here when address is at least as long as the stride
        
        # If it's as long as the stride, or there is no pointer to another multibit node
        if len(address) == STRIDE or child[1] is None:
            return child[0]

        else:
            if child[0] == "":
                return child[1].RecursiveLookup(address[STRIDE:], backtrack)
            else:
                return child[1].RecursiveLookup(address[STRIDE:], child[0])

    def NonRecursiveLookup(self, address, rootPrefix=''):
        backtrack = rootPrefix
        partialAddress = address
        node = self

        while node is not None:
            if len(partialAddress) < STRIDE:
                return backtrack

            first = partialAddress[:STRIDE]

            if len(partialAddress) < STRIDE or first not in node.children:
                return backtrack

            child = node.children[first]
            node = node.children[first][1]  # relocating pointer

            if len(partialAddress) == STRIDE or child[1] is None:
                return child[0]
            else:
                partialAddress = partialAddress[STRIDE:]
                if child[0] != "":
                    backtrack = child[0]
                    node = child[1]

def GetCombinations(length):
    # creating the combinations of the remaining bits
    char_set = [0, 1]
    return [''.join(map(str, i)) for i in itertools.product(char_set, repeat=length)]


def BuildTree(default='0'): # create the binary trie using the dbtest.txt and dbmask.txt
    _root = MultibitNode()

    with open("dbtest.txt", 'r') as f:
        my_list = [line.rstrip('\n') for line in f]

    for address in my_list:
        ip, mask = address.split("/")
        binary_address=getMaskBin(address)
        with open("dbmask.txt", 'a') as f:
            f.write(str(binary_address)+'\n')
        _root.AddChild(ip, binary_address)

    return _root

def getMaskBin(address):
    # simple method to convert an IP address in its binary representation
    if address.find('/') != -1:
        ip = address.split("/")[0]
        mask = int(address.split("/")[1])
        return ''.join([bin(int(x) + 256)[3:] for x in ip.split('.')])[:mask]
    else:
        return ''.join([bin(int(x) + 256)[3:] for x in address.split('.')])

# DEBUG
if __name__ == "__main__":

    root = BuildTree()

    # Qui stiamo cercando 000. Se non lo trova usiamo il backtrack Default
    # print (root.lookup("000", 'Default'))
    
    # Qui stiamo cercando 010. Se non lo trova usiamo il backtrack Default altrimenti printa l'ip per intero
    # print (root.lookup("010", "Default"))
    
    # L'indirizzo che usavi tu aveva una mask non multipla di 3 quindi fa casino quando va a cercarlo, ricordi? Quindi fa sempre backtrack sul Default!


    

    times = []
    start = timeit.default_timer()
    print(root.RecursiveLookup('111000'))
    end = timeit.default_timer() - start
    times.append(end * 1000)
    print ("search time: " + str(sum(times)) + "ms")
    #print(getMaskBin('224.54.25.5/3'))
    times=[]
    start = timeit.default_timer()
    print(root.NonRecursiveLookup('111000'))
    end = timeit.default_timer() - start
    times.append(end * 1000)
    print ("search time: " + str(sum(times)) + "ms")