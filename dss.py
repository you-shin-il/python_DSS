#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import grpc

import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

import datetime
import hmac
import hashlib

# Config for GiGA Genie gRPC
CLIENT_ID = 'Y2xpZW50X2lkMTU3MDY3NTI5OTQ2NA=='
CLIENT_KEY = 'Y2xpZW50X2tleTE1NzA2NzUyOTk0NjQ='
CLIENT_SECRET = 'Y2xpZW50X3NlY3JldDE1NzA2NzUyOTk0NjQ='
HOST = 'connector.gigagenie.ai'
PORT = 4080

### COMMON : Client Credentials ###

def getMetadata():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]

    #python 2.x
    message = CLIENT_ID + ':' + timestamp
    signature = hmac.new(CLIENT_SECRET, message, hashlib.sha256).hexdigest()

    # python 3.x
    # message = CLIENT_ID + ':' + timestamp
    # signature = hmac.new(bytes(CLIENT_SECRET, 'utf8'), bytes(message, 'utf8'), hashlib.sha256).hexdigest()

    metadata = [('x-auth-clientkey', CLIENT_KEY),
                ('x-auth-timestamp', timestamp),
                ('x-auth-signature', signature)]

    return metadata

def credentials(context, callback):
    callback(getMetadata(), None)

def getCredentials():
    with open('ca-bundle.pem', 'rb') as f:
        trusted_certs = f.read()
    sslCred = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    authCred = grpc.metadata_call_credentials(credentials)

    return grpc.composite_channel_credentials(sslCred, authCred)
    ### END OF COMMON ###

# DIALOG : queryByText
def queryByText(text):

    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

    message = gigagenieRPC_pb2.reqQueryText()
    message.queryText = text
    message.userSession = "1234"
    message.deviceId = "CC-2F-71-AD-99-A4"

    response = stub.queryByText(message)
    print('================================')
    print(response)
    print('================================')
    print ("resultCd: %d" % (response.resultCd))

    if response.resultCd == 200:
        print ("uword: %s" % (response.uword))
        #dssAction = response.action
    for a in response.action:
        print (a.mesg)
        print (a.actType)

    #return response.url
    else:
        print ("Fail: %d" % (response.resultCd))
        #return None

def main():
    # Dialog : queryByText
    queryByText("지금몇시야")

if __name__ == '__main__':
    main()