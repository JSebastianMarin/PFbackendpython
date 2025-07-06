from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Q
from datetime import datetime, date
from .models import MovimientoFinanciero
from .serializers import MovimientoFinancieroSerializer
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

@extend_schema_view(
    list=extend_schema(
        summary="Listar movimientos financieros",
        description="Obtiene una lista paginada de movimientos financieros con opciones de filtrado y ordenamiento",
        parameters=[
            OpenApiParameter(
                name='categoria',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por categoría (ingreso o gasto)',
                examples=[
                    OpenApiExample('Ingresos', value='ingreso'),
                    OpenApiExample('Gastos', value='gasto'),
                ]
            ),
            OpenApiParameter(
                name='fecha_desde',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha inicial para filtrar (YYYY-MM-DD)',
                examples=[OpenApiExample('Ejemplo', value='2024-01-01')]
            ),
            OpenApiParameter(
                name='fecha_hasta',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha final para filtrar (YYYY-MM-DD)',
                examples=[OpenApiExample('Ejemplo', value='2024-01-31')]
            ),
            OpenApiParameter(
                name='ordenar_por',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Campo para ordenar',
                examples=[
                    OpenApiExample('Por fecha', value='fecha'),
                    OpenApiExample('Por monto', value='monto'),
                    OpenApiExample('Por fecha de creación', value='fecha_creacion'),
                ]
            ),
            OpenApiParameter(
                name='orden',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Orden de clasificación',
                examples=[
                    OpenApiExample('Ascendente', value='asc'),
                    OpenApiExample('Descendente', value='desc'),
                ]
            ),
        ],
        tags=['movimientos']
    ),
    create=extend_schema(
        summary="Crear nuevo movimiento",
        description="Crea un nuevo movimiento financiero (ingreso o gasto)",
        examples=[
            OpenApiExample(
                'Crear ingreso',
                value={
                    "descripcion": "Salario mensual",
                    "monto": "3000.00",
                    "categoria": "ingreso",
                    "fecha": "2024-01-15",
                    "notas": "Salario de enero"
                },
                request_only=True
            ),
            OpenApiExample(
                'Crear gasto',
                value={
                    "descripcion": "Supermercado",
                    "monto": "150.50",
                    "categoria": "gasto",
                    "fecha": "2024-01-16",
                    "notas": "Compra semanal"
                },
                request_only=True
            ),
        ],
        tags=['movimientos']
    ),
    retrieve=extend_schema(
        summary="Obtener movimiento específico",
        description="Obtiene los detalles de un movimiento financiero por su ID",
        tags=['movimientos']
    ),
    update=extend_schema(
        summary="Actualizar movimiento completo",
        description="Actualiza todos los campos de un movimiento financiero",
        tags=['movimientos']
    ),
    partial_update=extend_schema(
        summary="Actualizar movimiento parcialmente",
        description="Actualiza solo los campos especificados de un movimiento financiero",
        tags=['movimientos']
    ),
    destroy=extend_schema(
        summary="Eliminar movimiento",
        description="Elimina permanentemente un movimiento financiero",
        tags=['movimientos']
    ),
)
class MovimientoFinancieroViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de movimientos financieros.
    
    list: Obtiene todos los movimientos con opciones de filtrado
    create: Crea un nuevo movimiento
    retrieve: Obtiene un movimiento específico
    update: Actualiza un movimiento completo
    partial_update: Actualiza parcialmente un movimiento
    destroy: Elimina un movimiento
    """
    queryset = MovimientoFinanciero.objects.all()
    serializer_class = MovimientoFinancieroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Permite filtrar movimientos por:
        - categoria: 'ingreso' o 'gasto'
        - fecha_desde: fecha inicial (YYYY-MM-DD)
        - fecha_hasta: fecha final (YYYY-MM-DD)
        - ordenar_por: 'fecha', 'monto', 'fecha_creacion'
        - orden: 'asc' o 'desc'
        """
        queryset = MovimientoFinanciero.objects.filter(user=self.request.user)
        
        # Filtros
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        fecha_desde = self.request.query_params.get('fecha_desde', None)
        if fecha_desde:
            try:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha__gte=fecha_desde)
            except ValueError:
                pass
        
        fecha_hasta = self.request.query_params.get('fecha_hasta', None)
        if fecha_hasta:
            try:
                fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha__lte=fecha_hasta)
            except ValueError:
                pass
        
        # Ordenamiento
        ordenar_por = self.request.query_params.get('ordenar_por', 'fecha')
        orden = self.request.query_params.get('orden', 'desc')
        
        if ordenar_por in ['fecha', 'monto', 'fecha_creacion']:
            if orden == 'asc':
                queryset = queryset.order_by(ordenar_por)
            else:
                queryset = queryset.order_by(f'-{ordenar_por}')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Obtener resumen financiero",
        description="Obtiene un resumen de ingresos y gastos en un rango de fechas opcional",
        parameters=[
            OpenApiParameter(
                name='fecha_desde',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha inicial para el resumen (YYYY-MM-DD)',
                examples=[OpenApiExample('Ejemplo', value='2024-01-01')]
            ),
            OpenApiParameter(
                name='fecha_hasta',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha final para el resumen (YYYY-MM-DD)',
                examples=[OpenApiExample('Ejemplo', value='2024-01-31')]
            ),
        ],
        responses={
            200: {
                'description': 'Resumen financiero exitoso',
                'examples': [
                    {
                        'resumen': {
                            'total_ingresos': 5000.0,
                            'total_gastos': 2500.0,
                            'balance': 2500.0,
                            'total_movimientos': 10,
                            'movimientos_ingresos': 5,
                            'movimientos_gastos': 5
                        },
                        'rango_fechas': {
                            'fecha_desde': '2024-01-01',
                            'fecha_hasta': '2024-01-31'
                        }
                    }
                ]
            }
        },
        tags=['reportes']
    )
    @action(detail=False, methods=['get'])
    def resumen(self, request):
        """
        Obtiene un resumen de ingresos y gastos en un rango de fechas.
        
        Parámetros:
        - fecha_desde: fecha inicial (YYYY-MM-DD)
        - fecha_hasta: fecha final (YYYY-MM-DD)
        """
        fecha_desde = request.query_params.get('fecha_desde', None)
        fecha_hasta = request.query_params.get('fecha_hasta', None)
        
        queryset = MovimientoFinanciero.objects.filter(user=request.user)
        
        if fecha_desde:
            try:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha__gte=fecha_desde)
            except ValueError:
                pass
        
        if fecha_hasta:
            try:
                fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha__lte=fecha_hasta)
            except ValueError:
                pass
        
        # Calcular totales
        total_ingresos = queryset.filter(categoria='ingreso').aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        total_gastos = queryset.filter(categoria='gasto').aggregate(
            total=Sum('monto')
        )['total'] or 0
        
        balance = total_ingresos - total_gastos
        
        # Estadísticas adicionales
        total_movimientos = queryset.count()
        movimientos_ingresos = queryset.filter(categoria='ingreso').count()
        movimientos_gastos = queryset.filter(categoria='gasto').count()
        
        return Response({
            'resumen': {
                'total_ingresos': float(total_ingresos),
                'total_gastos': float(total_gastos),
                'balance': float(balance),
                'total_movimientos': total_movimientos,
                'movimientos_ingresos': movimientos_ingresos,
                'movimientos_gastos': movimientos_gastos,
            },
            'rango_fechas': {
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta,
            }
        })
    
    @extend_schema(
        summary="Generar reporte mensual",
        description="Genera un reporte detallado de movimientos para un mes específico",
        parameters=[
            OpenApiParameter(
                name='año',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Año del reporte',
                examples=[OpenApiExample('Ejemplo', value=2024)]
            ),
            OpenApiParameter(
                name='mes',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Mes del reporte (1-12)',
                examples=[OpenApiExample('Ejemplo', value=1)]
            ),
        ],
        responses={
            200: {
                'description': 'Reporte mensual exitoso',
                'examples': [
                    {
                        'reporte_mensual': {
                            'año': 2024,
                            'mes': 1,
                            'total_ingresos': 5000.0,
                            'total_gastos': 2500.0,
                            'balance': 2500.0,
                            'total_movimientos': 10,
                            'top_movimientos': []
                        }
                    }
                ]
            },
            400: {
                'description': 'Parámetros inválidos',
                'examples': [
                    {'error': 'Año y mes deben ser números válidos'}
                ]
            }
        },
        tags=['reportes']
    )
    @action(detail=False, methods=['get'])
    def reporte_mensual(self, request):
        """
        Genera un reporte mensual de movimientos.
        
        Parámetros:
        - año: año del reporte (YYYY)
        - mes: mes del reporte (1-12)
        """
        año = request.query_params.get('año', date.today().year)
        mes = request.query_params.get('mes', date.today().month)
        
        try:
            año = int(año)
            mes = int(mes)
            
            # Filtrar por año y mes
            queryset = MovimientoFinanciero.objects.filter(
                user=request.user,
                fecha__year=año,
                fecha__month=mes
            )
            
            # Calcular totales
            total_ingresos = queryset.filter(categoria='ingreso').aggregate(
                total=Sum('monto')
            )['total'] or 0
            
            total_gastos = queryset.filter(categoria='gasto').aggregate(
                total=Sum('monto')
            )['total'] or 0
            
            balance = total_ingresos - total_gastos
            
            # Top 5 movimientos por monto
            top_movimientos = queryset.order_by('-monto')[:5]
            
            return Response({
                'reporte_mensual': {
                    'año': año,
                    'mes': mes,
                    'total_ingresos': float(total_ingresos),
                    'total_gastos': float(total_gastos),
                    'balance': float(balance),
                    'total_movimientos': queryset.count(),
                    'top_movimientos': MovimientoFinancieroSerializer(top_movimientos, many=True).data
                }
            })
            
        except ValueError:
            return Response(
                {'error': 'Año y mes deben ser números válidos'},
                status=status.HTTP_400_BAD_REQUEST
            )

