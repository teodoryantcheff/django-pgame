from pprint import pprint
import timeit
# import dogecoinrpc
from datetime import datetime
import sys


from django.conf import settings
settings.configure()

# rpc_user and rpc_password are set in the bitcoin.conf file
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:44555" % ('dogecoinrpc', 'CRP3FXKN847tXbVNiQ3nAh2A6tjRSJMFzqLUic3EnnGs'))
print rpc_connection.listreceivedbyaccount()

for t in rpc_connection.listtransactions():
    pprint(t)
# print [t['category'] for t in ts]

sys.exit()


a = [
    'D7NS6tGNifYLprFay4BZzwgAVbdKZ9VY38',
    'DGRE7ojuB1VcmF1iVJKy2UkVUk3efd2Dge',
    'DUJRzaSofMtnUFcExZW5ZYCDfaFbcsrT4r',
    'D9DWEdAN4rZhrQ1n6b7eyX1C92EGbsNuiY',
    'DFoESHDGULq6nyuT3i7zzGKNF3uAECw1vB',
    'D9ckkRQGvRgNbmmDaR3dE4xArhF4Wj6R3o',
    'DJQydF58ZMrvrQGjLbpNh4VNJBNrN58KaC',
    'DK6QeNmT87qXXdqkP5AG4ZXwsiCw1PJzDt',
    'DTrs5KX2SG5NDGuhJDXus5DC3mV6yzRu6w',
    'D74vyQxi5wZZ71yKeooAbBTYASEDjjcick',
]

conn = dogecoinrpc.connect_to_local('d:\\doge\\rpc.conf')

# print "Your balance is %f" % (conn.getbalance(),)
# print conn.validateaddress('DTZJ9v9rCpWaDUtzpfREMLRcLfJHxZQnvT')
# print conn.getconnectioncount()

# start = datetime.now()
# for i in xrange(11524, 12000):
#     name = 'account_{:05d}'.format(i)
#     pay_to = conn.getnewaddress(account=name)
#     print name, pay_to
# print (datetime.now() - start).total_seconds()

# conn.sendtoaddress('D74vyQxi5wZZ71yKeooAbBTYASEDjjcick', 15, 'comment', 'comment_to')

# print 'received', conn.getreceivedbyaddress('D74vyQxi5wZZ71yKeooAbBTYASEDjjcick')
# print conn.getreceivedbyaccount('default')
# #print 'received', conn.getreceivedbyaccount('rrr')
#
# conn.move('rrr', 'default', 25, comment='test move')
# print conn.getreceivedbyaccount('rrr')

# print conn.getaccountaddress('default')
# print conn.getaccountaddress('rrr')
# print conn.getaccount('D74vyQxi5wZZ71yKeooAbBTYASEDjjcick')

# pprint( conn.listreceivedbyaddress(includeempty=True))


from django.utils.crypto import get_random_string

print timeit.repeat(
    stmt='get_random_string()',
    setup='from django.utils.crypto import get_random_string',
    number=10000,
    repeat=3
)

sys.exit()

pprint(conn.listaccounts(as_dict=True))
print conn.getbalance()

pprint(conn.validateaddress('DRiKDaC7wxmBqAqRjS3ebkDpWyj8CjBYRN'))


# start = datetime.now()
# for i in xrange(1, 12000):
#     account = 'account_{:05d}'.format(i)
#     balance = conn.getbalance(account=account)
#     print account, conn.getaccountaddress(account), balance
# print (datetime.now() - start).total_seconds()