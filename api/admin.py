from django.contrib import admin
from .models import MovimientoFinanciero

@admin.register(MovimientoFinanciero)
class MovimientoFinancieroAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'monto', 'categoria', 'fecha', 'fecha_creacion']
    list_filter = ['categoria', 'fecha', 'fecha_creacion']
    search_fields = ['descripcion', 'notas']
    date_hierarchy = 'fecha'
    ordering = ['-fecha', '-fecha_creacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('descripcion', 'monto', 'categoria', 'fecha')
        }),
        ('Información Adicional', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
