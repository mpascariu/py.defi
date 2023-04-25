#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 13:12:43 2023
Setup for sending MATIC tokens from your wallet to another wallet
@author: mpascariu
"""

# Setup
import os
import sys
from web3 import Web3

# Here I have a file containing API keys, wallet and smart contract addresses
sys.path.append("/Volumes/DEIFX/py.defi")
import _init  

# Set up the API connection
w3 = Web3(Web3.HTTPProvider(_init.polygon_url_alchemy))
print(w3.is_connected())

# Function setup for sending MATIC tokens from your wallet to another wallet
def send_matic(
        sender, 
        sender_key, 
        recipient, 
        amount
        ):
    
    from_wallet = w3.to_checksum_address(sender) # validate wallet
    to_wallet   = w3.to_checksum_address(recipient)
    
    tx = {
        'type'  : '0x2',
        'nonce' : w3.eth.get_transaction_count(from_wallet),
        'from'  : from_wallet,
        'to'    : to_wallet,
        'value' : w3.to_wei(amount, 'ether'),
        'maxFeePerGas': w3.to_wei('1000', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('50', 'gwei'),
        'chainId': 137
    }
    
    tx['gas'] = w3.eth.estimate_gas(tx)
    tx_signed = w3.eth.account.sign_transaction(tx, private_key = sender_key)
    tx_hash   = w3.eth.send_raw_transaction(tx_signed.rawTransaction)
    
    print('Transaction hash   : ', str(w3.to_hex(tx_hash)))
    
    waiting_time = w3.eth.wait_for_transaction_receipt(tx_hash)
    receipt      = w3.eth.get_transaction_receipt(tx_hash)

    print(
     "Transaction hash   : ", str(w3.to_hex(tx_hash)), 
      "\nTransaction amount : ", amount,
      "\nSender balance     : ", w3.from_wei(w3.eth.get_balance(sender), unit = 'ether'), 
      "\nReceiver balance   : ", w3.from_wei(w3.eth.get_balance(recipient), unit = 'ether')
      )
    
    return print('\nTx DONE!') if receipt.status == 1 else print('\nTx FAILED!')


# ------------------------------------------------------------
# Run the function

send_matic(
    sender     = _init.w_cologne, 
    sender_key = _init.pk_cologne,
    recipient   = _init.w_brave, 
    amount     = 0.01
    )





