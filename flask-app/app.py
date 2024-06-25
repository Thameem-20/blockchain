from flask import Flask, request, jsonify, send_from_directory, render_template, request, redirect
from hfc.fabric import Client as FabricClient
from web3 import Web3
import matplotlib.pyplot as plt
import os

# Flask app setup
app = Flask(__name__)

# Ethereum setup
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
contract_address = "0xbeAeD27Bd521dc8BD24580eC73B2d4b26E7291C4"  # Replace with your deployed contract address
contract_abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "string",
				"name": "id",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "title",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "status",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "sponsor",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "participants",
				"type": "uint256"
			}
		],
		"name": "TrialCreated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "string",
				"name": "id",
				"type": "string"
			}
		],
		"name": "TrialDeleted",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "string",
				"name": "id",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "title",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "status",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "sponsor",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "participants",
				"type": "uint256"
			}
		],
		"name": "TrialUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "id",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "title",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "status",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "sponsor",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "participants",
				"type": "uint256"
			}
		],
		"name": "createTrial",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "id",
				"type": "string"
			}
		],
		"name": "deleteTrial",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "id",
				"type": "string"
			}
		],
		"name": "readTrial",
		"outputs": [
			{
				"internalType": "string",
				"name": "title",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "status",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "sponsor",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "participants",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "id",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "title",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "status",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "sponsor",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "participants",
				"type": "uint256"
			}
		],
		"name": "updateTrial",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

@app.route('/')
def index():
    return render_template('index.html')

# Load contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Hyperledger Fabric setup
fabric_client = FabricClient(net_profile="network.json")
fabric_client.new_channel('mychannel')

def plot_comparison(fabric_results, ethereum_results):
    labels = ['Throughput', 'Latency']
    fabric_means = [fabric_results['throughput'], fabric_results['latency']]
    ethereum_means = [ethereum_results['throughput'], ethereum_results['latency']]

    x = range(len(labels))

    fig, ax = plt.subplots()
    ax.bar(x, fabric_means, width=0.4, label='Hyperledger Fabric', align='center')
    ax.bar(x, ethereum_means, width=0.4, label='Ethereum', align='edge')

    ax.set_ylabel('Performance')
    ax.set_title('Performance comparison between Hyperledger Fabric and Ethereum')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Ensure the 'static' directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    # Save the plot to a file
    plt.savefig('static/performance_comparison.png')

@app.route('/fabric/clinical-trial', methods=['POST'])
def create_fabric_clinical_trial():
    data = request.get_json()
    id = data['id']
    title = data['title']
    description = data['description']
    status = data['status']
    sponsor = data['sponsor']
    participants = data['participants']

    try:
        fabric_client.chaincode_invoke(
            requestor='admin',
            channel_name='mychannel',
            peer_names=['peer0.org1.example.com'],
            fcn='createTrial',  # Ensure correct case for chaincode function name
            args=[id, title, description, status, sponsor, str(participants)],
            cc_name='basic',
            wait_for_event=True
        )
        return jsonify({'message': 'Clinical trial created successfully in Hyperledger Fabric'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ethereum/clinical-trial', methods=['POST'])
def create_clinical_trial_ethereum():
    data = request.json
    account = web3.eth.accounts[0]
    txn = contract.functions.createTrial(
        data['id'],
        data['title'],
        data['description'],
        data['status'],
        data['sponsor'],
        data['participants']
    ).buildTransaction({
        'from': account,
        'nonce': web3.eth.getTransactionCount(account),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei')
    })
    signed_txn = web3.eth.account.signTransaction(txn, private_key='0x64c9886aa6cbce6d408db7a2dca5f8a69473179820d0296be2ea690a0c098791')  # Replace with account 0 private key
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return jsonify({'transactionHash': receipt.transactionHash.hex()})

@app.route('/compare', methods=['GET'])
def compare():
    # Dummy data for comparison
    fabric_results = {'throughput': 100, 'latency': 1}
    ethereum_results = {'throughput': 50, 'latency': 5}
    
    plot_comparison(fabric_results, ethereum_results)
    
    return jsonify({"message": "Comparison done, check performance_comparison.png"})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
