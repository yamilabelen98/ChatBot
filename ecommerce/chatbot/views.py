from django.shortcuts import render
from django.http import JsonResponse
from .models import Conversation, Message
import json

# Tu diccionario PRODUCTOS permanece igual
from django.shortcuts import render
from django.http import JsonResponse
from .models import Conversation, Message
import json

# Actualizado PRODUCTOS con descripciones
PRODUCTOS = {
    'laptop': {
        'nombre': 'Laptop HP 15.6"',
        'precio': 799.99,
        'descripcion': 'Laptop HP con pantalla de 15.6", procesador Intel Core i5, 8GB de RAM, 256GB SSD. Perfecta para trabajo y estudios con una excelente duración de batería.'
    },
    'telefono': {
        'nombre': 'Smartphone Samsung Galaxy',
        'precio': 499.99,
        'descripcion': 'Samsung Galaxy con pantalla AMOLED de 6.5", cámara triple de 64MP, 128GB de almacenamiento y 6GB de RAM. Incluye cargador rápido y funda protectora.'
    },
    'tablet': {
        'nombre': 'Tablet iPad 10.2"',
        'precio': 329.99,
        'descripcion': 'iPad con pantalla Retina de 10.2", chip A13 Bionic, 64GB de almacenamiento. Compatible con Apple Pencil y Smart Keyboard. Perfecta para creatividad y productividad.'
    },
    'auriculares': {
        'nombre': 'Auriculares Inalámbricos Sony',
        'precio': 149.99,
        'descripcion': 'Auriculares Sony con cancelación de ruido activa, batería de hasta 30 horas, conectividad Bluetooth 5.0 y micrófono incorporado para llamadas.'
    }
}

def chatbot_view(request):
    return render(request, 'chatbot/chat.html')

def get_bot_response(message):
    message = message.lower()
    if 'precio' in message:
        return {
            'text': "Te dejo los productos con los que contamos con sus respectivos precios:",
            'type': 'product_selection',
            'products': PRODUCTOS
        }
    elif message.startswith('precio_producto:'):
        producto_id = message.split(':')[1]
        if producto_id in PRODUCTOS:
            producto = PRODUCTOS[producto_id]
            return {
                'text': f"📱 {producto['nombre']}\n\n" + 
                       f"💰 Precio: ${producto['precio']}\n\n" +
                       f"📝 Descripción: {producto['descripcion']}",
                'type': 'text'
            }
    elif message.startswith('descripcion:'):
        producto_id = message.split(':')[1]
        if producto_id in PRODUCTOS:
            producto = PRODUCTOS[producto_id]
            return {
                'text': f"📝 Descripción: {producto['descripcion']}",
                'type': 'text'
            }
        return {
            'text': "Lo siento, no encontré ese producto.",
            'type': 'text'
        }
    elif 'envio' in message or 'envío' in message:  # Aceptamos ambas formas
        return {
            'text': "¡Hacemos envíos a todo el país! El tiempo de entrega es de 3-5 días hábiles por correo Argentino. También tenemos envíos por motomensajería en el día según de la zona que seas.",
            'type': 'text'
        }
    elif 'pago' in message:
        return {
            'text': "Aceptamos tarjetas de crédito, débito y transferencias bancarias.",
            'type': 'text'
        }
    elif 'hola' in message.lower():  # Aceptamos Hola y hola
        return {
            'text': "¡Hola! ¿En qué puedo ayudarte hoy?",
            'type': 'text'
        }
    else:
        return {
            'text': "¿Podrías ser más específico? Estoy aquí para ayudarte con precios, envíos y métodos de pago.",
            'type': 'text'
        }

def get_conversation_history(request):
    try:
        # Crear una nueva sesión cada vez que se carga la página
        if request.session.session_key:
            request.session.flush()  # Elimina la sesión anterior
        request.session.create()  # Crea una nueva sesión
        
        return JsonResponse({'history': []})  # Retorna un historial vacío
        
    except Exception as e:
        print(f"Error in get_conversation_history: {str(e)}")
        return JsonResponse({'history': [], 'error': str(e)})

def process_message(request):
    if not request.session.session_key:
        request.session.create()
    
    try:
        # Siempre crear una nueva conversación para la sesión actual
        conversation = Conversation.objects.create(
            user_id=request.session.session_key
        )
        
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        Message.objects.create(
            conversation=conversation,
            content=user_message,
            is_bot=False
        )
        
        bot_response = get_bot_response(user_message)
        
        Message.objects.create(
            conversation=conversation,
            content=bot_response['text'],
            is_bot=True
        )
        
        return JsonResponse({
            'message': bot_response['text'],
            'type': bot_response.get('type', 'text'),
            'products': bot_response.get('products', None),
            'conversation_id': conversation.id
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)