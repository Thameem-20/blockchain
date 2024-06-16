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
    #to create clinical trial in Hyperledger Fabric
    pass

@app.route('/ethereum/clinical-trial', methods=['POST'])
def create_ethereum_clinical_trial():
    #to create clinical trial in Ethereum
    pass

@app.route('/compare', methods=['GET'])
def compare():
    #to compare performance and generate the plot
    fabric_results = {'throughput': 100, 'latency': 1}
    ethereum_results = {'throughput': 50, 'latency': 5}
    
    plot_comparison(fabric_results, ethereum_results)
    
    return jsonify({"message": "Comparison done, check performance_comparison.png"})

if __name__ == '__main__':
    app.run(debug=True)
