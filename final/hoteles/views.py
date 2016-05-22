from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib2
import sys
import os.path
from parseHandler import myContentHandler
from models import Alojamiento, Imagen, Comentario, Alojamiento_Seleccionado, CSS
from django.contrib.auth.models import User
from operator import itemgetter
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

#from models import Contenido
#from django.template.loader import get_template
#from django.template import Context
#from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def parsear(idioma):
    # Load parser and driver
    print "PARSEAR!"
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    # Ready, set, go!
    if idioma == 'es':
        xmlFile = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_es.xml')
    if idioma == 'en':
        xmlFile = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_en.xml')
    if idioma == 'fr':
        xmlFile = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_fr.xml')
    theParser.parse(xmlFile)
    lista = theHandler.dameLista()
    print "Parse " + idioma + " complete"
    return lista

@csrf_exempt
def inicio(request):
    respuesta = ""
    list_ordenada = []
    list_usrs = []
    alojamientos = Alojamiento.objects.all()
    if len(alojamientos) < 1:
        lista_es = parsear('es')
        iniHoteles(lista_es)
    list_ordenada = ordenarAloja(alojamientos)
    contador = 10
    list_aloj = []
    usuarios = User.objects.all()
    for elem in list_ordenada:
        if contador > 0 and elem[1] > 0:
            contador = contador - 1
            try:
                alojamiento = Alojamiento.objects.get(id = elem[0])
                imagenes = Imagen.objects.filter(alojamiento_id = alojamiento)
                usuarios = User.objects.all()
                for usuario in usuarios:
                    try:
                        css = CSS.objects.get(usuario=usuario.username)
                        if len(list_usrs)<len(usuarios):
                            list_usrs.append((css.usuario, css.titulo))
                    except CSS.DoesNotExist:
                        if len(list_usrs)<len(usuarios):
                            list_usrs.append((usuario.username, ("Pagina de " + usuario.username)))
                if len(imagenes)>0:
                    list_aloj.append((alojamiento, imagenes[0].url))
                else:
                    list_aloj.append((alojamiento, ""))
            except ObjectDoesNotExist:
                    print "No existe el alojamiento!"
            print list_usrs
    template = get_template('plantilla_index.html')
    context = RequestContext(request, {'alojamientos': list_aloj, 'usuarios': list_usrs}) #le pasamos el objeto completo
    return HttpResponse(template.render(context))

@csrf_exempt
def iniHoteles(lista):
    respuesta = ""
    for dicHotel in lista:
        nombre = dicHotel['name']
        direccion = dicHotel['address'] + ', ' + dicHotel['zipcode']
        categoria = dicHotel['categoria'] + "\n"
        try:
            estrellas = dicHotel['estrellas']
        except KeyError:
            pass
        url = dicHotel['web']
        descripcion = strip_tags(dicHotel['body'])
        hotel = Alojamiento(nombre = nombre, direccion = direccion, categoria = categoria, estrellas = estrellas, url = url, descripcion = descripcion)
        hotel.save()
        list_imag = dicHotel['url']
        print list_imag
        for url_imagen in list_imag:
            if len(list_imag) > 0:
                imagen = Imagen(url = url_imagen, alojamiento_id = hotel)
                imagen.save()
    print "Hoteles Guardados"

@csrf_exempt
#Ordena la lista de alojamientos por de numero de comentarios de mayor a menor
def ordenarAloja(lista):
    dic = {}
    lis_ordenada = []
    respuesta = ""
    for alojamiento in lista:
        identificador = alojamiento.id
        try:
            comentarios = Comentario.objects.filter(alojamiento_id = identificador)
            dic[identificador] =len(comentarios)
        except Comentario.DoesNotExist:
            respuesta += "No tiene comentarios"
            print respuesta
    lis_ordenada = sorted(dic.items(), key = itemgetter(1), reverse = True)
    print str(len(lis_ordenada))
    '''
    for elem in lis_ordenada:
        if elem[1]>0:
            respuesta += str(elem[0]) + ": " + str(elem[1])
    '''
    return lis_ordenada

@csrf_exempt
def pagUsuario(request, user):
    print user
    list_aloj = []
    #username = request.user.username
    try:
        css = CSS.objects.get(usuario=user)
        titulo = css.titulo
        u = user
        usuario = User.objects.get(username=user)
    except CSS.DoesNotExist:
        print user
        usuario = User.objects.get(username=user)
        u = usuario.username
        titulo = ""
    try:
        aloj_seleccionados = Alojamiento_Seleccionado.objects.filter(usuario=usuario)
        for alojamiento in aloj_seleccionados:
            imagenes = Imagen.objects.filter(alojamiento_id = alojamiento.alojamiento_id)
            if len(imagenes)>0:
                list_aloj.append((alojamiento, imagenes[0].url))
            else:
                list_aloj.append((alojamiento, ""))
    except ObjectDoesNotExist:
            print "No existen favoritos..."
    template = get_template('plantilla_usuario.html')
    context = RequestContext(request, {'alojamientos': list_aloj, 'usuario': u, 'titulo': titulo}) #le pasamos el objeto completo
    return HttpResponse(template.render(context))

