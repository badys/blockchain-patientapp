import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
import solcx


def compile_contract():
    with open('docmed.sol', 'r') as f:
        source = f.read()
        return solcx.compile_source(source)


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
w3.eth.defaultAccount = w3.eth.accounts[0]

docmed = compile_contract().pop("<stdin>:DocMed")
ABI = docmed['abi']

# Instantiate and deploy contract
contract = w3.eth.contract(
    abi=ABI,
    bytecode=docmed['bin']
)
# Get transaction hash from deployed contract
tx_hash = contract.constructor().transact()
# Get tx receipt to get contract address
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
ADDRESS = tx_receipt['contractAddress']

doctors = []
patients = []
password = "qwe123"
for i in range(5):
    acc = w3.personal.newAccount(password)
    doctors.append(acc)
    w3.personal.unlockAccount(acc, password, 0)
    print('Created and unlocked Doctor nr %d, address: %s' % (i + 1, acc))
    acc = w3.personal.newAccount(password)
    patients.append(acc)
    w3.personal.unlockAccount(acc, password, 0)
    print('Created and unlocked Patient nr %d, address: %s' % (i + 1, acc))

with open('data.json', 'w') as out:
    data = {
        "abi": ABI,
        "address": ADDRESS,
        "doctors": doctors,
        "patients": patients
    }
    json.dump(data, out, indent=4, sort_keys=True)
print('Contract compiled')
