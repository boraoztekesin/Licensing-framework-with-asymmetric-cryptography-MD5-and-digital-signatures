# Licensing-framework-with-asymmetric-cryptography-MD5-and-digital-signatures
## Introduction
This report outlines the development process of a licensing framework for a software project. The aim was to utilize asymmetric cryptography, the MD5 hashing algorithm, and digital signatures to create a secure and reliable licensing module. The framework is designed to handle the licensing process via two main Python scripts: `Client.py` and `LicenseManager.py`.

## Implementation Details
The implementation is based on the requirements provided through our instructor, where `public.pem` and `private.pem` keys were given. The `Client.py` serves as the client module holding the public key, while `LicenseManager.py` accesses both the public and private keys to enable encryption and decryption.

## System Design
### 1. Client Module:
- **Initialization (`__init__` Method)**: Configures the client with the username, serial number, and dynamically retrieved MAC address. The MAC address is obtained using the `uuid` library, ensuring each client instance has a unique identifier.
- **Signature Creation (`create_signature` Method)**: Concatenates the username, serial number, and MAC address into a unique string, separated by $. This string forms the raw license text.
- **Encryption (`encrypt_message` Method)**: Encrypts the raw license text using the public key and RSA algorithm.
- **License Acquisition (`secure_license` Method)**: Sends the encrypted license text to the server and handles the response, which includes the digital signature. Upon successful verification, it writes the signature to `license.txt`.

### 2. LicenseManager Module:
- **Verification**: Upon receiving the encrypted data, the server decrypts the message using its private key.
- **Hashing**: An MD5 hash of the decrypted text is generated.
- **Signing**: The hash is then signed with the private key, creating a digital signature.
- **Response**: This signature is sent back to the client for verification.

## Testing & Results
The system was tested to ensure reliability under various conditions, including the absence of the `license.txt` file, verifying an existing license, and handling a corrupted license file. The tests confirmed the robustness of the encryption, decryption, and signature verification mechanisms.

## Functionality Overview
- **Dynamic MAC Address Retrieval**: `get_mac_address` function dynamically retrieves the MAC address of the host machine, ensuring that each license is unique to the device.
- **Encryption & Decryption**: Utilizes RSA encryption to secure the license information, making it accessible only to the designated server and client.
- **Digital Signature Creation & Verification**: Ensures the integrity and authenticity of the license information, preventing unauthorized modifications.
