# Clinical Trials Management System

This project demonstrates a clinical trials management system using both private blockchain (Hyperledger Fabric) and public blockchain (Ethereum). It allows users to create, read, update, and delete clinical trial records and compares the performance (throughput and latency) of the two blockchain platforms.

## Project Overview

The system provides a web interface for managing clinical trials and interacts with both Hyperledger Fabric and Ethereum blockchain networks. It also includes functionality to compare the performance of the two blockchains.

## Features

- Create clinical trial records
- Read clinical trial details
- Update clinical trial information
- Delete clinical trial records
- Compare performance between Hyperledger Fabric and Ethereum

## Tech Stack

- **Frontend**: HTML, Bootstrap, JavaScript, jQuery
- **Backend**: Flask (Python)
- **Blockchain**:
  - Hyperledger Fabric (Private Blockchain)
  - Ethereum (Public Blockchain)

## Prerequisites

- Docker and Docker Compose
- Node.js and npm
- Python and pip
- Hyperledger Fabric binaries and images
- Truffle and Ganache CLI for Ethereum

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/clinical-trials-management.git
cd clinical-trials-management
```

### 2. Set Up Hyperledger Fabric

```sh
cd fabric-network
curl -sSL https://bit.ly/2ysbOFE | bash -s
cd fabric-samples/test-network
./network.sh up createChannel -c mychannel -ca
./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-go -ccl go
```

### 3. Set Up Ethereum

```sh
cd eth-contracts
truffle compile
truffle migrate --network development
```

### 4. Set Up Flask Application

```sh
cd flask-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Start Flask Server

```sh
cd flask-app
flask run
```

### Access the Application

Navigate to `http://127.0.0.1:5000` in your web browser.

### Performance Comparison

Click on the "Compare Performance" button in the web interface to generate a performance comparison chart between Hyperledger Fabric and Ethereum.

## Endpoints

- **`/fabric/clinical-trial`** (POST): Create a clinical trial on Hyperledger Fabric
- **`/ethereum/clinical-trial`** (POST): Create a clinical trial on Ethereum
- **`/compare`** (GET): Compare the performance of both blockchains

## Performance Comparison

The comparison results are saved as performance_comparison.png and displayed in the web interface. It compares the throughput and latency of Hyperledger Fabric and Ethereum based on user interactions.

created by team codex..

