# blockchain-patientapp
Simple dapp using Ethereum

# Geth node setup
To start private go-ethereum node type the given command where `--datadir` is your choosen ethereum data directory, `--bootnodes` points to always-on node running the same network that is setup on Microsoft Azure cloud service, `--networkid 101010101` specifies network that this node will join and finally `console` will drop interactive JS console after successfull geth node setup.

Genesis.json is descriptor of genesis block for this blockchain network and has to be the same for all nodes joining the network.

### Init command:
`geth --datadir datadir init genesis.json`

### Start command:
`geth --datadir datadir --bootnodes enode://e85024e6d15fe94372e77356e66f3866e80e8a96b67be54ceeeec3388d5e5654e4514b4c14ef43d1f11fdd281ab8aa5ab5e5581ebdb30f3f0dd78b99b90b3ab0@40.68.74.219:30303 --networkid 101010101 console`