@extend_schema(
    summary="Información de la API",
    description="Muestra información general sobre la API de movimientos financieros",
    responses={
        200: {
            'description': 'Información de la API',
            'examples': [
                {
                    'mensaje': 'API de Movimientos Financieros',
                    'version': '1.0',
                    'endpoints': {
                        'movimientos': '/api/movimientos/',
                        'resumen': '/api/movimientos/resumen/',
                        'reporte_mensual': '/api/movimientos/reporte_mensual/',
                        'admin': '/admin/',
                    }
                }
            ]
        }
    },
    tags=['información']
)
def inicio(request):
    """
    Vista de inicio que muestra información sobre la API
    """
    return JsonResponse({
        'mensaje': 'API de Movimientos Financieros',
        'version': '1.0',
        'endpoints': {
            'movimientos': '/api/movimientos/',
            'resumen': '/api/movimientos/resumen/',
            'reporte_mensual': '/api/movimientos/reporte_mensual/',
            'registro': '/api/registro/',
            'login': '/api/login/',
            'swagger': '/api/docs/',
            'redoc': '/api/redoc/',
        },
        'operaciones': {
            'GET /api/movimientos/': 'Listar todos los movimientos',
            'POST /api/movimientos/': 'Crear un nuevo movimiento',
            'GET /api/movimientos/{id}/': 'Obtener un movimiento específico',
            'PUT /api/movimientos/{id}/': 'Actualizar un movimiento',
            'DELETE /api/movimientos/{id}/': 'Eliminar un movimiento',
            'GET /api/movimientos/resumen/': 'Obtener resumen de ingresos y gastos',
            'GET /api/movimientos/reporte_mensual/': 'Generar reporte mensual',
            'POST /api/registro/': 'Registrar un nuevo usuario',
            'POST /api/login/': 'Iniciar sesión',
        },
        'filtros_disponibles': {
            'categoria': 'ingreso o gasto',
            'fecha_desde': 'YYYY-MM-DD',
            'fecha_hasta': 'YYYY-MM-DD',
            'ordenar_por': 'fecha, monto, fecha_creacion',
            'orden': 'asc o desc',
        },
        'documentacion': {
            'swagger': 'Interfaz interactiva para probar la API',
            'redoc': 'Documentación alternativa más limpia',
            'schema': 'Esquema OpenAPI en formato JSON'
        }
    })

@extend_schema(
    summary="Registro de usuario",
    description="Permite crear un nuevo usuario en el sistema.",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'password': {'type': 'string'},
                'email': {'type': 'string'},
            },
            'required': ['username', 'password']
        }
    },
    responses={
        201: {
            'description': 'Usuario creado correctamente',
            'examples': [
                {'token': 'TOKEN_GENERADO'}
            ]
        },
        400: {
            'description': 'Datos inválidos',
        }
    },
    tags=['usuarios']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def registro_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    if not username or not password:
        return Response({'error': 'Username y password son obligatorios.'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'El usuario ya existe.'}, status=400)
    user = User.objects.create_user(username=username, password=password, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=201)
