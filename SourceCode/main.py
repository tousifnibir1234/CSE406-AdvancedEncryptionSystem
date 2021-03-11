# key= input()
from collections import deque
from bitvector_demo import Sbox,InvSbox,getConstant 


def printing(list):
    print("round 0")

    for i in range(len(list)):
        print(list[i])
        if (i+1 )%4 == 0  and (i+1)/4 !=11:
            print("round ",(i+1)/4)

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
    for i in range(4):
        if int(list[i],16)< int('0xf',16):
            print('here ' , list[i])
            list[i] = "{0:#0{1}x}".format(int(list[i],16),4)
            print(list[i])
    temp=[ hex(Sbox[(int(list[i][2],16))*16+int(list[i][3],16)])  for  i in range(4)]
    temp.append(temp.pop(0))
    for i in range(len(temp)):
        temp[i] = hex(int(temp[i],16) ^ int(roundcondition[i],16))
    print("generating output is " , temp)
    return temp

    


def allKeyGenerator(list):
    rc=['0x01','0x00','0x00','0x00']

    for i in range(10):
        output = generatorFunction((w[len(w)-1]),rc)
        temp = [hex(int(output[i],16) ^ int(w[len(w)-1-3][i],16) ) for i in range(4)]
        w.append(temp) 
        for i in range(3):
            temp = [hex(int(w[len(w)-1][j],16) ^ int(w[len(w)-1-3][j],16) ) for j in range(4)]
            # print(temp)
            w.append(temp)
        rc[0]= getConstant(rc[0])
        

allKeyGenerator(w) 
printing(w)