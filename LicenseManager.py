from flask import Flask, request, jsonify
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import MD5
from Crypto.Signature import pkcs1_15
privKeyPath = "private.pem" 
publicKeyPath = "public.pem"

app = Flask(__name__)

@app.route("/verify", methods=['POST'])
def verify():
    print("Server -- Server is being requested...")
    encrypted_msg = request.json['encrypted_message']
    print(f"Server -- Incoming Encrypted Text: {encrypted_msg}")
    private_key = RSA.import_key(open(privKeyPath).read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher_rsa.decrypt(bytes.fromhex(encrypted_msg))
    print(f"Server -- Decrypted Text: {decrypted_message}")
    
    # MD5 hash
    hash_object = MD5.new(decrypted_message)
    
    # signing with private key
    signature = pkcs1_15.new(private_key).sign(hash_object)
    print(f"Server -- MD5 Plain License Text: {hash_object.hexdigest()}")
    print(f"Server -- Digital Signature: {signature.hex()}")
    return jsonify({"signature": signature.hex()}), 200
@app.route("/")
def running():
    return "<p>Server is running</p>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
