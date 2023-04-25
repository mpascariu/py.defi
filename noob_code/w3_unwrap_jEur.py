#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 00:41:44 2023
Interact with jEUR SynthereumFixedRateWrapper
@author: mpascariu
"""

# Setup
import os
import json
from web3 import Web3

# Here I have a file containing API keys, wallet and smart contract addresses
sys.path.append("/Volumes/DEIFX/py.defi")
import _init  

# Set up the API connection
w3 = Web3(Web3.HTTPProvider(_init.polygon_url_alchemy))
print(w3.is_connected())

#' Approve spending limit
#' Give permision to certain smart contract to spend our tokens. 
#' This would be the first step towards an interaction with the contract.
#' 
#' @param wallet_address:  your wallet; 
#' @param wallet_key:      the wallet' private key;  
#' @param token:           token address for which the approval is to be made;
#' @param spender_address: smart contract address and abi to receive the approval to spend. tuple; 
#' @param amount:          maximum amount for which the permision is given.
#'
def approve_spending_limit(
  wallet_address, 
  wallet_key,
  token, 
  spender_address,
  amount 
  ):
  
  _contract = w3.eth.contract(token[0], abi = json.loads(token[1]))
  _spender  = w3.to_checksum_address(spender_address)
  _wallet   = w3.to_checksum_address(wallet_address)
  _amount   = w3.to_wei(amount,'ether')

  tx = {
    'nonce'   : w3.eth.get_transaction_count(_wallet),
    'from'    : _wallet, 
    'gasPrice': w3.eth.gas_price
    }

  tx['gas']   = w3.eth.estimate_gas(tx)
  tx_function = _contract.functions.approve(spender = _spender, amount = _amount) 
  tx_build    = tx_function.build_transaction(tx)
  tx_signed   = w3.eth.account.sign_transaction(tx_build, wallet_key)
  tx_hash     = w3.eth.send_raw_transaction(tx_signed.rawTransaction)
  
  print('Transaction hash       :', str(w3.to_hex(tx_hash)))
  
  waiting_time = w3.eth.wait_for_transaction_receipt(tx_hash)
  receipt      = w3.eth.get_transaction_receipt(tx_hash)
  
  print(
    '\nApproved Amount        :', amount,
    '\nTransaction Fee (MATIC):', w3.from_wei(receipt.gasUsed,  'ether') * receipt.effectiveGasPrice,
    '\nGas Price (gwei)       :', w3.from_wei(receipt.effectiveGasPrice,  'gwei'),  
    '\nStatus                 :', receipt.status
    )

  return print('Approval DONE!') if receipt.status == 1 else print('Tx FAILED!')



#' Interact with the SynthereumFixedRateWrapper that allows 1:1 conversion between 
#' jEUR and EURe tokens, in any direction, on the Polygon network
#' 
#' @param wallet_address:  your wallet containing the tokens; 
#' @param wallet_key:      the wallet' private key;  
#' @param contract:        SynthereumFixedRateWrapper contract address and abi. Format: tuple;
#' @param amount:          maximum amount for which the permision is given;
#' @param action:          direction of the transaction. Options: 'wrap' and 'unwrap'. 
#'                         With the 'wrap' action we convert EURe to jEUR.
#'                         With the 'unwrap' action we convert jEUR to EURe.
#'
def call_jEUR_wrapper(
  wallet_address, 
  wallet_key, 
  contract, 
  amount, 
  action
  ):
    
  _wallet   = w3.to_checksum_address(wallet_address)
  _contract = w3.eth.contract(contract[0], abi = json.loads(contract[1]))
  _amount   = w3.to_wei(amount, 'ether')
  _nonce    = w3.eth.get_transaction_count(_wallet)
    
  tx = {
    'type'    : '0x2',
    'nonce'   : _nonce,
    'from'    : _wallet,
    'gas'     : 265000,
    'maxFeePerGas': w3.to_wei('2500', 'gwei'),
    'maxPriorityFeePerGas': w3.to_wei('50', 'gwei'),
    }
    
  if action == 'wrap':
    tx_action = _contract.functions.wrap(_collateral = _amount, _recipient = _wallet)
  elif action == 'unwrap':
    tx_action = _contract.functions.unwrap(_tokenAmount = _amount, _recipient = _wallet)
  else:
    raise TypeError("Choose the action you want to execute: 'wrap' or 'unwrap'")
        
  tx_build  = tx_action.build_transaction(tx)
  tx_signed = w3.eth.account.sign_transaction(tx_build, private_key = wallet_key)
  tx_hash   = w3.eth.send_raw_transaction(tx_signed.rawTransaction)
    
  print('Transaction hash   : ', str(w3.to_hex(tx_hash)))
    
  waiting_time = w3.eth.wait_for_transaction_receipt(tx_hash)
  receipt      = w3.eth.get_transaction_receipt(tx_hash)
    
  print(
    '\nToken Name             :', _contract.functions.syntheticToken().call(), '-', _contract.functions.syntheticTokenSymbol().call(),
    '\nTotal Supply           :', w3.from_wei(_contract.functions.totalSyntheticTokensMinted().call(), 'ether'),
    '\nTotal Peg Collateral   :', w3.from_wei(_contract.functions.totalPegCollateral().call(), 'ether'),
    '\nConversion Rate        :', w3.from_wei(_contract.functions.conversionRate().call(), 'ether'),
    '\nTransaction Amount     :', amount,
    '\nTransaction Fee (MATIC):', w3.from_wei(receipt.gasUsed, 'ether') * receipt.effectiveGasPrice,
    '\nGas Price (gwei)       :', w3.from_wei(receipt.effectiveGasPrice, 'gwei'),  
    '\nStatus                 :', receipt.status
  )
    
  return print('\nTx DONE!') if receipt.status == 1 else print('\nTx FAILED!')



# ------------------------------------------------------------
# Run the functions

approve_spending_limit(
  wallet_address  = _init.w_cologne,
  wallet_key      = _init.pk_cologne
  token           = _init.sc_PolygonPosEURe,
  spender_address = _init.sc_SynthereumFixedRateWrapper[0],
  amount          = 1000
  )

wrapper_jEUR(
  wallet_address = _init.w_cologne, 
  wallet_key     = _init.pk_cologne,
  contract       = _init.sc_SynthereumFixedRateWrapper,
  amount         = 1,
  action         = 'unwrap'
  )



