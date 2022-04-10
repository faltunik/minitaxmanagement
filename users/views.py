# in-built library import

# django and drf import 
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

# simplejwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# app import
from .serializer import UserSerializer


UserModel = get_user_model()




# Create your views here. 
# for login

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['id'] = user.id
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



# create taxt payer
@api_view(['POST'])
def create_tax_payer(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('Error is : ', e)
            message = {'detail': f'Error is {e}'}
            return Response(message, status = status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create tax-accountant
@api_view(['POST'])
def create_tax_accountant(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('Error is : ', e)
            message = {'detail': f'Error is {e}'}
            return Response(message, status = status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# View and List tax payers
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def list_tax_payers(request):
    print('user-typpe is:', request.user.user_type)
    if request.user.user_type == 'tax-payer':
        return Response(status=status.HTTP_403_FORBIDDEN)
    tax_payer = UserModel.taxpayermanager.all()
    serializer = UserSerializer(tax_payer, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





