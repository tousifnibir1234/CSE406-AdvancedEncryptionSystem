# key= input()
import copy
import time
import os
import binascii
from collections import deque
# from bitvector_demo import *
from BitVector import *


keyText = "BUET CSE16 Batch"
plainText="WillGraduateSoon . Let's party"
# cypherText=[]
w=[]
timer = {}
AES_modulus = BitVector(bitstring='100011011')
textPaddingLen=0

IsItText= True  # true for text , False for file

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]
def getConstant(item1,item2):
    item2=item2[2:]
    bv1 = BitVector(hexstring=item1)
    bv2 = BitVector(hexstring=item2)

    bv3 = bv1.gf_multiply_modular(bv2, AES_modulus, 8)
    # print(hex(int(str(bv3),2)))
    return hex(int(str(bv3),2))

def getConstant2(item1,item2):
    item2=item2[2:]
    bv1 = item1
    bv2 = BitVector(hexstring=item2)
    bv3 = bv1.gf_multiply_modular(bv2, AES_modulus, 8)
    return hex(int(str(bv3),2))

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
        

    print("\n\nSbox :")
    for i in range(256):
        if i %16==0 :
            print()
        print(Sbox[i],end =" ")

    print("\n\ninverseSbox :")
    for i in range(256):
        if i %16==0 :
            print()
        print(InvSbox[i],end =" ")


def textMatrixBuilder(plain):
    p= 0
    q= 4
    output= [ ]
    
    if(len(plain)%16!=0):
        global textPaddingLen
        textPaddingLen= 16-len(plain)
        padder = "0" * textPaddingLen
        plain =plain+ padder 

        plain = plain[0:16]
    # print(plain)
    plainTextChunk= [ hex(ord(plain[i])) for i in range(len(plain))]
    

    # decryptedHex=""
    # for  i in range(len(plainTextChunk)):
    #         if int(plainTextChunk[i],16)<=int('0xf',16):
    #                 plainTextChunk[i] = "{0:#0{1}x}".format(int(plainTextChunk[i],16),4)
    #         plainTextChunk[i]=plainTextChunk[i][2:]
    #         decryptedHex+=plainTextChunk[i]
            

    print("plaintext : ",plain)
    # print("plainText  Hex : " ,decryptedHex,"\n")

    

    for i in range(4):
        temp = plainTextChunk[p+i*4:q+i*4]
        output.append(temp)
    n = len(output)
    output = [[row[i] for row in output] for i in range(n)]
    # print("plain text matrix is\n ")
    x=fileEncryptor(output)
    decryptionStarter(x)

    # return output




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
    tic=time.perf_counter()
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
    
    encryptedHex=""
    for  i in range(len(hexKey)):
        if int(hexKey[i],16)<=int('0xf',16):
                hexKey[i] = "{0:#0{1}x}".format(int(hexKey[i],16),4)
        encryptedHex+=hexKey[i][2:]

    
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

    toc=time.perf_counter()
    print("keytext :",key)
    print("key Hex :" ,encryptedHex,"\n")
    global timer
    timer["Key Scheduling"]= toc-tic
    return w

def xoringStarter(s,p):  # will be stored in p
    for  i in range(4):
        for j in range(4):
            p[i][j]= hex(int(s[i][j],16) ^ int(p[i][j],16) )
    return p

def encryptionStarter():
    # w = allKeyGenerator(keyText)
    tic=time.perf_counter()

    starter = w [0:4]
    n = len(starter)
    starter = [[row[i] for row in starter] for i in range(n)]
    current = textMatrixBuilder(plainText)
    xoringStarter(starter,current)

    for i in range(1,11):
        roundKey = w[4*i:4*i+4]
        roundKey = [[row[i] for row in roundKey] for i in range(n)]  #transposing to colum major format
        current= firstRound(current,roundKey,i)

    toc=time.perf_counter()
    global timer
    timer["EncryptionTime"]= toc-tic
    # global cypherText
    cypherText = [[row[i] for row in current] for i in range(n)]
    s=""
    encryptedHex=""
    for  i in range(len(current)):
        for  j in range(len(current[i])):
            if int(current[i][j],16)<=int('0xf',16):
                    current[i][j] = "{0:#0{1}x}".format(int(current[i][j],16),4)
            current[i][j]=current[i][j][2:]
            encryptedHex+=current[i][j]
            obj=  bytes.fromhex(current[i][j])
            try:
                s=s+ obj.decode("unicode_escape")
            except:
                continue
    if IsItText:
        print("CypherText String is : \n",s)
        print("cypherText Hex is :", encryptedHex,"\n")
    return cypherText

