from tkinter import *
from Binary import *
from Binary import BinaryNode
from MultiBit import MultibitNode
from Compressed import CompressedNode
#from Patricia import PatriciaNode ,("Patricia Trie",1,PatriciaNode)
def getBinPrefix(address):
    if address.find('/') != -1:
        ip = address.split("/")[0]
        print(ip)
        mask = int(address.split("/")[1])
        print(mask)
        return ''.join([bin(int(x) + 256)[3:] for x in ip.split('.')])[:mask]
    else:
        return ''.join([bin(int(x) + 256)[3:] for x in address.split('.')])

def is_binary(string):
    is_binary = True
    try:
        int(string, 2)
    except ValueError:
        is_binary = False
    return is_binary

root=Tk()
canvas1 = Canvas(root, width = 400, height = 300)
canvas1.pack()


v = IntVar()
root.title("LookApp")
Tries = [("Binary Trie",0,BinaryNode),("MultiBit Trie",2,MultibitNode),("Compressed Trie",3,CompressedNode)]
label0 =Label(root, text='Type your address:',font=('helvetica', 10))
canvas1.create_window(200, 100, window=label0)
x =Entry (root)
canvas1.create_window(200, 140, window=x)
address = x.get()
if is_binary(address)==False:
    print('cool')
    bin_addr=getPrefix(address)
    print('anothercool')


label1=Label(root,text='Lookup Algorithms',font=("Helvetica", 14)).pack()
label2=Label(root,text='Choose an Algorithm ',font=("Helvetica", 14)).pack()
for trie,val,node in Tries:
    Radiobutton(root, text=trie,padx = 20,variable=v,value=val,indicatoron = 0,command=lambda address : node.RecursiveLookup(bin_addr)).pack()

myLabel3=Label(root,text='Estimated search time:',font=("Helvetica", 14)).pack()


root.mainloop()