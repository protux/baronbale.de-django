from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.urls import reverse

from .forms import CesarCipherEncryptForm, CesarCipherDecryptForm
from .tools import cesar_cipher
from .utils import remove_messages_from_session, CIPHER_MESSAGE_SESSION_KEY, PLAINTEXT_MESSAGE_SESSION_KEY

def index(request):
    if request.session and CIPHER_MESSAGE_SESSION_KEY in request.session:
        encrypt_form = CesarCipherEncryptForm(initial={'plain_message': request.session[PLAINTEXT_MESSAGE_SESSION_KEY]})
    else:
        encrypt_form = CesarCipherEncryptForm()
        
    if request.session and PLAINTEXT_MESSAGE_SESSION_KEY in request.session:
        decrypt_form = CesarCipherDecryptForm(initial={'cipher_message': request.session[CIPHER_MESSAGE_SESSION_KEY]})
    else:
        decrypt_form = CesarCipherDecryptForm()

    render_context = {
        'encrypt_form': encrypt_form,
        'decrypt_form': decrypt_form,
    }

    remove_messages_from_session(request)
    return render(request, 'gc_toolbox/cesar_cipher.html', render_context)

def decrypt(request):
    if request.method == 'POST':
        decrypt_form = CesarCipherDecryptForm(request.POST)
        if decrypt_form.is_valid():
            message = decrypt_form.cleaned_data['cipher_message']
            key = decrypt_form.cleaned_data['key']
            request.session[CIPHER_MESSAGE_SESSION_KEY] = message
            request.session[PLAINTEXT_MESSAGE_SESSION_KEY] = decrypt_cesar(message, key)
            
    return HttpResponseRedirect(reverse('gc_toolbox:cesar'))

def encrypt(request):
    if request.method == 'POST':
        encrypt_form = CesarCipherEncryptForm(request.POST)
        if encrypt_form.is_valid():
            message = encrypt_form.cleaned_data['plain_message']
            key = encrypt_form.cleaned_data['key']
            request.session[CIPHER_MESSAGE_SESSION_KEY] = encrypt_form.cleaned_data['plain_message']
            request.session[PLAINTEXT_MESSAGE_SESSION_KEY] = cesar_cipher.encrypt(key, message)
            
    return HttpResponseRedirect(reverse('gc_toolbox:cesar'))

def decrypt_cesar(message, key):
    if key == '0':
        return cesar_cipher.try_all_keys(message)
        
    try:
        int_key = int(key)
        return cesar_cipher.decrypt(key, message)
    except ValueError:
        return _('The key needs to be an Integer.')
