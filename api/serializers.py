from rest_framework import serializers
from order. models import*

class SignUpSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ['email','username','password']
     extra_kwargs = {
         'email':{'required':True, 'allow_blank':False},
         'username':{'required':True, 'allow_blank':False},
         'password': {'required':True, 'allow_blank':False},
         
         
     }
class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'status', 'date_created']

class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields ='__all__'

class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields ='__all__' 
        
class NotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields ='__all__' 

#Notification