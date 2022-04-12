import base64
import os
import os.path
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QFileDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import codecs
import PyQt5.QtWidgets as pyqt
from time import process_time
from main import decrypt
import random

global data
global teks

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

#FUNGSI ENKRIPSI DEKRIPSI
def konversiASCII(base64teks):
    inputEnk = ''
    for i in range(len(base64teks)):
        ordB = ord(base64teks[i])
        if ordB<10:
            inputEnk = inputEnk + '00' + str(ordB) + ' '
        elif ordB<100:
            inputEnk = inputEnk + '0' + str(ordB) + ' '
        else:
            inputEnk = inputEnk +str(ordB) + ' '
    return inputEnk
def encryptFunction (M,e,n):
        t1 = process_time()
        Cipher = ''
        C = ''
        hasil = ''
        i=0
        for i in range(len(M)//4):
            C = M[i*4:((i*4)+4)]
            hasil = (int(C)**e)%n
            if hasil < 10:
                Cipher = Cipher + '000' + str(hasil) + ' '
            elif hasil < 100:
                Cipher = Cipher + '00' + str(hasil) + ' '
            elif hasil < 1000:
                Cipher = Cipher + '0' + str(hasil) + ' '
            else:
                Cipher = Cipher + str(hasil) + ' '
        
        sisahberapa = len(M)%4
        if sisahberapa !=0:
            C = M[len(M)-sisahberapa:]
            hasil = (int(C)**e)%n
            if hasil < 10:
                Cipher = Cipher + '000' + str(hasil) + ' '
            elif hasil < 100:
                Cipher = Cipher + '00' + str(hasil) + ' '
            elif hasil < 1000:
                Cipher = Cipher + '0' + str(hasil) + ' '
            else:
                Cipher = Cipher + str(hasil) + ' '
        # print(Cipher)
        # print(sisahberapa)
        # print(M[len(M)-sisahberapa:])
        t2 = process_time()
        t = t2-t1
        # Cipher = hex(int(Cipher.replace(' ','')))
        file = open('HasilKonversiEncrypt.txt', 'w')
        # file.write(hex(int(Cipher.replace(' ',''))))
        file.write(Cipher)
        file.close()
        file_size = os.path.getsize('HasilKonversiEncrypt.txt')
        return Cipher, t, file_size
def decryptFunction (C,d,n):
        t1 = process_time()
        C = str(C).replace(' ','')
        Plain = ''
        P = ''
        hasil = ''
        for i in range(len(C)//4):
            P = C[i*4:((i*4)+4)]
            hasil = (int(P)**d)%n
            if hasil < 10:
                Plain = Plain + '00' + str(hasil) + ' '
            elif hasil < 100:
                Plain = Plain + '0' + str(hasil) + ' '
            else:
                Plain = Plain + str(hasil)
        t2 = process_time()
        t = t2-t1
        file = open('HasilKonversiDecrypt.txt', 'w')
        file.write(konversibase64(Plain))
        file.close()
        file_size = os.path.getsize('HasilKonversiDecrypt.txt')
        return Plain, t, file_size  
def konversibase64(base64teks):
    base64teks = base64teks.replace(" ","")
    inputEnk = ''
    for i in range(len(base64teks)//3):
        add = base64teks[i*3:(i*3)+3]
        inputEnk = inputEnk + str(chr(int(add)))
    return inputEnk
def konversiHex(angka):
    angka = str(angka).replace(" ","")
    angka = int(angka)
    angka = hex(angka)
    return angka

#Halaman Utama
class Landing(QDialog):
    def __init__(self):
        super(Landing, self).__init__()
        loadUi('landingpage.ui', self)
        self.teks.clicked.connect(self.goTeks)
        self.nonteks.clicked.connect(self.goNon)
    def goTeks(self):
        widget.setCurrentIndex(2)
    def goNon(self):
        widget.setCurrentIndex(1)

#Enkripsi Teks Biasa -> 26 char
class Text(QDialog):
    def __init__(self):
        super(Text, self).__init__()
        loadUi('text.ui', self)
        self.uploadButton.clicked.connect(self.upload)
        self.uploadedFile = None 
        self.encryptB.clicked.connect(self.encrypt)
        self.decryptB.clicked.connect(self.decrypt)   
        self.backButton.clicked.connect(self.goLand)
        self.genButton.clicked.connect(self.genKey)

    def genKey(self):
        nilaiP = self.nilaip.text()
        nilaiQ = self.nilaiq.text()
        generateKey(int(nilaiP),int(nilaiQ))
    def goLand(self):
        widget.setCurrentIndex(0) 
    def encryptFunction (self,M,e,n):
        t1 = process_time()
        Cipher = ''
        C = ''
        hasil = ''
        for i in range(len(M)//4):
            C = M[i*4:((i*4)+4)]
            hasil = (int(C)**e)%n
            if hasil < 10:
                Cipher = Cipher + '000' + str(hasil) + ' '
            elif hasil < 100:
                Cipher = Cipher + '00' + str(hasil) + ' '
            elif hasil < 1000:
                Cipher = Cipher + '0' + str(hasil) + ' '
            else:
                Cipher = Cipher + str(hasil) + ' '
        if (len(M)//4 != len(M)/4):
            C = M[(i*4)+4:(i*4)+6]
            hasil = (int(C)**e)%n
            if hasil < 10:
                Cipher = Cipher + '000' + str(hasil) + ' '
            elif hasil < 100:
                Cipher = Cipher + '00' + str(hasil) + ' '
            elif hasil < 1000:
                Cipher = Cipher + '0' + str(hasil) + ' '
            else:
                Cipher = Cipher + str(hasil) + ' '
        t2 = process_time()
        t = t2-t1
        # Cipher = hex(int(Cipher.replace(' ','')))
        file = open('HasilKonversiEncrypt.txt', 'w')
        # file.write(hex(int(Cipher.replace(' ',''))))
        file.write(Cipher)
        file.close()
        file_size = os.path.getsize('HasilKonversiEncrypt.txt')
        return Cipher, t, file_size
    def convertPlainText(self,m):
        m = m.replace(" ","")
        M = ''
        for i in range (len(m)):
            if ord(m[i])>90:
                concatM = ord(m[i])-97
            else:
                concatM =ord(m[i])-65
            if concatM > 9:
                M = M + str(concatM)
            else:
                M = M + '0' + str(concatM)
        return M
    def convertAngka (self,m):
        P = ''
        Teks = ''
        for i in range(len(m)//2):
            P = m[i*2:((i*2)+2)]
            Teks = Teks + str(chr(int(P)+65))
        return Teks   
    def decryptFunction (self,C,d,n):
        # C = int(C,16)
        t1 = process_time()
        C = str(C).replace(' ','')
        Plain = ''
        P = ''
        hasil = ''
        for i in range(len(C)//4):
            P = C[i*4:((i*4)+4)]
            hasil = (int(P)**d)%n
            if hasil < 10:
                Plain = Plain + '000' + str(hasil) 
            elif hasil < 100:
                Plain = Plain + '00' + str(hasil) 
            elif hasil < 1000:
                Plain = Plain + '0' + str(hasil) 
            else:
                Plain = Plain + str(hasil)
        t2 = process_time()
        t = t2-t1
        file = open('HasilKonversiDecrypt.txt', 'w')
        file.write(konversibase64(Plain))
        file.close()
        file_size = os.path.getsize('HasilKonversiDecrypt.txt')
        
        return Plain, t, file_size  
    
    def encrypt(self):
        nilaiP = self.nilaip.text()
        nilaiQ = self.nilaiq.text()
        M = self.convertPlainText(data)
        n = int(nilaiP) * int(nilaiQ)
        # e = generateKey(int(nilaiP),int(nilaiQ))[1]
        # with open 'PublicKey.pub' as pub:
        #    e = pub.read
        f = open("PublicKey.pub","r")
        e = int(f.read())
        hasilenkripsi = self.encryptFunction(M,e,n)
        plainteks = 'Plainteks: '  + str(data)
        cipherteks = 'Cipherteks: ' + str(hasilenkripsi[0])
        waktuEnkripsi = "%.5f" %hasilenkripsi[1]
        waktuproses = 'Waktu Proses: ' + waktuEnkripsi + ' s'
        ukuranfile = 'Ukuran File: ' + str(hasilenkripsi[2]) + ' bytes'
        self.hasil.setText(plainteks) 
        self.hasil_2.setText(cipherteks) 
        self.hasil_3.setText(waktuproses) 
        self.hasil_4.setText(ukuranfile) 
    
    def decrypt(self):
        nilaiP = self.nilaip.text()
        nilaiQ = self.nilaiq.text()
        f = open("PrivateKey.pri","r")
        d = int(f.read())
        global data
        data = str(data)
        if data[:2] == '0x':
            cipherteks = 'Cipherteks: ' + str(data)
            data = int(data,16)
        else:
            cipherteks = 'Cipherteks: ' + hex(int(data.replace(' ','')))
        
        # d = generateKey(int(nilaiP),int(nilaiQ))[0]
        n = int(nilaiP) * int(nilaiQ)
        plain = self.decryptFunction(data,d,n)
        plainteks = 'Plainteks: ' + str(self.convertAngka(plain[0])) #belomkonversi
        waktuDekripsi = "%.5f" %plain[1]
        waktuproses = 'Waktu Proses: ' + waktuDekripsi + ' s'
        ukuranfile = 'Ukuran File: ' + str(plain[2]) + ' bytes'
        self.hasil.setText(plainteks) 
        self.hasil_2.setText(cipherteks) 
        self.hasil_3.setText(waktuproses) 
        self.hasil_4.setText(ukuranfile) 

    def upload(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload File","","Text files (*.txt)")
        if fileName:
            global data
            self.uploadedFile = fileName
            self.fileName.setText(os.path.basename(fileName))
            with open(self.uploadedFile,'rt') as d:
                data = d.read()
        else:
            print("No file selected")  

class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('main.ui', self)
        self.uploadButton.clicked.connect(self.upload)
        self.uploadedFile = None 
        self.encryptB.clicked.connect(self.encrypt)
        self.decryptB.clicked.connect(self.decrypt)   
        self.backButton.clicked.connect(self.goLand)
        self.genButton.clicked.connect(self.genKey)

    def genKey(self):
        nilaiP = self.nilaip.text()
        nilaiQ = self.nilaiq.text()
        generateKey(int(nilaiP),int(nilaiQ))

    def goLand(self):
        widget.setCurrentIndex(0) 
    
    def encrypt(self):
        nilaiP = self.nilaip.text()
        nilaiQ = self.nilaiq.text()
        M = konversiASCII(teks)
        n = int(nilaiP) * int(nilaiQ)
        e = generateKey(int(nilaiP),int(nilaiQ))[1]
        hasilenkripsi = encryptFunction(M,e,n)
        plainteks = 'Plainteks: '  + str(teks)
        ciper = konversiHex(hasilenkripsi[0])
        print(ciper)
        cipherteks = 'Cipherteks: ' + str(ciper)
        waktuEnkripsi = "%.5f" %hasilenkripsi[1]
        waktuproses = 'Waktu Proses: ' + waktuEnkripsi + ' s'
        ukuranfile = 'Ukuran File: ' + str(hasilenkripsi[2]) + ' bytes'
        self.hasil.setText(plainteks) 
        self.hasil_2.setText(cipherteks)
        self.hasil_3.setText(waktuproses) 
        self.hasil_4.setText(ukuranfile) 

    def decrypt(self):
        with open(self.uploadedFile,'rt') as d:
            data = d.read()
        nilaiP = self.nilaip.text()
        nilaiQ = self.nilaiq.text()
        f = open("PrivateKey.pri","r")
        d = int(f.read())
        global teks
        teks = str(konversibase64(data))
        data = data.replace(" ","")
        cipherteks = 'Cipherteks: ' + str(konversiHex(int(data)))
        n = int(nilaiP) * int(nilaiQ)
        plain = decryptFunction(data,d,n)
        plainT = konversibase64(plain[0])
        plainteks = 'Plainteks: ' + str(plainT) #belomkonversi
        print(konversibase64(plain[0]))
        waktuDekripsi = "%.5f" %plain[1]
        waktuproses = 'Waktu Proses: ' + waktuDekripsi + ' s'
        ukuranfile = 'Ukuran File: ' + str(plain[2]) + ' bytes'
        self.hasil.setText(plainteks) 
        # print(cipherteks)
        self.hasil_2.setText(cipherteks)
        self.hasil_3.setText(waktuproses) 
        self.hasil_4.setText(ukuranfile) 

    def upload(self):
        global teks
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Upload File", "")
        if fileName:
            self.uploadedFile = fileName
            self.fileName.setText(os.path.basename(fileName))
            with open(self.uploadedFile,'rb') as d:
                bytesData = d.read()
                b64content = base64.b64encode(bytesData)
                teks = b64content.decode('utf-8')
        else:
            print("No file selected")  


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.addWidget(Landing())
widget.addWidget(Main())  
widget.addWidget(Text())
widget.setCurrentIndex(0)
widget.setFixedWidth(780)
widget.setFixedHeight(319)
widget.show()
app.exec_()