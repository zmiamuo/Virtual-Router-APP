import timeit

class PatriciaNode(object):
    def __init__(self, NextHop=""):
        self.NextHop = NextHop  # here we save the value of the leaf node
        self.Left = None  # 0's branch
        self.Right = None  # 1's branch
        self.bitIndex=NextHop[i]



        def AddChild(self, prefix, path):
            if len(path) == 0:
                return

            if len(path) == 1:
                if path == "0":
                    self.Left = PatriciaNode(NextHop=prefix)
                else:
                    self.Right = PatriciaNode(NextHop=prefix)
            elif len(path) > 1:
                if path[0]=="0":
                    if self.Left is None:
                        self.Left = PatriciaNode()

                    self.Left.AddChild(prefix, path[1:])

                else:
                    if self.Right is None:
                        self.Right = PatriciaNode()

                    self.Right.AddChild(prefix, path[1:])

def BuildTree(default='0'): # create the binary trie using the dbtest.txt and dbmask.txt
    _root = PatriciaNode(default)

    with open("dbtest.txt", 'r') as f:
        my_list = [line.rstrip('\n') for line in f]

    for address in my_list:
        ip, mask = address.split("/")
        binary_address=getMaskBin(address)
        with open("dbmask.txt", 'a') as f:
            f.write(str(binary_address)+'\n')
        _root.AddChild(ip, binary_address)
    return _root
def BuildPatricia():
    if self.NextHop != ""

def getMaskBin(address): #get the binary mask of the address
    if address.find('/') != -1:
        ip = address.split("/")[0]
        mask = int(address.split("/")[1])
        return ''.join([bin(int(x) + 256)[3:] for x in ip.split('.')])[:mask]
    else:
        return ''.join([bin(int(x) + 256)[3:] for x in address.split('.')])


#TEST
if __name__ == "__main__":

    root = BuildTree()


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