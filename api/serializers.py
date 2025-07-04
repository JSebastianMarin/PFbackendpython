from rest_framework import serializers
from .models import MovimientoFinanciero

class MovimientoFinancieroSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    
    class Meta:
        model = MovimientoFinanciero
        fields = [
            'id', 'descripcion', 'monto', 'categoria', 'categoria_display',
            'fecha', 'notas', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0")
        return value
    
    def validate_fecha(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("La fecha no puede ser futura")
        return value 