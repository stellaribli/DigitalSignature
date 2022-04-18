import os
import os.path
import sys
# from numpy import insert
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import codecs
import PyQt5.QtWidgets as pyqt
import random
import hashlib

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
        file_pubkey = open('PublicKey.pub', 'w')
        file_pubkey.write(str(pubKey))
        file_pubkey.close()

        file_prikey = open('PrivateKey.pri', 'w')
        file_prikey.write(str(priKey))
        file_prikey.close()
    
    return(priKey,pubKey,n)

def readFile(filename):
    file = open(filename, 'rt')
    text = file.read()
    idx = text.find('<ds>')
    idx2 = text.find('</ds>')
    file.close()
    if ((idx == -1) or (idx2 == -1)):
        return 'Error'
    else:
        return(text[:idx])

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

#File Terpisah
def insertSignaturePisah(filename,p, q, privKey): #export signature to a new file
    file = open(filename,'rt')
    isifile = file.read()
    signature = encSignature(hashSHA(isifile),p*q,privKey)
    fileBaru = open('Sign.txt', 'w')
    teksSign = '<ds>' + str(hex(signature)) + '</ds>'
    fileBaru.write(teksSign)
    fileBaru.close()
    return 
def verifyPisah(filename,filesignature,p,q,pubKey):
    signature = readSignatureFile(filesignature)
    if signature == 'Error':
        return False
    else:
        signature = convHexaDec(signature)
        hAksen = encSignature(signature,p*q,pubKey)
        file = open(filename,'rt')
        isifile = file.read()
        hashedPass = int(hashSHA(isifile))%(p*q)
        if hAksen == hashedPass:
            return True
        else:
            return False

#File Tidak Terpisah
def insertSignatureSameFile(filename,signature): #Returns New File with Signature
    file = open(filename,'rt')
    teksawal = file.read()
    fileBaru = open(filename, 'w')
    teksSign = '<ds>' + str(signature) + '</ds>'
    fileBaru.write(teksawal + teksSign)
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

#InsertButton
def insertButtonSameFile(filename,p,q,privKey):
    file = open(filename, 'rt')
    isifile = str(file.read())
    signature = encSignature(hashSHA(isifile),p*q,privKey)
    signature = hex(signature)
    insertSignatureSameFile(filename,signature)

#VerifyButton
def verifyButtonSameFile(filename,p,q,pubKey):
    signature = readSignatureFile(filename)
    if signature == 'Error':
        return 'Tidak Ada'
    else:
        signature = convHexaDec(signature)
        isifile = readFile(filename)
        hAksen = encSignature(signature,p*q,pubKey)
        hashedPass = int(hashSHA(isifile))%(p*q)
        print(hAksen, hashedPass)
        if hAksen == hashedPass:
            return 'True'
        else:
            return 'Tidak Sesuai'

class Landing(QDialog):
    def __init__(self):
        super(Landing, self).__init__()
        loadUi("landingpage.ui", self)
        self.disatukan.clicked.connect(self.goToSatukan)
        self.terpisah.clicked.connect(self.goToPisah)
    def goToSatukan(self):
        widget.setCurrentIndex(1)
    def goToPisah(self):
        widget.setCurrentIndex(4)

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

class Pisah(QDialog):
    def __init__(self):
        super(Pisah, self).__init__()
        loadUi("pisah.ui", self)
        self.backButton.clicked.connect(self.goBack)
        self.verifikasi.clicked.connect(self.goToVerifPisah)
        self.insert.clicked.connect(self.goToInsertPisah)
    def goBack(self):
        widget.setCurrentIndex(0)    
    def goToVerifPisah(self):
        widget.setCurrentIndex(6)    
    def goToInsertPisah(self):
        widget.setCurrentIndex(5)    

class InsertPisah(QDialog):
    def __init__(self):
        super(InsertPisah, self).__init__()
        loadUi("insertSigPisah.ui", self)
        self.backButton.clicked.connect(self.goBack)
        self.genButton.clicked.connect(self.genKey)
        self.uploadButton.clicked.connect(self.upload)
        self.uploadedFile = None 
        self.namaFile = ''
        self.insertSig.clicked.connect(self.result)
    def goBack(self):
        widget.setCurrentIndex(4)  
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
            self.namaFile = str(os.path.basename(fileName))
            data = open(fileName,"rt")
            text = data.read()
            data.close()
            fileBaru = open(self.namaFile,'w')
            fileBaru.write(str(text))
            fileBaru.close()
  
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
            insertSignaturePisah(self.namaFile,int(nilaiP),int(nilaiQ),privKey)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Berhasil!")
            msg.setInformativeText('Tanda Tangan Berhasil!')
            msg.exec_()

