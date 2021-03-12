# key= input()
from collections import deque
from bitvector_demo import Sbox,InvSbox,getConstant ,Mixer,getConstant2


def printing(list):
    print("round 0")

    for i in range(len(list)):
        print(list[i])
        if (i+1 )%4 == 0  and (i+1)/4 !=11:
            print("round ",(i+1)/4)

keyText = "BUET CSE16 Batch"
plainText="WillGraduateSoon"
cypherText=[]


def textMatrixBuilder(plain):
    p= 0
    q= 4
    output= [ ]
    if len(plain)>16:
        plain= plain[0:16]
    elif len(plain)<16:
        plain = "0000000000000000"+ plain+"0"
        plain = plain[-16:-1]
    print(plain)
    plainTextChunk= [ hex(ord(plainText[i])) for i in range(len(plain))]
    

    for i in range(4):
        temp = plainTextChunk[p+i*4:q+i*4]
        output.append(temp)
    n = len(output)
    output = [[row[i] for row in output] for i in range(n)]
    print("plain text matrix is\n ")
    return output




def generatorFunction(list,roundcondition):
    for i in range(4):
        if int(list[i],16)< int('0xf',16):
            print('here ' , list[i])
            list[i] = "{0:#0{1}x}".format(int(list[i],16),4)
            # print(list[i])
    temp=[ hex(Sbox[(int(list[i][2],16))*16+int(list[i][3],16)])  for  i in range(4)]
    temp.append(temp.pop(0))  #used  for shifting
    for i in range(len(temp)):
        temp[i] = hex(int(temp[i],16) ^ int(roundcondition[i],16))
    print("generating output is " , temp)
    return temp

    


def allKeyGenerator(key):
    p= 0
    q= 4
    w= []
    if len(key)>16:
        key = key[0:16]
    elif len(key)<16:
        key = "0000000000000000"+ key+"0"
        key = key[-16:-1]
    hexKey=[]
    for i in range(len(key)):
        hexKey.append(hex(ord(key[i])))
    for i in range(4):
        temp = hexKey[p+i*4:q+i*4]
        w.append(temp)

    rc=['0x01','0x00','0x00','0x00']

    for i in range(10):
        output = generatorFunction((w[len(w)-1]),rc)
        temp = [hex(int(output[i],16) ^ int(w[len(w)-1-3][i],16) ) for i in range(4)]
        w.append(temp) 
        for i in range(3):
            temp = [hex(int(w[len(w)-1][j],16) ^ int(w[len(w)-1-3][j],16) ) for j in range(4)]
            # print(temp)
            w.append(temp)
        rc[0]= getConstant("02",rc[0])

    return w

def xoringStarter(s,p):  # will be stored in p
    for  i in range(4):
        for j in range(4):
            p[i][j]= hex(int(s[i][j],16) ^ int(p[i][j],16) )
    return p

def encryptionStarter():
    w = allKeyGenerator(keyText)
    starter = w [0:4]
    n = len(starter)
    starter = [[row[i] for row in starter] for i in range(n)]
    current = textMatrixBuilder(plainText)

    print(starter)
    xoringStarter(starter,current)

    for i in range(1,11):
        roundKey = w[4*i:4*i+4]
        roundKey = [[row[i] for row in roundKey] for i in range(n)]
        current= firstRound(current,roundKey,i)


    cypherText = [[row[i] for row in current] for i in range(n)]
    print("cypherText is " ,cypherText)

def decryptionStarter():
    print()



    
 
def firstRound(current,cycle,roundNum):
    substituter(current)
    for i in range(4):
        shifter(current[i],i)
    if( roundNum != 10):
        current = MixerColum(current)
    current = xoringStarter(cycle,current)

    return current
    print ( 'after round ' ,current)

def MixerColum(list):
    result = [['0x00','0x00','0x00','0x00'],
                ['0x00','0x00','0x00','0x00'],
                ['0x00','0x00','0x00','0x00'],
                ['0x00','0x00','0x00','0x00']]
         

    for i in range(len(Mixer)):
        # iterate through columns of Y
        for j in range(len(list)):
            # iterate through rows of Y
            for k in range(len(list)):
                result[i][j] =  hex(int(result[i][j],16) ^ int(getConstant2(Mixer[i][k],list[k][j]),16))

    return result

def substituter(list):
    for i in range(4):
        for j in range(4):
            if int(list[i][j],16)<=int('0xf',16):
                    list[i][j] = "{0:#0{1}x}".format(int(list[i][j],16),4)
            list[i][j]= hex(Sbox[(int(list[i][j][2],16))*16+int(list[i][j][3],16)])
    

def shifter(list,cycle):
    for i in range(cycle):
        list.append(list.pop(0))


encryptionStarter()

