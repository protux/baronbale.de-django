from django.conf.urls import url

from . import views_cesar, views_polybius, views_lettervalues, views_base64

app_name = 'gc_toolbox'
urlpatterns = [
    url(r'^base64/$', views_base64.index, name='base64'),
    url(r'^base64/encode/file/$', views_base64.encode_file, name='base64_encode_file'),
    url(r'^base64/encode/text/$', views_base64.encode_text, name='base64_encode_text'),
    url(r'^base64/decode/$', views_base64.decode, name='base64_decode'),
    
    url(r'^cesar/$', views_cesar.index, name='cesar'),
    url(r'^cesar/encrypt/$', views_cesar.encrypt, name='cesar_encrypt'),
    url(r'^cesar/decrypt/$', views_cesar.decrypt, name='cesar_decrypt'),
    
    url(r'^lettervalues/$', views_lettervalues.letter_value_calculator, name='lettervalues'),
    
    url(r'^polybius/$', views_polybius.index, name='polybius'),
    url(r'^polybius/encrypt/$', views_polybius.encrypt, name='polybius_encrypt'),
    url(r'^polybius/decrypt/$', views_polybius.decrypt, name='polybius_decrypt'),
]
