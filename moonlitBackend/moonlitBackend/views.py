from django.http import HttpResponse
from django.conf import settings
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class LoginView(APIView):
    def post(self, request):
        print(request.data)
        username = request.data.get('id')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=400)


def get_image(request, image_name):
    image_path = os.path.join(settings.MEDIA_ROOT, 'posted_images', image_name)
    with open(image_path, 'rb') as f:    
        return HttpResponse(f.read(), content_type="image/jpeg")