class VerifPisah2(QDialog):
    def __init__(self):
        super(VerifPisah2, self).__init__()
        loadUi("verifSigPisah2.ui", self)
        self.backButton.clicked.connect(self.goBack)
        self.uploadButton.clicked.connect(self.upload)
        self.uploadPub.clicked.connect(self.uploadKey)
        self.uploadSign.clicked.connect(self.uploadSignature)
        self.uploadedFile = None 
        self.uploadedPub = None 
        self.uploadedSignature = None
        self.namaFile = ''
        self.verifikasi.clicked.connect(self.result)
    def goBack(self):
        widget.setCurrentIndex(4) 
    def upload(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload File","","Text files (*.txt)")
        if fileName:
            global data
            self.uploadedFile = fileName
            self.fileName.setText(os.path.basename(fileName))
            self.namaFile = os.path.basename(fileName)
            file = open(fileName,"rt")
            data = file.read()
            file.close()
            fileBaru = open(self.namaFile,'w')
            fileBaru.write(str(data))
            fileBaru.close()
    def uploadSignature(self):
        signFile, _ = QFileDialog.getOpenFileName(self, "Upload File","","Text files (*.txt)")
        if signFile:
            global dataSign
            self.uploadedSignature = signFile
            self.fileName3.setText(os.path.basename(signFile))
            self.namaFileSign = os.path.basename(signFile)
            file = open(signFile,"rt")
            dataSign = file.read()
            file.close()
            fileBaru = open(self.namaFileSign,'w')
            fileBaru.write(str(dataSign))
            fileBaru.close()
    def uploadKey(self):
        pubFile, _ = QFileDialog.getOpenFileName(self, "Upload File","","Text files (*.pub *.txt)")
        if pubFile:
            global dataPub
            self.uploadedPub = pubFile
            self.fileName2.setText(os.path.basename(pubFile))
            file = open(pubFile,"rt")
            dataPub = file.read()
            file.close()
            fileBaru = open('PublicKey.pub','w')
            fileBaru.write(str(dataPub))
            fileBaru.close()    
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
            pubKeyFile = open('PublicKey.pub','r')
            pubKey = int(pubKeyFile.read())
            hasilVerifikasi = verifyPisah(self.namaFile,self.namaFileSign,int(nilaiP),int(nilaiQ),pubKey)
            if hasilVerifikasi:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Berhasil!")
                msg.setInformativeText('Tanda Tangan Terverifikasi')
                msg.exec_()         
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Gagal")
                msg.setInformativeText('Tanda Tangan Tidak Berhasil Diverifikasi')
                msg.exec_()    

class VerifSatu(QDialog):
    def __init__(self):
        super(VerifSatu, self).__init__()
        loadUi("verifSigSatu.ui", self)
        self.backButton.clicked.connect(self.goBack)
        self.uploadButton.clicked.connect(self.upload)
        self.uploadPub.clicked.connect(self.uploadKey)
        self.uploadedFile = None 
        self.uploadedPub = None 
        self.namaFile = ''
        self.verifikasi.clicked.connect(self.result)
    def goBack(self):
        widget.setCurrentIndex(1) 
    def upload(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload File","","Text files (*.txt)")
        if fileName:
            global data
            self.uploadedFile = fileName
            self.fileName.setText(os.path.basename(fileName))
            self.namaFile = os.path.basename(fileName)
            file = open(fileName,"rt")
            data = file.read()
            file.close()
            fileBaru = open(self.namaFile,'w')
            fileBaru.write(str(data))
            fileBaru.close()
    def uploadKey(self):
        pubFile, _ = QFileDialog.getOpenFileName(self, "Upload File","","Text files (*.pub *.txt)")
        if pubFile:
            global dataPub
            self.uploadedPub = pubFile
            self.fileName2.setText(os.path.basename(pubFile))
            file = open(pubFile,"rt")
            dataPub = file.read()
            file.close()
            fileBaru = open('PublicKey.pub','w')
            fileBaru.write(str(dataPub))
            fileBaru.close()    
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
            pubKeyFile = open('PublicKey.pub','r')
            pubKey = int(pubKeyFile.read())
            hasilVerifikasi = verifyButtonSameFile(self.namaFile,int(nilaiP),int(nilaiQ),pubKey)
            if hasilVerifikasi == 'True':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Berhasil!")
                msg.setInformativeText('Tanda Tangan Terverifikasi')
                msg.exec_()         
            else:
                if hasilVerifikasi == 'Tidak Ada':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Gagal")
                    msg.setInformativeText('Tanda Tangan Tidak Ada')
                    msg.exec_()    
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Gagal")
                    msg.setInformativeText('Tanda Tangan Tidak Berhasil Diverifikasi')
                    msg.exec_()     
                 
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
            self.namaFile = str(os.path.basename(fileName))
            data = open(fileName,"rt")
            text = data.read()
            data.close()
            fileBaru = open(self.namaFile,'w')
            fileBaru.write(str(text))
            fileBaru.close()
  
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

widget.addWidget(Pisah())  # Index jadi 4
widget.addWidget(InsertPisah()) # Index jadi 5
widget.addWidget(VerifPisah2()) # Index jadi 6
widget.setCurrentIndex(0)
widget.setFixedWidth(800)
widget.setFixedHeight(320)
widget.show()

app.exec_()