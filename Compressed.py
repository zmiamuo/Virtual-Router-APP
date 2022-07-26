import timeit

class CompressedNode(object):
    def __init__(self, NextHop="", Segment=""):
        self.NextHop = NextHop
        self.Left = None 
        self.Right = None  
        self.Segment = Segment
        self.Skip = len(Segment)

    def AddChild(self, prefix, path):
        if len(path) == 0:
            return
        if len(path) == 1:
            if path == "0":
                self.Left = CompressedNode(NextHop=prefix)
            else:
                self.Right = CompressedNode(NextHop=prefix)
        elif len(path) > 1:
            if path[0]=="0":
                if self.Left is None:
                    self.Left = CompressedNode()

                self.Left.AddChild(prefix, path[1:])

            else:
                if self.Right is None:
                    self.Right = CompressedNode()

                self.Right.AddChild(prefix, path[1:])

    def Lookup(self, address, rootPrefix="0"):
        backtrack = ""
        node = self
        while node is not None:
            if node.NextHop != "":
                backtrack = node.NextHop
            if address == "" or (node.Left is None and node.Right is None):
                return backtrack
            if address[0]=="0":
                if node.Left is not None and len(address) >= node.Left.Skip +1 and (node.Left.Segment == "" or address[0]==("0" + node.Left.Segment)):
                    address = address[node.Left.Skip+1:]
                    node = node.Left
                else:
                    return backtrack
            else:
                if node.Right is not None and len(address) >= node.Right.Skip + 1 and (node.Right.Segment == "" or address[0]==("0" + node.Right.Segment)):
                    address = address[node.Right.Skip+1:]
                    node = node.Right
                else:
                    return backtrack

        return backtrack

    def Compress(self, segment=""):
        if self.Right is None and self.Left is None:
            self.Segment = segment
            return self
        if self.Right is not None and self.Left is not None:
            self.Right = self.Right.Compress("")
            self.Left = self.Left.Compress("")
            self.Segment = segment
            return self
        if self.NextHop != "":
            self.Segment = segment
            if self.Left is not None:
                self.Left = self.Left.Compress("")
            elif self.Right is not None:
                self.Right = self.Right.Compress("")
            return self
        else:
            if self.Left is not None:
                return self.Left.Compress(segment + '0')
            else:
                return self.Right.Compress(segment + '1')


def getMaskBin(address):
    if address.find('/') != -1:
        ip = address.split("/")[0]
        mask = int(address.split("/")[1])
        return ''.join([bin(int(x) + 256)[3:] for x in ip.split('.')])[:mask]
    else:
        return ''.join([bin(int(x) + 256)[3:] for x in address.split('.')])

def Create(default_value = '0'):
    _root = CompressedNode(default_value)
    with open("C:\\Users\\hp\\Desktop\\lookupproject\\test.txt", 'r') as f:
        my_list = [line.rstrip('\n') for line in f]

    for address in my_list:
        ip, mask = address.split("/")
        binary_address=getMaskBin(address)
        with open("dbmask.txt", 'a') as f:
            f.write(str(binary_address)+'\n')
        _root.AddChild(ip, binary_address)

    _root.Compress()
    return _root


def __create_random_ip_list(list_length=10000, for_creating_tries=True):
    # creating set of ips for creating/searching tries.
    import random

    if for_creating_tries:
        with open('db.txt', 'w') as f:
            for i in range(1, list_length):
                ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
                mask = str(random.choice([8, 12, 16, 24, 28]))
                f.write(ip + "\\" + mask + "," + getMaskBin(ip)[:int(mask)] + "\n")
    else:  # else it means that it is for searching
        with open('to_search.txt', 'w') as f:
            for i in range(1, list_length):
                ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
                mask = str(random.choice([8, 12, 16, 24, 28]))
                f.write(ip + "\\" + mask + "," + getMaskBin(ip)[:mask] + "\n")


# DEBUG
if __name__ == "__main__":

    root = Create("0")


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