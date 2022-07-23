# INTERNET LIBRARIES
import urllib.request
import urllib.error
from machine import UART, Pin

##BITCOIN LIBRARIES
from embit import bip32, bip39
from embit.psbt import PSBT
from embit.descriptor import Descriptor

## LOGGING LIBRARIES 
from binascii import hexlify
import utime,time

##WIFI LOGIN INFORMATION
SSID='XXX'
password = 'XXX'
ServerIP = 'XXX'

##RASPBERRY PI CONNECTION INFORMATION
Port = '442'
uart = UART(0, 115200)

# 5 STEP BITCOIN MINING PROCESS
#-------------------------------------------------------
#- 1 CONNECT TO INTERNET
#- 2 GENERATE BITCOIN ADDRESS
#- 3 SEND BITCOIN ADDRESS TO LAPTOP MINER
#- 4 LAPTOP MINER CONSTRUCTS BLOCK HEADER
#- 5 LAPTOP MINER MINES BITCOIN
#-------------------------------------------------------

## STEP 1 - CONNECT TO INTERNET
def sendCMD(cmd,ack,timeout=2000):
    uart.write(cmd+'\r\n')
    t = utime.ticks_ms()
    while (utime.ticks_ms() - t) < timeout:
        s=uart.read()
        if(s != None):
            s=s.decode()
            print(s)
            if(s.find(ack) >= 0):
                return True
    return False

##PRINT OUT SUCCESSFULL WIFI CONNECTION
uart.write('+++')
time.sleep(1)
if(uart.any()>0):uart.read()
#Test if AT system works correctly
sendCMD("AT","OK")
##Set AP’s info which will be connect by ESP8266, 3= host and client 
sendCMD("AT+CWMODE=3","OK")
##Commands ESP8266 to connect a SSID with supplied password.
sendCMD("AT+CWJAP=\""+SSID+"\",\""+password+"\"","OK",20000)
##Get local IP address.
sendCMD("AT+CIFSR","OK")
#Start a connection as client. (Single connection mode)
sendCMD("AT+CIPSTART=\"TCP\",\""+ServerIP+"\","+Port,"OK",10000)

## STEP 2 - GENERATE BITCOIN ADDRESS

# Generate mnemonic from 16 bytes of entropy (use real entropy here!):
mnemonic = bip39.mnemonic_from_bytes(b"128 bits is fine")
# >>> couple mushroom amount shadow nuclear define like common call crew fortune slice

# Generate root privkey, password can be omitted if you don't want it
seed = bip39.mnemonic_to_seed(mnemonic, password="my bip39 password")
root = bip32.HDKey.from_seed(seed)

# Derive and convert to pubkey
xpub = root.derive("m/84h/0h/0h").to_public()

#- STEP 3 SEND BITCOIN ADDRESS TO LAPTOP MINER

def send_address(url):
    while True:
        try:
            conn = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            # Email admin / log
            print(f'HTTPError: {e.code} for {url}')
        except urllib.error.URLError as e:
            # Email admin / log
            print(f'URLError: {e.code} for {url}')
        else:
            # Website is up
            print(f'{url} is up')
            data = parse.urlencode(xpub.encode() + root.encode())
            req =  request.Request(<your url>, data=data) # this will make the method "POST"
            resp = request.urlopen(req)
            time.sleep(60)
        

send_address("localhost:3000")

## STEPS 4 AND 5 ARE CONTINUED ON GITHUB AT https://github.com/jgarzik/pyminer
#----------------------------------------------
# STEP - 4 LAPTOP MINER CONSTRUCTS BLOCK HEADER
# STEP - 5 LAPTOP MINER MINES BITCOIN

