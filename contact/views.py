import json
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings


@api_view(["POST"])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def contact_view(request):
    data = request.data

    # 🔥 CASO ESPECIAL RENDER
    if "_content" in data:
        try:
            data = json.loads(data["_content"])
        except json.JSONDecodeError:
            return Response(
                {"error": "JSON inválido"},
                status=400
            )

    name = data.get("from_name")
    email = data.get("from_email")
    message = data.get("message")

    if not name or not email or not message:
        return Response(
            {
                "error": "Todos los campos son obligatorios",
                "data_recibida": data
            },
            status=400
        )

    full_message = f"""
Nombre: {name}
Email: {email}

Mensaje:
{message}
"""

    send_mail(
        subject="Nuevo mensaje desde el portafolio",
        message=full_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )

    return Response(
        {"success": "Mensaje enviado correctamente"},
        status=200
    )
