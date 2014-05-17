from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    nigeriacoin=math.Object(
        PARENT=networks.nets['nigeriacoin'],
        SHARE_PERIOD=12, # seconds
        CHAIN_LENGTH=24*60*60//12, # shares
        REAL_CHAIN_LENGTH=24*60*60//12, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=15, # blocks
        IDENTIFIER='9323e43a6805a417'.decode('hex'),
        PREFIX='af69020acd611ac0'.decode('hex'),
        P2P_PORT=9557,
        MIN_TARGET=16,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=9556,
        BOOTSTRAP_ADDRS=''.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-ngc',
        VERSION_CHECK=lambda v: v >= 90000,
        VERSION_WARNING=lambda v: 'Upgrade Nigeriacoin to >=0.9.0!' if v < 90000 else None,
    ),
    skeincoin=math.Object(
        PARENT=networks.nets['skeincoin'],
        SHARE_PERIOD=12, # seconds
        CHAIN_LENGTH=24*60*60//12, # shares
        REAL_CHAIN_LENGTH=24*60*60//12, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=15, # blocks
        IDENTIFIER='f134a62e7cee0cab'.decode('hex'),
        PREFIX='9030d1a8f32a9d55'.decode('hex'),
        P2P_PORT=19230,
        MIN_TARGET=16,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=18230,
        BOOTSTRAP_ADDRS=''.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-skc',
        VERSION_CHECK=lambda v: v >= 80600,
        VERSION_WARNING=lambda v: 'Upgrade Skeincoin to >=0.8.6!' if v < 80600 else None,
    )
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
