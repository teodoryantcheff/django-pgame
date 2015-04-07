# coding=utf-8
import socket
import sys
import logging
from decimal import Decimal
from time import sleep

import django
from django.contrib.auth import get_user_model
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pgame.settings")
# settings.configure()
from django.conf import settings
django.setup()

from pgameapp.models import CryptoTransaction, GameConfiguration
from pgameapp.models.wallet import BlockProcessingHistory
from pgameapp.services import apply_payment

import wallet

__author__ = 'Jailbreaker'

logger = logging.getLogger(__name__)


MIN_TX_CONFIRMATIONS = 1
SLEEP_TIME = 5

TX_CAT_TO_CHAR = {
    "send": 'S',
    "receive": 'R',
    "move": 'M',
    "orphan": 'O',
    "immature": 'I',
    "generate": 'G'
}


User = get_user_model()


def main():
    w = AuthServiceProxy(wallet.CRYPTO_WALLET_CONNSTRING)
    logger.debug('test', wallet)
    try:
        last_record = BlockProcessingHistory.objects.latest()
        lastblock = last_record.blockhash
    except BlockProcessingHistory.DoesNotExist:
        lastblock = ''

    while True:
        try:
            data = w.listsinceblock(lastblock, MIN_TX_CONFIRMATIONS)  # TODO proper error handling

            if lastblock == data['lastblock']:
                sys.stdout.write('.')  # to avoid newlines
                sleep(SLEEP_TIME)
                continue
            print ''  # to add a new line after all the dots

            lastblock = data['lastblock']

            blockinfo = w.getblock(lastblock) or {}
            blockheight = blockinfo.get('height', 0)

            transactions = sorted(data['transactions'], key=lambda t: t['time'], reverse=True)

            print 'block:{} TXs:{}'.format(lastblock, len(transactions))

            num_pending = 0
            for tx in transactions:
                print '{attn}{category} c:{confirmations} Ð:{amount:.2} => {address} ({account})'.format(
                    attn='!!' if tx['confirmations'] >= MIN_TX_CONFIRMATIONS else '',
                    category=TX_CAT_TO_CHAR[tx['category']],
                    confirmations=tx['confirmations'],
                    amount=tx['amount'],
                    address=tx['address'],
                    account=tx['account']
                )

                if tx['confirmations'] >= MIN_TX_CONFIRMATIONS and tx['category'] == 'receive':
                    transaction = CryptoTransaction.objects.create(
                        tx_type=CryptoTransaction.RECEIVE,  # since we are in the "== receive" branch
                        amount=(Decimal(tx['amount'])),
                        address=tx['address'],
                        txid=tx['txid']
                    )

                    apply_payment(tx['address'], tx['amount'], transaction)

                    w.move(tx['account'], wallet.MOVE_TO_ACCOUNT, tx['amount'])
                else:
                    num_pending += 1

            # Processing transactions done, save blockhash to db as processed
            print '{} TXs in pending (< {} confs)'.format(num_pending, MIN_TX_CONFIRMATIONS)
            print 'Done TXs processing until block {} {}'.format(lastblock, blockheight)

            BlockProcessingHistory.objects.create(
                blockhash=lastblock,
                blockheight=blockheight
            )

        except socket.error:
            print 'Wallet connection error ({wallet_address}). Retrying in {retry_seconds} sec(s)...'.format(
                wallet_address=wallet.CRYPTO_WALLET_ADDRESS,
                retry_seconds=SLEEP_TIME
            )
            w = AuthServiceProxy(wallet.CRYPTO_WALLET_CONNSTRING)  # retry connecting

        sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()



        # Eccel "interface"
        # with open('data.csv', 'w+') as f:
        #     w = csv.DictWriter(f, ['time', 'blocktime', 'account', 'address',
        #                            'amount', 'fee', 'category', 'confirmations'],
        #                        extrasaction='ignore')
        #     w.writeheader()
        #     w.writerows(transactions)
        #     #f.close()