from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
 
alice = generate_keypair()
bdb = BigchainDB('https://test.bigchaindb.com')


def createTransaction(bdb, alice, site_asset, metadata):
 
    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=alice.public_key,
        asset=site_asset,
        metadata=site_asset_metadata
    )
    
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=alice.private_key
    )
    
    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
    
    txid = fulfilled_creation_tx['id']
    print(txid)
    print(sent_creation_tx)


site_asset = {
    'data': {
        'website': {
            'url': 'facebook.com',
            'ip': '66.220.159.255'
        },
    },
}
site_asset2 = {
    'data': {
        'website': {
            'url': 'google.com',
            'ip': '8.8.4.4'
        },
    },
}

site_asset_metadata = {
    'planet': 'earth'
}


createTransaction(bdb, alice, site_asset, site_asset_metadata)
createTransaction(bdb, alice, site_asset2, site_asset_metadata)
print(bdb.assets.get(search='8.8.8.4',limit=1), "\n")
print(bdb.assets.get(search='66.220.159.255',limit=1), "\n")
print(bdb.assets.get(search='google.com',limit=1),"\n")
print(bdb.metadata.get(search='google.com',limit=1))

