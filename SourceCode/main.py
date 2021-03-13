# key= input()
import time
import os
import binascii
from collections import deque
from bitvector_demo import *
from BitVector import *


keyText = "BUET CSE16 Batch"
plainText="WillGraduateSoon"
# cypherText=[]
w=[]

def printing(list):
    # print("round 0")
    for i in range(len(list)):
        print(list[i])
        if (i+1 )%4 == 0  and (i+1)/4 !=11:
            print("round ",(i+1)/4)


def sboxAndInvSboxGenerator():

    AES_modulus = BitVector(bitstring='100011011')
    Sbox= ['0x63']
    InvSbox=[0]*256
    for i in range(1,256):
        b = BitVector( intVal = i, size = 8 )
        b = b.gf_MI(AES_modulus, 8)

        p= copy.copy(b)
        q= copy.copy(b)
        r= copy.copy(b)
        t= copy.copy(b)

        p =  p<< 1
        q=q << 2
        r = r<<3
        t=t<<4

        l=bin(int("63",16))
        l=l[2:]
        dummy = BitVector(bitstring= l)
        ans=b^p^q^r^t^dummy
        Sbox.append(hex(ans.intValue()))

    for i in range(256):
        InvSbox[int(Sbox[i],16)] = hex(i)
        
    print(InvSbox)


def textMatrixBuilder(plain):
    p= 0
    q= 4
    output= [ ]
    if len(plain)>16:
        plain= plain[0:16]
    elif len(plain)<16:
        plain = "0000000000000000"+ plain+"0"
        plain = plain[-16:-1]
    # print(plain)
    plainTextChunk= [ hex(ord(plainText[i])) for i in range(len(plain))]
    print("plaintext : ",plain)
    print("plainText  Hex : " ,plainTextChunk)

    

    for i in range(4):
        temp = plainTextChunk[p+i*4:q+i*4]
        output.append(temp)
    n = len(output)
    output = [[row[i] for row in output] for i in range(n)]
    # print("plain text matrix is\n ")
    return output




def generatorFunction(list,roundcondition):
    for i in range(4):
        if int(list[i],16)< int('0xf',16):
            list[i] = "{0:#0{1}x}".format(int(list[i],16),4)
            # print(list[i])
    temp=[ hex(Sbox[(int(list[i][2],16))*16+int(list[i][3],16)])  for  i in range(4)]
    temp.append(temp.pop(0))  #used  for shifting
    for i in range(len(temp)):
        temp[i] = hex(int(temp[i],16) ^ int(roundcondition[i],16))
    # print("generating output is " , temp)
    return temp

    


def allKeyGenerator(key):
    p= 0
    q= 4
    if len(key)>16:
        key = key[0:16]
    elif len(key)<16:
        key = "0000000000000000"+ key
        key = key[-16:]
    hexKey=[]
    for i in range(len(key)):
        hexKey.append(hex(ord(key[i])))
    print("keytext :",key)
    print("key Hex :" ,hexKey)

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
    # w = allKeyGenerator(keyText)
    starter = w [0:4]
    n = len(starter)
    starter = [[row[i] for row in starter] for i in range(n)]
    current = textMatrixBuilder(plainText)
    xoringStarter(starter,current)

    for i in range(1,11):
        roundKey = w[4*i:4*i+4]
        roundKey = [[row[i] for row in roundKey] for i in range(n)]  #transposing to colum major format
        current= firstRound(current,roundKey,i)

    # global cypherText
    cypherText = [[row[i] for row in current] for i in range(n)]
    s=""
    print("cypherText is", cypherText)
    s=" "
    for  i in range(len(current)):
        for  j in range(len(current[i])):
            if int(current[i][j],16)<=int('0xf',16):
                    current[i][j] = "{0:#0{1}x}".format(int(current[i][j],16),4)
            current[i][j]=current[i][j][2:]
            obj=  bytes.fromhex(current[i][j])

            s=s+ obj.decode("unicode_escape")
    print("string is ",s)
    return cypherText

def decryptionStarter(cypherText):
    starter= w[-4:] 
    starter = [[row[i] for row in starter] for i in range(len(starter))]
    current= [[row[i] for row in cypherText] for i in range(len(cypherText))]
    xoringStarter(starter,current)

    for i in range(1,11):
        roundKey = w[-4*i -4 :-4*i]
        roundKey = [[row[i] for row in roundKey] for i in range(4)]  #transposing to colum major format
        current= decryptRound(current,roundKey,i)
    current= [[row[i] for row in current] for i in range(4)]
    s=" "
    decryptedHex=""
    for  i in range(len(current)):
        for  j in range(len(current[i])):
            if int(current[i][j],16)<=int('0xf',16):
                    current[i][j] = "{0:#0{1}x}".format(int(current[i][j],16),4)
            current[i][j]=current[i][j][2:]
            decryptedHex+=current[i][j]
            # obj=  bytes.fromhex(current[i][j])
            # s=s+ obj.decode("UTF-8")
    # print("string is ",s)
    # print("decrypted key is " ,current)

    return decryptedHex

