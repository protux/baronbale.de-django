from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import PolybiusCipherForm
from .tools import polybius
from .utils import remove_messages_from_session, CIPHER_MESSAGE_SESSION_KEY, PLAINTEXT_MESSAGE_SESSION_KEY


def index(request):
    if request.session and CIPHER_MESSAGE_SESSION_KEY in request.session:
        encrypt_form = PolybiusCipherForm(initial={'message': request.session[PLAINTEXT_MESSAGE_SESSION_KEY]})
    else:
        encrypt_form = PolybiusCipherForm()

    if request.session and PLAINTEXT_MESSAGE_SESSION_KEY in request.session:
        decrypt_form = PolybiusCipherForm(initial={'message': request.session[CIPHER_MESSAGE_SESSION_KEY]})
    else:
        decrypt_form = PolybiusCipherForm()

    render_context = {
        'encrypt_form': encrypt_form,
        'decrypt_form': decrypt_form,
    }

    remove_messages_from_session(request)
    return render(request, 'gc_toolbox/polybius.html', render_context)


def encrypt(request):
    if request.method == 'POST':
        encrypt_form = PolybiusCipherForm(request.POST)
        if encrypt_form.is_valid():
            message = encrypt_form.cleaned_data['message']
            request.session[PLAINTEXT_MESSAGE_SESSION_KEY] = message
            request.session[CIPHER_MESSAGE_SESSION_KEY] = polybius.encrypt(message)

    return HttpResponseRedirect(reverse('gc_toolbox:polybius'))


def decrypt(request):
    if request.method == 'POST':
        decrypt_form = PolybiusCipherForm(request.POST)
        if decrypt_form.is_valid():
            message = decrypt_form.cleaned_data['message']
            request.session[CIPHER_MESSAGE_SESSION_KEY] = message
            request.session[PLAINTEXT_MESSAGE_SESSION_KEY] = polybius.decrypt(message)

    return HttpResponseRedirect(reverse('gc_toolbox:polybius'))
