from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import MD5
from Crypto.Signature import pkcs1_15
import json
import os
from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import urlencode
import socket
import uuid

def get_mac_address():
        mac_num = uuid.getnode()
        mac = ':'.join(['{:02x}'.format((mac_num >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])
        return mac
class Client():
    def __init__(self, username, serialNumber):
        self.serverUrl = "http://localhost:5000/verify"
        self.publickeyPath = "public.pem"
        self.licensePath = "license.txt"
        self.username = username
        self.serialNumber = serialNumber
        self.MAC = get_mac_address()
    
    def create_signature(self):
        return "{}${}${}".format(self.username, self.serialNumber, self.MAC)

    def encrypt_message(self, message):
        public_key = RSA.import_key(open(self.publickeyPath).read())
        cipher_rsa = PKCS1_OAEP.new(public_key)
        return cipher_rsa.encrypt(message.encode('utf-8'))

    def secure_license(self):
        print("LicenseManager service started...")
        message = self.create_signature()
        encrypted_message = self.encrypt_message(message)
        print(f"Client -- Encrypted License Text: {encrypted_message.hex()}")
        data = json.dumps({"encrypted_message": encrypted_message.hex()}).encode('utf-8')
        req = Request(self.serverUrl, data, headers={'Content-Type': 'application/json'})
        try:
            with urlopen(req) as response:
                response_data = response.read()
                signature = json.loads(response_data)['signature']
                print(f"Server -- Digital Signature: {signature}")
                with open(self.licensePath, 'w') as f:
                    f.write(signature)
                print("Succeed. The license file content is secured and signed by the server.")
        except URLError as e:
            print(f"Client -- Failed to obtain license: {e.reason}")

    def verify_signature(self, signature):
        message = self.create_signature()
        public_key = RSA.import_key(open(self.publickeyPath).read())
        hash_object = MD5.new(message.encode('utf-8'))
        try:
            pkcs1_15.new(public_key).verify(hash_object, bytes.fromhex(signature))
            return True
        except (ValueError, TypeError):
            return False

    def run(self):
        if os.path.exists(self.licensePath):
            with open(self.licensePath, 'r') as f:
                existing_signature = f.read()
            if self.verify_signature(existing_signature):
                print("License is correct.")
            else:
                print("The license file has been broken!!")
                self.secure_license()
        else:
            self.secure_license()

if __name__ == "__main__":
    username = "bora"
    serialNumber = "1234-4093-2200"
    client = Client(username, serialNumber)
    client.run()