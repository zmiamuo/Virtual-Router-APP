import timeit
 

class BinaryNode(object):
    def __init__(self, NextHop=""):
        self.NextHop = NextHop  
        self.Left = None 
        self.Right = None  
        self.path=''

    def AddChild(self, address, path):
        if len(path) == 0:
            return

        if len(path) == 1:
            if path == "0":
                self.Left = BinaryNode(NextHop=address)
            else:
                self.Right = BinaryNode(NextHop=address)
        elif len(path) > 1:
            if path[0]=="0":
                if self.Left is None:
                    self.Left = BinaryNode()
                self.Left.AddChild(address, path[1:])

            else:
                if self.Right is None:
                    self.Right = BinaryNode()
                self.Right.AddChild(address, path[1:])

    def RecursiveLookup(self, address, backtrack=""):
        if self.NextHop != "":  
            backtrack = self.NextHop
        if address == "" or (self.Left is None and self.Right is None):  
            return backtrack
        if address[0]=="0":  # for each hop we check whether go to the left or right branch
            if self.Left is not None:  # if there's still a child, look deeper in the trie
                return self.Left.RecursiveLookup(address[1:], backtrack)
            else:  # otherwise return the last valid prefix
                return backtrack
        else:
            if self.Right is not None:
                return self.Right.RecursiveLookup(address[1:], backtrack)
            else:
                return backtrack
    def NonRecursiveLookup(self, address, backtrack = ""):
        node = self
        while (node is not None):
            if node.NextHop != "":
                backtrack = node.NextHop
            if address == "" or (node.Left is None and node.Right is None):
                return backtrack
            if address[0]=="0":
                if node.Left is not None:
                    address = address[1:]
                    node = node.Left
                else:
                    return backtrack
            else:
                if node.Right is not None:
                    address = address[1:]
                    node = node.Right
                else:
                    return backtrack

        return backtrack

    def printTree(self):
        if self.Left:
            self.Left.printTree()
        print(self.path)
        if self.Right:
            self.Right.printTree()


def BuildTree(default='0'): 
    _root = BinaryNode(default)
    
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
    if address.find("/") != -1:
        ip = address.split("/")[0]
        mask = int(address.split("/")[1])
        return ''.join([bin(int(x) + 256)[3:] for x in ip.split(".")])[:mask]
    else:
        return ''.join([bin(int(x) + 256)[3:] for x in address.split(".")])

    


if __name__ == "__main__":

    root = BuildTree()
    
    
    times= []
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