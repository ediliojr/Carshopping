from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import Carro
from .serializers import CarroSerializer, UserSerializer
from django.core.files.storage import default_storage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

# Create your views here.


@csrf_exempt
def userAPI(request,pk=0):
    if request.method== 'GET':
        if pk==0:
            carros = Carro.objects.filter(is_active=True)
           
            carros_serializer= CarroSerializer(carros,many=True)
            return JsonResponse(carros_serializer.data,safe=False)
        else:
            carro = Carro.objects.get(id=pk)
            data = {
                "Id": carro.id,
                "Nome": carro.nome ,
                "Marca": carro.marca ,
                "Modelo": carro.modelo ,
                "Preco": carro.preco ,
                "Kilometro": carro.kilometro ,
                "Tempo_post": carro.tempo_post ,
                "Tags": carro.tags,
           
                "is_active": carro.is_active ,
               
            'url': request.build_absolute_uri()
        }
            return JsonResponse(data)
       
        
    elif request.method=='POST':
        
        user_data = JSONParser().parse(request)
        carros_serializer = CarroSerializer(data=user_data)
        
        if carros_serializer.is_valid():
            carros_serializer.save()
            return JsonResponse("Criado com sucesso",safe=False)
        return JsonResponse("Criação falhou", safe=False)
        
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)

        try:
            user = Carro.objects.get(UserId=user_data.get('Id'))
            carros_serializer = CarroSerializer(user, data=user_data)

            if carros_serializer.is_valid():
                carros_serializer.save()
                return JsonResponse('Atualizado com sucesso', safe=False)

            return JsonResponse('Atualização falhou', safe=False)

        except Carro.DoesNotExist:
            return JsonResponse({'error': 'Carro matching query does not exist.'})

    elif request.method == 'DELETE':
        try:
            user = Carro.objects.get(UserId=pk)
            user.is_active = False  # Soft delete by marking user as inactive
            user.save()
            return JsonResponse("Deactivated successfully", safe=False)
        except Carro.DoesNotExist:
            return JsonResponse({'error': 'User matching query does not exist.'})
        
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response