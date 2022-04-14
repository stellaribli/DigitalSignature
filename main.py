import base64
import os
import os.path
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import codecs
import PyQt5.QtWidgets as pyqt
import random
import hashlib
import pytesseract
import cv2

#FUNGSI KEY
def gcd(x,y):
    if x > y:
        var = y
    else:
        var = x
    for i in range(1, var+1):
        if((x % i == 0) and (y % i == 0)):
            gcd = i     
    return gcd
def isPrime(x):
    found=True
    if (x > 1):
        for i in range(2, x):
            if (x % i) == 0:
                found= False 
        
    return found   
def generateKey(p, q):
    if (isPrime(p) and (isPrime(q) == False)):
        raise Exception("p dan q harus prima")
        
    elif (isPrime(p)) and (isPrime(q)): # jika p dan q sudah prima
    
        n = p * q
        totient = (p-1)*(q-1)

        # generate public key
        pubKey = random.randrange(1, totient)
        e = gcd(pubKey,totient)
        while e != 1:
            pubKey = random.randrange(1,totient)
            e = gcd (pubKey,totient)
        
        # generate private key
        found = 0
        k = 1
        while not(found):
            priKey = (1+k*totient)/pubKey
            if ((pubKey*int(priKey))%totient == 1):
                found = 1    
            k = k+1
        priKey = int(priKey)
        # print (str(pubKey)+" "+str(priKey)+" "+ str(n))
        
        # export public dan private key
        file_pubkey = open('PublicKey.pub', 'w')
        file_pubkey.write(str(pubKey))
        # file_pubkey.write(" ")
        # file_pubkey.write(str(n))
        file_pubkey.close()

        file_prikey = open('PrivateKey.pri', 'w')
        file_prikey.write(str(priKey))
        # file_prikey.write(" ")
        # file_prikey.write(str(n))
        file_prikey.close()
    
    return(priKey,pubKey,n)

#Algoritma Digital Signature
def convHexaDec(hexa): 
    return(int(hexa,16))

def hashSHA(text): #Returns hashed text in Decimals
    hash_object = hashlib.sha1(text.encode())
    pbHash = hash_object.hexdigest()
    return convHexaDec(pbHash)

def encSignature(h,n,Key):
    result = (h**Key) % n
    return result

#File Tidak Terpisah
def insertSignatureSameFile(filename,signature): #Returns New File with Signature
    file = open(filename,'rt')
    teksawal = file.read()
    fileBaru = open('Hasil.txt', 'w')
    fileBaru.write(teksawal)
    teksSign = '<ds>' + str(signature) + '</ds>'
    fileBaru.write(teksSign)
    file.close()
    fileBaru.close()
    return

def readSignatureFile(filename): # Returns Error or Signature on File
    file = open(filename, 'rt')
    text = file.read()
    idx = text.find('<ds>')
    idx2 = text.find('</ds>')
    file.close()
    if ((idx == -1) or (idx2 == -1)):
        return 'Error'
    else:
        return(text[idx+4:idx2])


