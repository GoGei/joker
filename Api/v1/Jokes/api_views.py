from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from .serializers import JokeSendToEmailSerializer, JokeSendToTelegramSerializer


class BaseJokeSendAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = None
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'v1/Jokes/send_joke_form.html'
    style = {'template_pack': 'rest_framework/vertical/'}

    def get_user_data(self):
        data = {
            'email': 'example@gmail.com',
            'nickname': '@your_nickname'
        }
        user = self.request.user
        if user.is_authenticated:
            data.update({'email': user.email,
                         'nickname': f'@{user.username}'})
        return data

    def get(self, request):
        data = self.get_user_data()
        serializer = self.serializer_class(data)
        return Response({'serializer': serializer, 'style': self.style})


class JokeSendToEmailAPIView(BaseJokeSendAPIView):
    serializer_class = JokeSendToEmailSerializer


class JokeSendToTelegramAPIView(BaseJokeSendAPIView):
    serializer_class = JokeSendToTelegramSerializer