def decryptionStarter(cypherText):
    tic=time.perf_counter()

    starter= w[-4:] 
    starter = [[row[i] for row in starter] for i in range(len(starter))]
    current= [[row[i] for row in cypherText] for i in range(len(cypherText))]
    xoringStarter(starter,current)

    for i in range(1,11):
        roundKey = w[-4*i -4 :-4*i]
        roundKey = [[row[i] for row in roundKey] for i in range(4)]  #transposing to colum major format
        current= decryptRound(current,roundKey,i)
    current= [[row[i] for row in current] for i in range(4)]
    toc=time.perf_counter()

    global timer
    timer["DecrytionTime"]= toc-tic

    s=" "
    decryptedHex=""
    for  i in range(len(current)):
        for  j in range(len(current[i])):
            if int(current[i][j],16)<=int('0xf',16):
                    current[i][j] = "{0:#0{1}x}".format(int(current[i][j],16),4)
            current[i][j]=current[i][j][2:]
            decryptedHex+=current[i][j]
            obj=  bytes.fromhex(current[i][j])
            try:
                s=s+ obj.decode("unicode_escape")
            except:
                continue
    # if IsItText :
        # if textPaddingLen !=0:
        #     s= s[0:-textPaddingLen]
    print("Decrypted string is :",s)
    print("decrypted Hex  is :" ,decryptedHex)

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

def decryptedStringPrinter(list):
    for  i in range(len(current)):
        for  j in range(len(current[i])):
            if int(current[i][j],16)<=int('0xf',16):
                    current[i][j] = "{0:#0{1}x}".format(int(current[i][j],16),4)
            current[i][j]=current[i][j][2:]
            decryptedHex+=current[i][j]
            obj=  bytes.fromhex(current[i][j])
            s=s+ obj.decode("unicode_escape")
    print("Decrypted string is ",s)

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
    starter = w [0:4]
    n = len(starter)
    starter = [[row[i] for row in starter] for i in range(n)]
    
    xoringStarter(starter,current)

    for i in range(1,11):
        roundKey = w[4*i:4*i+4]
        roundKey = [[row[i] for row in roundKey] for i in range(n)]  #transposing to colum major format
        current= firstRound(current,roundKey,i)

    cypherText = [[row[i] for row in current] for i in range(n)]
    
    for  i in range(len(current)):
        for  j in range(len(current[i])):
            if int(current[i][j],16)<=int('0xf',16):
                    current[i][j] = "{0:#0{1}x}".format(int(current[i][j],16),4)
            current[i][j]=current[i][j][2:]  

    return cypherText

def fileHandler():
    global IsItText
    IsItText = False
    x=input("\n\n\nEnter the  file name for encryption  : " )
    

    file1=open(x,"rb")
    file2= open("decrypted"+x, "wb") 
    file3 = open("encrpytion.txt","w")
    print("File Encription-Decryption process ongoing ")

    b = file1.read()
    hexa = binascii.hexlify(b)
    n=hexa.decode('utf-8')#this suppresses the b and encodes to string
    file3.write("Main Hex Code of file is: ")
    file3.write(n)
    # m=n.encode('utf-8')#this bring  s up the b with  and encode to bytearray
    # print(n)
    padderLen= 32- len(n)%32
    if len(n)%32 != 0:
        padder = "0" * padderLen
        n= n + padder
        # print(len(n))
    plain = []
    temp=[]

    for i in range(int(len(n)/2)):
        temp.append("0x" + n[i*2 : i*2+2])
        if (i+1)%4==0 :
            plain.append(temp)
            temp = []     #temp.clear will not work
 
    # print( "round count is" ,int(len(plain)/4))
    outputHex=""
    EncrytionHex=" "
    EncrytionAscii=" "
    for i in range(int(len(plain)/4)):
        # print("round ",i)
        y= plain[i*4:i*4+4]
        y = [[row[t] for row in y] for t in range(4)]
        x=fileEncryptor(y)
        p=getHexFromList(x)
        EncrytionHex+=p[0]
        EncrytionAscii+=p[1]
        outputHex+=decryptionStarter(x)

    file3.write("\nEncryptionHex is \n") ;file3.write(EncrytionHex) ;file3.write("\nEncryptionAscii is \n")
    file3.write(EncrytionAscii);file3.write("\noutputHex is \n");file3.write(outputHex)

    outputHex = outputHex[0 : -padderLen]
    outputHex=outputHex.encode('utf-8')

    q = binascii.unhexlify(outputHex) #unhexlify converts hex to other
    c=bytearray(q)
    file2.write(c)
    file2.close()

    IsItText = True
    print("File Encription-Decryption process finished .\nCheck encryption & decrypted  file" )


def getHexFromList(current):
    encryption = ""
    s=""
    for  i in range(len(current)):
        for  j in range(len(current[i])):
            if int(current[i][j],16)<=int('0xf',16):
                    current[i][j] = "{0:#0{1}x}".format(int(current[i][j],16),4)
            obj=  bytes.fromhex(current[i][j][2:])
            s+=current[i][j][2:]  
            try:
                encryption+= obj.decode("unicode_escape")
            except:
                continue
    return [s ,encryption]
def main():
    w = allKeyGenerator(keyText)
    # print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")


    # x= input("Give the Plain text : ")
    # global plainText
    # plainText=x

    textMatrixBuilder(plainText)
    # l=encryptionStarter()
    # k=decryptionStarter(l)
    # sboxAndInvSboxGenerator()

    print("\n\n")
    for key,value in timer.items():
        print ( key ,"  : ", value)
    # print("\n",timer)

    # fileHandler()



if __name__ == "__main__": 
    main()