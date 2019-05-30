# blockchain-patientapp
Simple dapp using Ethereum

# Geth node setup
To start private go-ethereum node type the given command where `--datadir` is your choosen ethereum data directory, `--bootnodes` points to always-on node running the same network that is setup on Microsoft Azure cloud service, `--networkid 101010101` specifies network that this node will join and finally `console` will drop interactive JS console after successfull geth node setup.

Genesis.json is descriptor of genesis block for this blockchain network and has to be the same for all nodes joining the network.

### Init command:
`geth --datadir datadir init genesis.json`

### Start command:
`geth --datadir datadir --bootnodes enode://eaba0a6354c4d36377ba0e7b80886644e27d532da3b98ece22a1858f7bcc3c90bb40063eafe23c6b895cd964c736832e1340f1da506c771d732d93480b3e3968@40.68.74.219:30303 --networkid 101010101 console`

# Local test
### geth
Start geth using 'geth --dev console --rpc --rpcapi="db,eth,net,web3,personal,web3"'
Be sure to check if HTTP endpoint from geth matches address in both compile.py and app.py

### Start
First execute compile.py, it also create 5 addresses for patients and doctors.
Then execute app.py.
