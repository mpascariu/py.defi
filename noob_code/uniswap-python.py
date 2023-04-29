#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
uniswap-python examples
@author: mpascariu
"""

# Setup
import os
import json
import sys
from web3 import Web3
from uniswap import Uniswap

# Here I have a file containing API keys, wallet and smart contract addresses
sys.path.append("/Volumes/DEIFX/py.defi")
import _init  

# Set up the API connection
w3 = Web3(Web3.HTTPProvider(_init.polygon_url_alchemy))
print(w3.is_connected())

# Uniswap-python 

uniswap = Uniswap(
    address     = _init.w_cologne, 
    private_key = _init.pk_cologne, 
    provider    = _init.polygon_url_alchemy,
    version     = 3
    )


wmatic = uniswap.get_weth_address()
dai   = '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'
eure  = '0x18ec0A6E18E5bc3784fDd3a3634b31245ab704F6'
usdt  = '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'
usdc  = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'

def value(x):
    out = w3.from_wei(x,  'ether')
    out = round(out, 4)
    return print(out)


# sell 1000 tokens for DAI
# the amount of DAI received is:
amount     = 1000
decimals   = 18
amount_wei = amount * (10**decimals)

value(uniswap.get_price_output(wmatic, dai, amount_wei))
value(uniswap.get_price_output(eure, dai, amount_wei))
uniswap.get_raw_price(token_in = dai, token_out = eure) * 1000

# spend 1000 DAI for tokens
# the amount of tokens received is:
value(uniswap.get_price_input(dai, wmatic, amount_wei))
value(uniswap.get_price_input(dai, eure, amount_wei))
uniswap.get_raw_price(token_in = dai, token_out = eure) * 1000
uniswap.get_raw_price(token_in = usdt, token_out = eure) * 1000

# check wallet ballance 
value(uniswap.get_token_balance(eure))
value(uniswap.get_token_balance(dai))



