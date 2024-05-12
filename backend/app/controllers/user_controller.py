from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status


from app.models import User 
from app.serializers import UserSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UserAPIView(APIView):
    def get(self, request, id=0):
        if id == 0:
            users = User.objects.all()
            users_serializer = UserSerializer(users, many=True)
            return Response(users_serializer.data)
        else:
            try:
                user = User.objects.get(userId=id)
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data)
            except User.DoesNotExist:
                raise NotFound("Article not found")
    
    def post(self, request):
        user_data = JSONParser().parse(request)
        users_serializer = UserSerializer(data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return Response("Added Successfully")
        return Response("Failed to Add", status=400)
    
    def put(self, request, id):
        user_data = JSONParser().parse(request)
        try:
            user = User.objects.get(pk=id)
            users_serializer = UserSerializer(user, data=user_data)
            if users_serializer.is_valid():
                users_serializer.save()
                return Response("Updated Successfully")
            return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            raise NotFound("User not found")
    
    def delete(self, request, id):
        try:
            user = User.objects.get(userId=id)
            user.delete()
            return Response("Deleted Successfully")
        except User.DoesNotExist:
            raise NotFound("Article not found")

