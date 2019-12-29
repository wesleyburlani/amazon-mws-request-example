## Use python2.7 to run this code
## this code makes an MWS request to retrieve an order based on your AmazonOrderId
import urllib
import pandas
import requests
import hashlib
import base64
from hashlib import sha256
from hmac import HMAC
from datetime import datetime
from xml.dom import minidom

## Configs ###
MwsDomain = "https://mws.amazonservices.com" 
AWSAccessKeyId = ""
MWSAuthToken = ""
SellerId = ""
SecretKey = "" ## hub
MarketplaceId = "A2Q3Y263D00KWC" ## brazil

def __main__():
    orderID = input('orderID: ')
    request(orderID)

def request(orderId):
    params = {
        'AWSAccessKeyId': AWSAccessKeyId,
        'Action': 'GetOrder',
        'AmazonOrderId.Id.1': orderId,
        'SellerId': SellerId,
        'SignatureVersion': '2',
        'MWSAuthToken': MWSAuthToken,
        'Timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        'Version': '2013-09-01',
        'SignatureMethod': 'HmacSHA256',
        'MarketplaceId': MarketplaceId,
        'PurgeAndReplace': 'false'
    }
    params['Signature'] = calcMWSSignatureParam(SecretKey, "POST", MwsDomain, params)
    params = sorted(params.items())
    headers = {
        'User-Agent': 'Example'
    }
    results = requests.post(MwsDomain +"/Orders/2013-09-01", params=params, headers= headers)
    print(results.text)

def calcMWSSignatureParam(secretKey, method, url, params):
    urlparams = urllib.urlencode(sorted(params.items()))
    url = url.replace('https://', '').lower()
    signData = '\n'.join([method, url, "/Orders/2013-09-01", urlparams])
    signature = base64.b64encode(HMAC(secretKey, signData, sha256).digest())
    return signature

__main__()