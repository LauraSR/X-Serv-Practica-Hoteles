from django.contrib import admin
from models import Alojamiento, Imagen, Comentario, Alojamiento_Seleccionado, CSS

# Register your models here.

admin.site.register(Alojamiento)
admin.site.register(Imagen)
admin.site.register(Comentario)
admin.site.register(Alojamiento_Seleccionado)
admin.site.register(CSS)
