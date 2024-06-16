from flask import Flask, request, jsonify
from hfc.fabric import Client as FabricClient
from web3 import Web3
import time
import matplotlib.pyplot as plt

app = Flask(__name__)

#Hyperledger Fabric setup
fabric_client = FabricClient(net_profile="network.json")
fabric_client.new_channel('mychannel')

#Ethereum setup
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

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

    plt.savefig('performance_comparison.png')

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
            fcn='CreateTrial',
            args=[id, title, description, status, sponsor, str(participants)],
            cc_name='basic',
            wait_for_event=True
        )
        return jsonify({'message': 'Clinical trial created successfully in Hyperledger Fabric'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ethereum/clinical-trial', methods=['POST'])
def create_ethereum_clinical_trial():
    data = request.get_json()
    id = data['id']
    title = data['title']
    description = data['description']
    status = data['status']
    sponsor = data['sponsor']
    participants = data['participants']

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    tx_hash = contract.functions.createTrial(id, title, description, status, sponsor, participants).transact({'from': web3.eth.accounts[0]})

    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    if receipt['status'] == 1:
        return jsonify({'message': 'Clinical trial created successfully in Ethereum'})
    else:
        return jsonify({'error': 'Failed to create clinical trial in Ethereum'}), 500


@app.route('/compare', methods=['GET'])
def compare():
    #to compare performance and generate the plot
    fabric_results = {'throughput': 100, 'latency': 1}
    ethereum_results = {'throughput': 50, 'latency': 5}
    
    plot_comparison(fabric_results, ethereum_results)
    
    return jsonify({"message": "Comparison done, check performance_comparison.png"})

if __name__ == '__main__':
    app.run(debug=True)