def decryptRound(current,cycle,roundNum):
    for i in range(4):
        inverseShifter(current[i],i)
    inverseSub(current)
    current = xoringStarter(cycle,current)
    if( roundNum != 10):
        current = DecryptMixerColum(current)

    return current

def inverseSub(list):
    for i in range(4):
        for j in range(4):
            if int(list[i][j],16)<=int('0xf',16):
                    list[i][j] = "{0:#0{1}x}".format(int(list[i][j],16),4)
            list[i][j]= hex(InvSbox[(int(list[i][j][2],16))*16+int(list[i][j][3],16)])

def inverseShifter(list,cycle):   
    for i in range(cycle):
        list.insert(0,(list.pop(len(list)-1)))

def DecryptMixerColum(list):
    result = [['0x00','0x00','0x00','0x00'],
                ['0x00','0x00','0x00','0x00'],
                ['0x00','0x00','0x00','0x00'],
                ['0x00','0x00','0x00','0x00']]
         

    for i in range(len(InvMixer)):
        # iterate through columns of Y
        for j in range(len(list)):
            # iterate through rows of Y
            for k in range(len(list)):
                result[i][j] =  hex(int(result[i][j],16) ^ int(getConstant2(InvMixer[i][k],list[k][j]),16))

    return result
 
def firstRound(current,cycle,roundNum):
    substituter(current)
    for i in range(4):
        shifter(current[i],i)
    if( roundNum != 10):
        current = MixerColum(current)
    current = xoringStarter(cycle,current)

    return current

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

def fileEncryptor(current):
    # global w
    starter = w [0:4]
    n = len(starter)
    starter = [[row[i] for row in starter] for i in range(n)]
    
    # current = textMatrixBuilder(plainText)
    xoringStarter(starter,current)

    for i in range(1,11):
        roundKey = w[4*i:4*i+4]
        roundKey = [[row[i] for row in roundKey] for i in range(n)]  #transposing to colum major format
        current= firstRound(current,roundKey,i)

    cypherText = [[row[i] for row in current] for i in range(n)]
    s=""
    # print("cyphertext is", cypherText)
    s=" "
    for  i in range(len(current)):
        for  j in range(len(current[i])):
            if int(current[i][j],16)<=int('0xf',16):
                    current[i][j] = "{0:#0{1}x}".format(int(current[i][j],16),4)
            current[i][j]=current[i][j][2:]
            # obj=  bytes.fromhex(current[i][j])

            # s=s+ obj.decode("unicode_escape")
    # print("string is ",s)
    return cypherText
def main():
    file1=open('./SourceCode/dummy.txt',"rb")
    file2= open("./SourceCode/newFile.txt", "wb")

    b = file1.read()
    hexa = binascii.hexlify(b)
    print('hexa is ',hexa)
    n=hexa.decode('utf-8')#this suppresses the b and encodes to string
    # ni=hexa.decode('utf-8')#this suppresses the b and encodes to string

    m=n.encode('utf-8')#this brings up the b with  and encode to bytearray
    # print(n)
    padderLen= 32- len(n)%32
    if len(n)%32 != 0:
        padder = "0" * padderLen
        n= n + padder
        print(len(n))
    plain = []
    temp=[]

    for i in range(int(len(n)/2)):
        temp.append("0x" + n[i*2 : i*2+2])
        if (i+1)%4==0 :

            plain.append(temp)
            temp = []     #temp.clear will not work
 
    # printing(plain)
    # print(hex(int( temp[0],16)))
    # hexa= '42554554204353453136204261746368'

    
    w = allKeyGenerator(keyText)
    outputHex=""
    print( "round count is" ,int(len(plain)/4))
    for i in range(int(len(plain)/4)):
        # print("round ",i)
        y= plain[i*4:i*4+4]
        # print(y)
        y = [[row[t] for row in y] for t in range(4)]
        x=fileEncryptor(y)
        outputHex+=decryptionStarter(x)
    outputHex = outputHex[0 : -padderLen]
    outputHex=outputHex.encode('utf-8')
    # print("output hex is ",outputHex)
    # if(ni==outputHex):  
    #     print('same for here')
    
    q = binascii.unhexlify(outputHex)
    c=bytearray(q)
    file2.write(c)
    file2.close()
    # l=encryptionStarter()
    # k=decryptionStarter(l)

if __name__ == "__main__": 
    main()