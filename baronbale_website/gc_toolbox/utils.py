
CIPHER_MESSAGE_SESSION_KEY = 'cipher_message'
PLAINTEXT_MESSAGE_SESSION_KEY = 'plain_message'

def remove_messages_from_session(request):
    if PLAINTEXT_MESSAGE_SESSION_KEY in request.session:
        request.session[PLAINTEXT_MESSAGE_SESSION_KEY] = None
    if CIPHER_MESSAGE_SESSION_KEY in request.session:
        request.session[CIPHER_MESSAGE_SESSION_KEY] = None
