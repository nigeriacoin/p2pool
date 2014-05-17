import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    nigeriacoin=math.Object(
        P2P_PREFIX='2f232c25'.decode('hex'),
        P2P_PORT=3557,
        ADDRESS_VERSION=53,
        RPC_PORT=3556,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            "nigeriacoinaddress" in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 41900*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('skeinhash').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='NGC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Nigeriacoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Nigeriacoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.nigeriacoin'), 'nigeriacoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://explorer.nigeriacoin.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://explorer.nigeriacoin.org/address/',
        TX_EXPLORER_URL_PREFIX='https://explorer.nigeriacoin.org/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.01e8,
    ),
    skeincoin=math.Object(
        P2P_PREFIX='f726a1bf'.decode('hex'),
        P2P_PORT=11230,
        ADDRESS_VERSION=63,
        RPC_PORT=21230,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            "skeincoinaddress" in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 10000 if height < 100 else max((32*int(1e8))>> (height + 1)//262800, 10000),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('skeinhash').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='SKC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Skeincoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Skeincoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.skeincoin'), 'skeincoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://explorer.skeincoin.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://explorer.skeincoin.org/address/',
        TX_EXPLORER_URL_PREFIX='https://explorer.skeincoin.org/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    )

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
