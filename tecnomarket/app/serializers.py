from .models import Descripcion, Producto
from rest_framework import serializers

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto 
        fields = '__all__'


###########################################################################################

class DescripcionSerializer(serializers.ModelSerializer):
    nombre_marca = serializers.CharField(read_only=True, source="marca.nombre")
    marca = MarcaSerializer(read_only=True)
    marca_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source="marca")
    nombre = serializers.CharField(required=True, min_length=3)

    def validate_nombre(self, value):
        existe = Descripcion.objects.filter(nombre_iexact= value).exists()

        if existe:
            raise value

    class Meta:
        model = Descripcion 
        fields = '__all__'