@csrf_exempt
def miPagina(request):
    username = request.user.username
    return HttpResponseRedirect("/" + username)

@csrf_exempt
def cambiartitulo(request):
    list_aloj = []
    if request.user.is_authenticated():
        username = request.user.username
        titulo = request.POST.get("titulo")
        print "TITULO1 : "
        print titulo
        try:
            css = CSS.objects.get(usuario=username)
            css.titulo = titulo
            css.save()
            usuario = User.objects.get(username=username)
        except CSS.DoesNotExist:
            css = CSS(titulo=titulo, usuario=username, tamannoFuente=0.0, colorFondo="#20B2AA")
            css.save()
            usuario = User.objects.get(username=username)
    else:
        titulo = ""
        print "TITULO2 : "
        print titulo
        usuario = User.objects.get(username=request.user.username)
        username = usuario.username
    try:
        aloj_seleccionados = Alojamiento_Seleccionado.objects.filter(usuario=usuario)
        for alojamiento in aloj_seleccionados:
            imagenes = Imagen.objects.filter(alojamiento_id = alojamiento.alojamiento_id)
            if len(imagenes)>0:
                list_aloj.append((alojamiento, imagenes[0].url))
            else:
                list_aloj.append((alojamiento, ""))
    except ObjectDoesNotExist:
            print "No existen favoritos..."
    print "TITULO : "
    print titulo
    template = get_template('plantilla_usuario.html')
    context = RequestContext(request, {'alojamientos': list_aloj, 'usuario': username, 'titulo': titulo}) #le pasamos el objeto completo
    return HttpResponse(template.render(context))


@csrf_exempt
def loggear (request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username= username, password = password)
    if user is not None:
        login(request, user)
    return HttpResponseRedirect("/")

@csrf_exempt
def incluirFavorito(request, id):
    if request.user.is_authenticated():
        username = request.user.username
        try:
            usr = User.objects.get(username=username)
            alojamiento = Alojamiento.objects.get(id=id)
            imagenes = Imagen.objects.filter(alojamiento_id = alojamiento)
            comentarios = Comentario.objects.filter(alojamiento_id=alojamiento)
            if len(imagenes)==0:
                imagenes = []
            if len(comentarios)==0:
                comentarios = []
            try:
                Alojamiento_Seleccionado.objects.get(alojamiento_id=alojamiento)
                template = get_template('plantilla_favoritoYA.html')
                context = RequestContext(request, {'alojamiento': alojamiento, 'imagenes': imagenes, 'comentarios': comentarios}) #le pasamos el objeto completo
                return HttpResponse(template.render(context))
            except Alojamiento_Seleccionado.DoesNotExist:
                favorito = Alojamiento_Seleccionado(alojamiento_id=alojamiento, usuario=usr)
                favorito.save()
                template = get_template('plantilla_alojamientoID.html')
                context = RequestContext(request, {'alojamiento': alojamiento, 'imagenes': imagenes, 'comentarios': comentarios})
                return HttpResponse(template.render(context))
        except ObjectDoesNotExist:
            print "No existe el alojamiento!"

@csrf_exempt
def mostrarAlojamientos(request):
    alojamientos = Alojamiento.objects.all()

    template = get_template('plantilla_alojamiento.html')
    context = RequestContext(request, {'alojamientos': alojamientos})
    return HttpResponse(template.render(context))

@csrf_exempt
def filtrarAloja(request):
    list_aloj = []
    categoria = request.POST.get("categoria")
    categoria = categoria + "\n"
    estrellas = request.POST.get("estrellas")
    todos = Alojamiento.objects.all()
    if categoria in ["Hoteles\n","Apartahoteles\n","Hostales\n","Albergues\n","Residencias universitarias\n","Camping\n","Pensiones\n"] and estrellas == "todos":
        list_aloj = Alojamiento.objects.filter(categoria=categoria)
    elif categoria in ["Hoteles\n", "Hostales\n"] and estrellas in ["1 estrella", "2 estrellas", "3 estrellas", "4 estrellas", "5 estrellas", "5 estrellas Gran Lujo"]:
        list_aloj = Alojamiento.objects.filter(categoria=categoria, estrellas=estrellas)
    elif categoria == "Apartahoteles\n" and estrellas in ["1 llave", "2 llaves", "3 llaves", "4 llaves"]:
        list_aloj = Alojamiento.objects.filter(categoria=categoria, estrellas=estrellas)
    elif categoria == "todos" and estrellas in ["1 estrella", "2 estrellas", "3 estrellas", "4 estrellas", "5 estrellas", "5 estrellas Gran Lujo"]:
        list_aloj = Alojamiento.objects.filter(estrellas=estrellas)
        print len(list_aloj)
    elif categoria == "todos" and estrellas in ["1 llave", "2 llaves", "3 llaves", "4 llaves"]:
        list_aloj = Alojamiento.objects.filter(estrellas=estrellas)
    elif categoria == "todos" and estrellas == "todos":
        list_aloj = Alojamiento.objects.all()
    template = get_template('plantilla_alojamiento.html')
    context = RequestContext(request, {'alojamientos': list_aloj, 'todos': todos}) #le pasamos el objeto completo
    return HttpResponse(template.render(context))

