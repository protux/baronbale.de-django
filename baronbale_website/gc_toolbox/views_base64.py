from datetime import datetime
import os

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse

from .forms import Base64EncodeFileForm, Base64EncodeTextForm, Base64DecodeForm
from .tools import base64
from .utils import remove_messages_from_session, CIPHER_MESSAGE_SESSION_KEY, PLAINTEXT_MESSAGE_SESSION_KEY

FILE_NAME_SESSION_KEY = 'download_file_name'
DECODE_DIRECTORY = os.path.join(settings.MEDIA_ROOT, 'base64_decoder')

def index(request):
    encode_file_form = Base64EncodeFileForm()
    if request.session:
        encode_text_form = Base64EncodeTextForm(initial={'message': request.session.get(PLAINTEXT_MESSAGE_SESSION_KEY, None)})
        decode_form = Base64DecodeForm(initial={'message': request.session.get(CIPHER_MESSAGE_SESSION_KEY, None)})
    else:
        encode_text_form = Base64EncodeTextForm()
        decode_form = Base64DecodeForm()

    render_context = {
        'encode_file_form': encode_file_form,
        'encode_text_form': encode_text_form,
        'decode_form': decode_form,
    }

    if FILE_NAME_SESSION_KEY in request.session and request.session[FILE_NAME_SESSION_KEY] != None:
        file_name = request.session[FILE_NAME_SESSION_KEY]
        request.session[FILE_NAME_SESSION_KEY] = None
        print(file_name)
        response = return_download(file_name)
        os.remove(file_name)
        return response

    remove_messages_from_session(request)
    return render(request, 'gc_toolbox/base64.html', render_context)
    
def return_download(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_name)
            return response
    else:
        raise Http404
    
def encode_file(request):
    if request.method == 'POST':
        form = Base64EncodeFileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            file_to_encode = form.cleaned_data['file_to_encode']
            request.session[CIPHER_MESSAGE_SESSION_KEY] = base64.encode(file_to_encode.read())
    return HttpResponseRedirect(reverse('gc_toolbox:base64'))
    
def encode_text(request):
    if request.method == 'POST':
        form = Base64EncodeTextForm(request.POST)
    
        if form.is_valid():
            message = form.cleaned_data['message']
            request.session[CIPHER_MESSAGE_SESSION_KEY] = base64.encode(message)
            request.session[PLAINTEXT_MESSAGE_SESSION_KEY] = message
        
    return HttpResponseRedirect(reverse('gc_toolbox:base64'))
    
def decode(request):
    if request.method == 'POST':
        form = Base64DecodeForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            is_file = form.cleaned_data['is_file']
            if is_file:
                file_content = base64.decode_binary(message)
                file_name = os.path.join(DECODE_DIRECTORY, str(datetime.utcnow().time()))
                with open(file_name, 'wb') as output:
                    output.write(file_content)
                request.session[FILE_NAME_SESSION_KEY] = file_name
            else:
                request.session[CIPHER_MESSAGE_SESSION_KEY] = message
                try:
                    request.session[PLAINTEXT_MESSAGE_SESSION_KEY] = base64.decode_text(message)
                except UnicodeDecodeError:
                    request.session[PLAINTEXT_MESSAGE_SESSION_KEY] = str(base64.decode_binary(message))
    return HttpResponseRedirect(reverse('gc_toolbox:base64'))
