from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from rest_framework import status
from order.models import*  
from .serializers import *

@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)  
    if user.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create(
                email=data['email'],
                username=data['username'],
                password= make_password(data['password']),
                
            )
        
            return Response({'details': 'Your Account Registered Successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'This email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'details': 'Successfully logged out.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getorder(request):
    orders = Order.objects.all()
    data = OrderSerializers(orders, many=True).data
    return Response({'data':data})

@api_view(['GET'])
def getService(request):
    services = Service.objects.all()
    data = ServiceSerializers(services, many=True).data
    return Response({'data':data})

@api_view(['GET'])
def getRating(request):
    Ratings = Rating.objects.all()
    data = RatingSerializers(Ratings, many=True).data
    return Response({'data':data})

@api_view(['GET'])
def getNotification(request):
    notifications = Notification.objects.all()
    data = NotificationSerializers(notifications, many=True).data
    return Response({'data':data})

@api_view(['GET'])
def getorder_id(reques, id):
    orders = Order.objects.get(id=id)
    data = OrderSerializers(orders).data
    return Response({'data':data})

@api_view(['GET'])
def getService_id(request, id):
    services = Service.objects.get(id=id)
    data = ServiceSerializers(services).data
    return Response({'data':data})

@api_view(['GET'])
def getRating_id(request, id):
    Ratings = Rating.objects.get(id=id)
    data = RatingSerializers(Ratings).data
    return Response({'data':data})

@api_view(['GET'])
def getNotification_id(request, id):
    notifications = Notification.objects.get(id=id)
    data = NotificationSerializers(notifications).data
    return Response({'data':data})


@api_view(['POST'])
def createOrder(request):
    user = request.user
    serializer = OrderSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
@api_view(['POST'])
def createService(request):
    
    serializer = ServiceSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def addRating(request):
    user = request.user
    serializer = RatingSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def updateOrder(request, id):
    order = Order.objects.get(id=id)
    serializer = OrderSerializers(instance=order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)
@api_view(['DELETE'])
def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    
    return Response('done')
    
    
