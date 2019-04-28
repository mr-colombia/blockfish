# import BigchainDB and create an object
from bigchaindb_driver import BigchainDB
bdb_root_url = 'https://test.bigchaindb.com'
bdb = BigchainDB(bdb_root_url)

# generate a keypair
from bigchaindb_driver.crypto import generate_keypair
alice, bob = generate_keypair(), generate_keypair()

# create a digital asset for Alice
game_boy_token = {
    'data': {
        'token_for': {
            'game_boy': {
                'serial_number': 'LR35902'
            }
        },
        'description': 'Time share token. Each token equals one hour of usage.',
    },
}

# prepare the transaction with the digital asset and issue 10 tokens for Bob
prepared_token_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    recipients=[([bob.public_key], 10)],
    asset=game_boy_token)

# fulfill and send the transaction
fulfilled_token_tx = bdb.transactions.fulfill(
    prepared_token_tx,
    private_keys=alice.private_key)
bdb.transactions.send_commit(fulfilled_token_tx)

# Use the tokens
# create the output and inout for the transaction
transfer_asset = {'id': fulfilled_token_tx['id']}
output_index = 0
output = fulfilled_token_tx['outputs'][output_index]
transfer_input = {'fulfillment': output['condition']['details'],
                  'fulfills': {'output_index': output_index,
                               'transaction_id': transfer_asset['id']},
                  'owners_before': output['public_keys']}

# prepare the transaction and use 3 tokens
prepared_transfer_tx = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=transfer_asset,
    inputs=transfer_input,
    recipients=[([alice.public_key], 3), ([bob.public_key], 7)])

# fulfill and send the transaction
fulfilled_transfer_tx = bdb.transactions.fulfill(
    prepared_transfer_tx,
    private_keys=bob.private_key)
sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
print(sent_transfer_tx)
