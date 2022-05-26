from math import prod
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Descripcion, Producto
from .forms import ContactoForm, CustomUserCreationForm, DescripcionForm, UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets
from .serializers import DescripcionSerializer, MarcaSerializer

def error_facebook(request):
    return render(request,'registration/error_facebook.html')

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = MarcaSerializer



class DescripcionViewset(viewsets.ModelViewSet):
    queryset  = Descripcion.objects.all()
    serializer_class = DescripcionSerializer

    def get_queryset(self):
        productos = Descripcion.objects.all()

        nombre = self.request.GET.get('nombre')

        if nombre:
            productos = productos.filter(nombre__contains=nombre)
        
        return productos


###########################################################################

def home(request):
    productos = Descripcion.objects.all()
    data = {
        'productos' : productos

    }
    return render(request, 'app/home.html',data)

###########################################################################################

def contacto(request):
    data = {
        'form' : ContactoForm()
    }

    if request.method == 'POST' :
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Contacto guardado"
        else :
            data["form"] = formulario

    return render(request, 'app/contacto.html',data)

###########################################################################################

def galeria(request):
    return render(request, 'app/galeria.html')

###########################################################################################

@permission_required('app.add_producto')
def agregar_producto(request):
    data = {
        'form' : DescripcionForm()

    }

    if request.method == 'POST':
        formulario = DescripcionForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto registrado")
        else :
            data["form"] = formulario
        

    return render(request, 'app/producto/agregar.html', data )

###########################################################################################

@permission_required('app.view_producto')
def listar_productos(request):
    productos= Descripcion.objects.all() 
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)

    except:
        raise Http404
    
    
    data = {
        'entity' : productos,
        'paginator' : paginator

    }
    return render(request, 'app/producto/listar.html', data)

###########################################################################################

@permission_required('app.change_producto')
def modificar_producto(request, id):

    producto = get_object_or_404(Descripcion, id=id)

    data = {
        'form' : DescripcionForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = DescripcionForm(data=request.POST, instance=producto , files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_productos")
        else :
            data["form"] = formulario
        

    return render(request, 'app/producto/modificar.html', data)

###########################################################################

@permission_required('app.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Descripcion, id=id)
    producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_productos")

###########################################################################

def registro(request):
    data = {
        'form' : CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registro exitoso  ")
            return redirect(to="home")
        data["form"] = formulario
    
    return render(request, 'registration/registro.html', data)

###########################################################################    