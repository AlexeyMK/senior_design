#!/usr/bin/env python
# kindly borrowed from http://blog.onideas.ws/remote_api.gae

import getpass
import os
import sys

## Application specific
SDK_DIR = '../appengine' # TODO - make this work for others
APP_DIR = '.'
APPID = None 
EMAIL = 'alexey86@gmail.com'

REMOTE_API_PATH = '/_ah/remote_api'

## Extra paths to be inserted into sys.path,
## including the SDK, it's libraries, your APPDIR, and APPDIR/lib
EXTRA_PATHS = [
    SDK_DIR,
    os.path.join(SDK_DIR, 'lib', 'antlr3'),
    os.path.join(SDK_DIR, 'lib', 'django'),
    os.path.join(SDK_DIR, 'lib', 'webob'),
    os.path.join(SDK_DIR, 'lib', 'yaml', 'lib'),
    os.path.join(SDK_DIR, 'lib', 'fancy_urllib'),
    APP_DIR,
    os.path.join(APP_DIR, 'lib'),
]
sys.path = EXTRA_PATHS + sys.path

from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.tools import appengine_rpc

def attach(host=None):
    def auth_func():
        if host and host.startswith('localhost'):
            return ('foo', 'bar')
        else:
            return (EMAIL, getpass.getpass())
    remote_api_stub.ConfigureRemoteApi(
      APPID, REMOTE_API_PATH, auth_func, 
      save_cookies=True, secure=False,
      rpc_server_factory=appengine_rpc.HttpRpcServer,
      servername='marketplacr.appspot.com'
    )
    remote_api_stub.MaybeInvokeAuthentication()
    os.environ['SERVER_SOFTWARE'] = 'Development (remote_api)/1.0'
