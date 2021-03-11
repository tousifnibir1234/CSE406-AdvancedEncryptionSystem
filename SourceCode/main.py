# key= input()
from collections import deque
from bitvector_demo import Sbox,InvSbox 


def printing(list):
    for i in range(len(list)):
        print(list[i])

key = "Thats my Kung Fu"
if len(key)>=16:
    print(key[0:16])
elif len(key)<=16:
    key = "0000000000000000"+ key+"0"
    print(key[-16:-1])
hexKey=[]
for i in range(len(key)):
    hexKey.append(hex(ord(key[i])))

p= 0
q= 4
w= []
for i in range(4):
    temp = hexKey[p+i*4:q+i*4]
    w.append(temp)

def generatorFunction(list,roundcondition):
    temp=[ hex(Sbox[(int(list[i][2],16))*16+int(list[i][3],16)])  for  i in range(4)]
    temp.append(temp.pop(0))
    for i in range(len(temp)):
        temp[i] = hex(int(temp[i],16) ^ roundcondition[i])
    print("generating output is " , temp)
    return temp

    

def allKeyGenerator(list):
    rc=[0x01,0x00,0x00,0x00]

    for i in range(1):
        output = generatorFunction((w[len(w)-1]),rc)
        temp = [hex(int(output[i],16) ^ int(w[0][i],16) ) for i in range(4)]
        w.append(temp) 
        for i in range(3):
            temp = [hex(int(w[len(w)-1][j],16) ^ int(w[len(w)-1-3][j],16) ) for j in range(4)]
            # print(temp)
            w.append(temp)

        roundKeyGenerator

allKeyGenerator(w) 
printing(w)