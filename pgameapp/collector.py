# coding=utf-8

import csv
import socket
import sys

from time import sleep

import django
from django.contrib.auth import get_user_model
from pgameapp.models import DepositHistory

django.setup()

from django.conf import settings
# settings.configure()
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pgame.settings")
from pgameapp.models.wallet import BlockProcessingHistory

CRYPTO_WALLET_CONNSTRING = '{proto}://{user}:{password}@{address}:{port}'.format(
    proto=settings.CRYPTO_WALLET_PROTO,
    user=settings.CRYPTO_WALLET_USER,
    password=settings.CRYPTO_WALLET_PASSWORD,
    address=settings.CRYPTO_WALLET_IP,
    port=settings.CRYPTO_WALLET_PORT
)

CRYPTO_WALLET_ADDRESS = '{proto}://{address}:{port}'.format(
    proto=settings.CRYPTO_WALLET_PROTO,
    address=settings.CRYPTO_WALLET_IP,
    port=settings.CRYPTO_WALLET_PORT
)

MIN_TX_CONFIRMATIONS = 3
SLEEP_TIME = 5

__author__ = 'Jailbreaker'


# "send"
# "receive"
# "move"
# "orphan"
# "immature"
# "generate"


User = get_user_model()

doge = AuthServiceProxy(CRYPTO_WALLET_CONNSTRING)

if __name__ == '__main__':

    try:
        last_record = BlockProcessingHistory.objects.all()[0]
        lastblock = last_record.blockhash
    except BlockProcessingHistory.DoesNotExist:
        lastblock = ''
        # lastblock = '03d74a6dec6983bc37287b12b5ef8fdc8ab9dfa5030b8982d131a9b5f67ead55'

    while True:
        try:
            data = doge.listsinceblock(lastblock, MIN_TX_CONFIRMATIONS)  # TODO proper error handling
        except socket.error:
            print 'Wallet connection error ({wallet_address}). Retrying in {retry_seconds} sec(s)...'.format(
                wallet_address=CRYPTO_WALLET_ADDRESS,
                retry_seconds=SLEEP_TIME
            )
            sleep(SLEEP_TIME)
            doge = AuthServiceProxy(CRYPTO_WALLET_CONNSTRING)  # retry connecting
            continue

        if lastblock == data['lastblock']:
            sys.stdout.write('.')  # to avoid newlines
            sleep(SLEEP_TIME)
            continue
        print ''  # to add a new line after all the dots

        lastblock = data['lastblock']

        transactions = sorted(data['transactions'], key=lambda t: t['time'], reverse=True)

        confirmed = []
        pending = []

        print 'block:{} TXs:{}'.format(lastblock, len(transactions))

        for tx in transactions:
            print '{attn}{cat} c:{conf} Ð:{amount:.2} => {addr} ({acc})'.format(
                attn='!!' if tx['confirmations'] >= MIN_TX_CONFIRMATIONS else '',
                cat='R' if tx['category'] == 'receive' else 'S',
                conf=tx['confirmations'],
                amount=tx['amount'],
                addr=tx['address'],
                acc=tx['account']
            )

            if tx['confirmations'] >= MIN_TX_CONFIRMATIONS and tx['category'] == 'receive':
                confirmed.append(tx)

                try:
                    user = User.objects.select_related('profile').get(profile__crypto_address=tx['address'])

                    real_currency = tx['amount']
                    game_currency = real_currency  # TODO optional conversion rate
                    user.profile.balance_i += float(game_currency)

                    DepositHistory.objects.create(
                        user=user,
                        real_currency=real_currency,
                        game_currency=game_currency
                    )

                    user.profile.save()

                    print 'Credited Ð {:.2} to {}'.format(game_currency, user)

                except User.DoesNotExist:
                    print 'Owner of "{}" not found. Will credit to catchall address !'. format(tx['address'])  # TODO

            else:
                pending.append(tx)

        else:  # Processing transactions done, save blockhash to db as processed
            print '{} TXs in pending (< {} confs)'.format(len(pending), MIN_TX_CONFIRMATIONS)
            print 'Done TXs processing until block {}'.format(lastblock)
            BlockProcessingHistory.objects.create(blockhash=lastblock)


        
        # Eccel "interface"
        # with open('data.csv', 'w+') as f:
        #     w = csv.DictWriter(f, ['time', 'blocktime', 'account', 'address',
        #                            'amount', 'fee', 'category', 'confirmations'],
        #                        extrasaction='ignore')
        #     w.writeheader()
        #     w.writerows(transactions)
        #     #f.close()

        sleep(SLEEP_TIME)