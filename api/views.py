from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Exercise, ExerciseResult, Conversation, Message
from .serializers import ExerciseSerializer, ExerciseResultSerializer, ConversationSerializer, MessageSerializer

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all().order_by('-created_at')
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]  # ajustar según rol en frontend

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ExerciseResultViewSet(viewsets.ModelViewSet):
    queryset = ExerciseResult.objects.all().order_by('-submitted_at')
    serializer_class = ExerciseResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        return ExerciseResult.objects.filter(student=user)

@api_view(['POST'])
@permission_classes([AllowAny])  # cambiar a IsAuthenticated si usas auth
def chat_interact(request):
    data = request.data
    user_id = data.get('user_id')
    text = data.get('message', '')
    if not user_id:
        return Response({'detail': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    conv, _ = Conversation.objects.get_or_create(user_id=user_id)
    # lógica simple de matching
    reply = "No entendí, intenta preguntar sobre ejercicios."
    t = text.lower()
    if 'hola' in t:
        reply = "¡Hola! ¿Qué tema quieres practicar?"
    elif 'ejercicio' in t:
        reply = "Puedes ir a Ejercicios para comenzar un reto."
    msg = Message.objects.create(conversation=conv, sender=f"user_{user_id}", text=text, bot_response=reply)
    serializer = MessageSerializer(msg)
    return Response({'reply': reply, 'message': serializer.data})
