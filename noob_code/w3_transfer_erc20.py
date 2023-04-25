#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 22:06:44 2023
Setup for sending ERC20 tokens from your wallet to another wallet on the Polygon network
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

# Function setup for sending ERC20 tokens from your wallet to another wallet
# on the Polygon network
def send_erc20(
        sender, 
        sender_key, 
        recipient, 
        token, 
        amount
        ):
    
    tx = {
        'nonce': w3.eth.get_transaction_count(sender),
        'gasPrice': w3.eth.gas_price
    }

    tx['gas'] = w3.eth.estimate_gas(tx)
    _contract = w3.eth.contract(token[0], abi = token[1])
    _amount   = w3.to_wei(amount, 'ether')
    built_tx  = _contract.functions.transfer(recipient, _amount).build_transaction(tx)
    signed_tx = w3.eth.account.sign_transaction(built_tx , private_key = sender_key)
    tx_hash   = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print('Transaction hash   : ', str(w3.to_hex(tx_hash)))
    
    waiting_time = w3.eth.wait_for_transaction_receipt(tx_hash)
    receipt      = w3.eth.get_transaction_receipt(tx_hash)
    
    print(
      '\nToken Name             :', _contract.functions.name().call(), '-', _contract.functions.symbol().call(),
      '\nTotal Supply           :', w3.from_wei(_contract.functions.totalSupply().call(), 'ether'),
      '\nTransaction amount     :', amount,
      '\nSender Balance         :', w3.from_wei(_contract.functions.balanceOf(sender).call(), 'ether'),
      '\nRecipient Balance      :', w3.from_wei(_contract.functions.balanceOf(recipient).call(), 'ether'),
      '\nTransaction Fee (MATIC):', w3.from_wei(receipt.gasUsed, 'ether') * receipt.effectiveGasPrice,
      '\nGas Price (gwei)       :', w3.from_wei(receipt.effectiveGasPrice, 'gwei'),  
      '\nStatus                 :', receipt.status
    )
    
    return print('\nTx DONE!') if receipt.status == 1 else print('\nTx FAILED!')


# ------------------------------------------------------------
# Run the function

send_erc20(
    sender     = _init.w_cologne, 
    sender_key = _init.pk_cologne,
    recipient  = _init.w_brave,
    erc20      = _init.sc_PolygonPosjEUR,
    amount     = 0.011
    )


