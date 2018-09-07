# from __future__ import print_function

import hashlib
import hmac
import logging
import os
import sys

# TODO: Refresh all keys

# BART
BART_PUBL = os.environ.get('BART_PUBL')
BART_PRIV = os.environ.get('BART_PRIV')

# Facebook
FB_PAGE_ACCESS = os.environ.get('FB_PAGE_ACCESS')
FB_PAGE_ACCESS_2 = os.environ.get('FB_PAGE_ACCESS_2')
FB_VERIFY_TOK = os.environ.get('FB_VERIFY_TOK')

# Dark Sky
DS_TOK = os.environ.get('DARK_SKY_PRIV')

# Wit
WIT_TOK = os.environ.get('WIT_SERVER_TOK')

# Debug
DEBUG_TOK = os.environ.get('DEBUG_TOK')


def gen_app_secret_proof():
    """Calculates FB app secret proof from SHA256"""
    logging.info("Generating app secret proof in keys.py")
    pudding = hmac.new(FB_PAGE_ACCESS_2.encode('utf-8'),
        msg=FB_PAGE_ACCESS.encode('utf-8'),
        digestmod=hashlib.sha256).hexdigest()
    return pudding

