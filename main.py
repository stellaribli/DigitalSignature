import base64
import os
import os.path
import sys

from numpy import insert
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import codecs
import PyQt5.QtWidgets as pyqt
import random
import hashlib
import pytesseract
import cv2

namaFile = ''
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
    fileBaru = open(filename, 'w')
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


p = 11
q = 13
#GenKeyButton
generateKey(p,q)

privKeyFile = open('PrivateKey.pri','r')
privKey = int(privKeyFile.read())
pubKeyFile = open('PublicKey.pub','r')
pubKey = int(pubKeyFile.read())

filename = 'test.txt'

#InsertButton
def insertButtonSameFile(filename,p,q,privKey):
    signature = encSignature(hashSHA(filename),p*q,privKey)
    insertSignatureSameFile(filename,signature)

#VerifyButton
def verifyButtonSameFile(filename,p,q,pubKey):
    signature = int(readSignatureFile(filename))
    hAksen = encSignature(signature,p*q,pubKey)
    hashedPass = int(hashSHA(filename))%(p*q)
    if hAksen == hashedPass:
        return True
    else:
        return False

# insertButtonSameFile('test.txt',p,q,privKey)
# print(verifyButtonSameFile('test.txt',p,q,pubKey))

class Landing(QDialog):
    def __init__(self):
        super(Landing, self).__init__()
        loadUi("landingpage.ui", self)
        self.disatukan.clicked.connect(self.goToSatukan)
    def goToSatukan(self):
        widget.setCurrentIndex(1)

class Satu(QDialog):
    def __init__(self):
        super(Satu, self).__init__()
        loadUi("disatukan.ui", self)
        self.backButton.clicked.connect(self.goBack)
        self.verifikasi.clicked.connect(self.goToVerif)
        self.insert.clicked.connect(self.goToInsert)
    def goBack(self):
        widget.setCurrentIndex(0)    
    def goToVerif(self):
        widget.setCurrentIndex(2)    
    def goToInsert(self):
        widget.setCurrentIndex(3)    

class VerifSatu(QDialog):
    def __init__(self):
        super(VerifSatu, self).__init__()
        loadUi("verifSigSatu.ui", self)
        self.backButton.clicked.connect(self.goBack)
    def goBack(self):
        widget.setCurrentIndex(1) 

class InsertSatu(QDialog):
    def __init__(self):
        super(InsertSatu, self).__init__()
        loadUi("insertSigSatu.ui", self)
        self.backButton.clicked.connect(self.goBack)
        self.genButton.clicked.connect(self.genKey)
        self.uploadButton.clicked.connect(self.upload)
        self.uploadedFile = None 
        self.namaFile = ''
        self.insertSig.clicked.connect(self.result)

    def goBack(self):
        widget.setCurrentIndex(1)  
    def genKey(self):
        nilaiP = self.nilaip.text()
        nilaiQ = self.nilaiq.text()
        if nilaiP == '' or nilaiQ == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('P dan Q belum diinput!')
            msg.exec_()
        else:
            generateKey(int(nilaiP),int(nilaiQ))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Berhasil")
            msg.setInformativeText('Kunci Publik dan Private Berhasil Dibuat!')
            msg.exec_()
    def upload(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload File","","Text files (*.txt)")
        if fileName:
            global data
            self.uploadedFile = fileName
            self.fileName.setText(os.path.basename(fileName))
            self.namaFile = os.path.basename(fileName)
            data = open(fileName,"rt")
            fileBaru = open(self.namaFile,'w')
            fileBaru.write(str(data.read()))
        else:
            print("No file selected")     

    def result(self):
        nilaiP = self.nilaip.text()
        nilaiQ = self.nilaiq.text()
        if nilaiP == '' or nilaiQ == '' or self.namaFile == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Pastikan seluruh field telah terisi!')
            msg.exec_()  
        else:
            privKeyFile = open('PrivateKey.pri','r')
            privKey = int(privKeyFile.read())
            insertButtonSameFile(self.namaFile,int(nilaiP),int(nilaiQ),privKey)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Berhasil!")
            msg.setInformativeText('Tanda Tangan Berhasil diinput!')
            msg.exec_()  
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.addWidget(Landing())  # Index jadi 0
widget.addWidget(Satu())  # Index jadi 1
widget.addWidget(VerifSatu())  # Index jadi 2
widget.addWidget(InsertSatu())  # Index jadi 3
widget.setCurrentIndex(0)
widget.setFixedWidth(800)
widget.setFixedHeight(320)
widget.show()

app.exec_()