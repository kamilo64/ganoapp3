from django.contrib import admin
from .models import Producto,Descripcion,Contacto
from .forms import DescripcionForm


class ProductonAdmin(admin.ModelAdmin):
    list_display = ["nombre","precio","nuevo","descripcion"]
    list_editable = ["precio"]
    search_fields = ["nombre"]
    list_filter = ["descripcion","nuevo"]
    list_per_page: 5
    form = DescripcionForm

admin.site.register(Producto)
admin.site.register(Descripcion,ProductonAdmin)
admin.site.register(Contacto)