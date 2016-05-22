"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'hoteles.views.inicio'),
    url(r'^cambiartitulo$', 'hoteles.views.cambiartitulo'),
    url(r'^filtrarAloja$', 'hoteles.views.filtrarAloja'),
    url(r'^alojamientos/img/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/img/'}),
    url(r'^alojamientos/css/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/css/'}),
    url(r'^alojamientos$','hoteles.views.mostrarAlojamientos'),
    url(r'^incluirFavorito/img/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/img/'}),
    url(r'^incluirFavorito/css/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/css/'}),
    url(r'^incluirComentario/img/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/img/'}),
    url(r'^incluirComentario/css/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/css/'}),
    url(r'^incluirFavorito/(.+)$','hoteles.views.incluirFavorito'),
    url(r'^incluirComentario/(.+)$','hoteles.views.incluirComentario'),
    url(r'^cambiarIdioma/img/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/img/'}),
    url(r'^cambiarIdioma/css/(.*)$',  'django.views.static.serve',
{'document_root': 'templates/css/'}),
    url(r'^cambiarIdioma/(.*)$','hoteles.views.cambiarIdioma'),
    url(r'^alojamientos/(.+)$','hoteles.views.mostrarAlojamientoId'),
    url(r'^usuario/xml$','hoteles.views.mostrarCss'),
    url(r'^about$','hoteles.views.mostrarAbout'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page' : '/'}),
    url(r'^login', 'hoteles.views.loggear'),
    url(r'^img/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/img/'}),
    url(r'^css/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/css/'}),
    url(r'^mostrarXml/img/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/img/'}),
    url(r'^mostrarXml/css/(.*)$', 'django.views.static.serve',
{'document_root': 'templates/css/'}),
    url(r'^mostrarXml/(.*)$','hoteles.views.mostrarXml'),
    url(r'^miPagina$','hoteles.views.miPagina'),
    url(r'^(.*)$','hoteles.views.pagUsuario'),
]
