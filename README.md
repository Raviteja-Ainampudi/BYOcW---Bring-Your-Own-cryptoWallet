
# Crypto Wallet Generator

A Dockerized multi-currency crypto wallet generator with support for Ethereum and Bitcoin. The application provides an API to generate wallets, securely store encrypted private keys, and create QR codes for wallet addresses.

---

## **Features**
1. **Multi-Currency Support**:
   - Ethereum
   - Bitcoin

2. **Secure Key Storage**:
   - Private keys are encrypted and stored securely in the `wallets/` directory.

3. **QR Code Generation**:
   - QR codes for wallet addresses are generated and saved in the `wallets/` directory.

4. **REST API**:
   - Simple API to create and retrieve wallet details.

5. **Dockerized**:
   - Fully containerized for ease of deployment and security.

---

## **Directory Structure**
```
crypto-wallet/
├── Dockerfile                 # Docker configuration file
├── requirements.txt           # Python dependencies
└── app/
    ├── wallet_generator.py    # Wallet creation logic for Ethereum and Bitcoin
    ├── api.py                 # REST API implementation
    ├── utils.py               # Utility functions (encryption, QR code generation)
    └── wallets/               # Directory to store generated keys and QR codes
```

---

## **Getting Started**

### **Prerequisites**
1. Install [Docker](https://docs.docker.com/get-docker/).

---

### **Installation**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd BYOcW - Bring Your Own cryptoWallet
   ```

2. Build the Docker image:
   ```bash
   docker build -t BYOcW - Bring Your Own cryptoWallet .
   ```

---

### **Usage**

#### **Run the Application**
Start the application by running the Docker container:
```bash
docker run --rm -p 5000:5000 -v $(pwd)/app/wallets:/app/wallets BYOcW - Bring Your Own cryptoWallet
```

The application will run on [http://localhost:5000](http://localhost:5000).

---

#### **API Endpoints**

##### **1. Create an Ethereum Wallet**
**Request**:
```bash
GET /create_wallet/ethereum
```

**Example**:
```bash
curl http://localhost:5000/create_wallet/ethereum
```

**Response**:
```json
{
  "currency": "Ethereum",
  "address": "0x1234abcd5678ef...",
  "encrypted_private_key": "wallets/0x1234abcd5678ef..._private.enc",
  "qr_code": "wallets/0x1234abcd5678ef....png"
}
```

---

##### **2. Create a Bitcoin Wallet**
**Request**:
```bash
GET /create_wallet/bitcoin
```

**Example**:
```bash
curl http://localhost:5000/create_wallet/bitcoin
```

**Response**:
```json
{
  "currency": "Bitcoin",
  "address": "bc1qxyz123abc...",
  "encrypted_private_key": "wallets/bc1qxyz123abc..._private.enc",
  "qr_code": "wallets/bc1qxyz123abc...png"
}
```

---

## **Wallet Details**

1. **Encrypted Private Key**:
   - Private keys are securely stored in the `wallets/` directory with `.enc` extension.
   - Example: `wallets/0x1234abcd5678ef..._private.enc`

2. **QR Codes**:
   - QR codes for wallet addresses are saved as `.png` files in the `wallets/` directory.
   - Example: `wallets/0x1234abcd5678ef...png`

---

## **Development**

### **Code Overview**

#### **`wallet_generator.py`**
- Contains functions to generate Ethereum and Bitcoin wallets.

#### **`utils.py`**
- Utility functions for:
  - Encrypting private keys.
  - Generating QR codes for wallet addresses.

#### **`api.py`**
- Implements the Flask REST API.

---

### **Extend the Project**

1. **Add More Cryptocurrencies**:
   - Extend `wallet_generator.py` to include other blockchains (e.g., Litecoin, Dogecoin).

2. **Add Transaction Signing**:
   - Implement transaction signing and broadcasting for Bitcoin and Ethereum.

3. **Build a Frontend**:
   - Add a React or Vue.js frontend for user-friendly interaction.

4. **Deploy to Cloud**:
   - Deploy the container to a cloud service like AWS, Azure, or GCP for public access.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Contributing**
Contributions are welcome! Feel free to submit issues or pull requests.

---

## **Contact**
For any questions or feedback, please contact:
- **LinkedIn**: [ https://www.linkedin.com/in/ainampudiraviteja ]
- **GitHub**: [https://github.com/Raviteja-Ainampudi/]

---

Enjoy your secure and flexible crypto wallet generator! 🚀