@csrf_exempt
def mostrarAlojamientoId(request, id):
    try:
        alojamiento = Alojamiento.objects.get(id=id)
        imagenes = Imagen.objects.filter(alojamiento_id = alojamiento)
        comentarios = Comentario.objects.filter(alojamiento_id = alojamiento)
        if len(imagenes)==0:
            imagenes = []
        if len(comentarios)==0:
            comentarios = []
    except ObjectDoesNotExist:
        print "No existe dicho alojamiento!"

    template = get_template('plantilla_alojamientoID.html')
    context = RequestContext(request, {'alojamiento': alojamiento, 'imagenes': imagenes, 'comentarios': comentarios})
    return HttpResponse(template.render(context))

@csrf_exempt
def incluirComentario(request, id):
    if request.user.is_authenticated():
        username = request.user.username
        cuerpo = request.POST.get("comentario")
        alojamiento = Alojamiento.objects.get(id = id)
        coment = Comentario(cuerpo=strip_tags(cuerpo), alojamiento_id = alojamiento)
        coment.save()
        return HttpResponseRedirect("/alojamientos/" + str(id))
    else:
        return HttpResponseRedirect("/alojamientos/" + str(id))


@csrf_exempt
def cambiarIdioma(request, ident):
    lista = []
    idioma = request.POST.get("idioma")
    print idioma
    alojamiento = Alojamiento.objects.get(id=ident)
    imagenes = Imagen.objects.filter(alojamiento_id = alojamiento)
    comentarios = Comentario.objects.filter(alojamiento_id=alojamiento)
    if len(imagenes)==0:
        imagenes = []
    if len(comentarios)==0:
        comentarios = []
    nombre = alojamiento.nombre
    if idioma=="ingles":
        lista = parsear("en")
        for elem in lista:
            if elem["name"]==nombre:
                body = elem["body"]
                print body
                alojamiento.descripcion = body
        template = get_template('plantilla_alojamientoID.html')
        context = RequestContext(request, {'alojamiento': alojamiento, 'imagenes': imagenes, 'comentarios': comentarios}) #le pasamos el objeto completo
        return HttpResponse(template.render(context))
    if idioma=="frances":
        lista = parsear("fr")
        for elem in lista:
            if elem["name"]==nombre:
                body = elem["body"]
                alojamiento.descripcion = body
        template = get_template('plantilla_alojamientoID.html')
        context = RequestContext(request, {'alojamiento': alojamiento, 'imagenes': imagenes, 'comentarios': comentarios}) #le pasamos el objeto completo
        return HttpResponse(template.render(context))
    if idioma=="espaniol":
        return HttpResponseRedirect("/alojamientos/" + str(ident))

@csrf_exempt
def cargarXml():
    list_aloj = []
    xmlFile = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_es.xml')
    lineas = xmlFile.read()
    list_aloj = lineas.split('</service>')
    list_aloj[0].replace('<serviceList>', '')
    for aloj in list_aloj:
        aloj = aloj + '</service>'
    return list_aloj


@csrf_exempt
def mostrarXml(request, user):
    list_aloj = cargarXml()
    usuario = User.objects.get(username=user)
    alojamientos = Alojamiento_Seleccionado.objects.filter(usuario=usuario)
    elementosXML = ["<serviceList>\n"]
    for alojamiento in alojamientos:
        for elem in list_aloj:
            if not elem.find(alojamiento.alojamiento_id.nombre.encode('utf-8')) == -1:
                elementosXML.append(elem + "\n")
    elementosXML.append("</serviceList>\n")
    template = get_template('plantilla_xml.html')
    context = RequestContext(request, {'elementosXML': elementosXML, 'usuario': user})
    return HttpResponse(template.render(context))


@csrf_exempt
def mostrarCss(request):
    respuesta = ""
    return HttpResponse(respuesta)

@csrf_exempt
def mostrarAbout(request):
    template = get_template('plantilla_about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
