from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Exercise, ExerciseResult, Conversation, Message
from .serializers import ExerciseSerializer, ExerciseResultSerializer, ConversationSerializer, MessageSerializer


# ============================
# 📘 EJERCICIOS (CRUD completo)
# ============================
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all().order_by('-created_at')
    serializer_class = ExerciseSerializer
    permission_classes = [AllowAny]


# ==========================================
# 🧾 RESULTADOS DE LOS EJERCICIOS (CRUD)
# ==========================================
class ExerciseResultViewSet(viewsets.ModelViewSet):
    queryset = ExerciseResult.objects.all().order_by('-submitted_at')
    serializer_class = ExerciseResultSerializer
    permission_classes = [AllowAny]

    # 🔹 Eliminamos el filtro antiguo por "student"
    def get_queryset(self):
        return ExerciseResult.objects.all()


# ==================================
# 💬 CHATBOT SIMPLIFICADO
# ==================================
@api_view(['POST'])
@permission_classes([AllowAny])
def chat_interact(request):
    data = request.data
    text = data.get('message', '').strip()
    user_id = data.get('user_id', 'anon')

    if not text:
        return Response({'detail': 'message required'}, status=status.HTTP_400_BAD_REQUEST)

    # Buscar o crear conversación del "usuario"
    conv, _ = Conversation.objects.get_or_create(user_identifier=str(user_id))

    # Lógica simple del chatbot
    t = text.lower()
    reply = "No entendí, intenta preguntar sobre ejercicios."

    if 'hola' in t:
        reply = "¡Hola! ¿Qué tema quieres practicar?"
    elif 'ejercicio' in t:
        reply = "Puedes ir a la sección de Ejercicios para comenzar un reto."
    elif 'gracias' in t:
        reply = "¡De nada! Estoy aquí para ayudarte."
    elif 'resultado' in t:
        reply = "Puedes ver tus resultados en la sección de 'Resultados'."

    msg = Message.objects.create(
        conversation=conv,
        sender=f"user_{user_id}",
        text=text,
        bot_response=reply
    )

    serializer = MessageSerializer(msg)
    return Response({'reply': reply, 'message': serializer.data})
