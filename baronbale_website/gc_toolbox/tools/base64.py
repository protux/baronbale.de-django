import base64, sys

def decode_text(b64):
    return base64.b64decode(b64).decode('utf-8')
    
def decode_binary(b64):
    return base64.b64decode(b64)
    
def encode(text):
    if type(text) == str:
        text = bytes(text, 'utf-8')
    return base64.b64encode(text).decode('utf-8')
