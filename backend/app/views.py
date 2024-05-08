from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework import status


from app.models import User, Article, Quote
from app.serializers import UserSerializer, ArticleSerializer, QuoteSerializer


@method_decorator(csrf_exempt, name='dispatch')
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
            'id': user.userId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')


        responce = Response()

        responce.set_cookie(key='jwt', value=token, httponly=True)

        responce.data = {
            'jwt': token
        }

        return responce
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

# @csrf_exempt
# def UserApi(request, id=0):
#     if request.method == 'GET':
#         if id == 0:
#             users = User.objects.all()
#             users_serializer = UserSerializer(users, many=True)
#             return JsonResponse(users_serializer.data, safe=False)
#         else:
#             user = User.objects.filter(userId=id).first()
#             if user:
#                 user_serializer = UserSerializer(user)
#                 return JsonResponse(user_serializer.data, safe=False)
#             else:
#                 return JsonResponse("User not found", status=404, safe=False)
    
#     elif request.method == 'POST':
#         user_data = JSONParser().parse(request)
#         users_serializer = UserSerializer(data=user_data)
#         if users_serializer.is_valid():
#             users_serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
    
#     elif request.method == 'PUT':
#         user_data = JSONParser().parse(request)
#         user = User.objects.filter(userId=user_data['userId']).first()
#         if user:
#             users_serializer = UserSerializer(user, data=user_data)
#             if users_serializer.is_valid():
#                 users_serializer.save()
#                 return JsonResponse("Updated Successfully", safe=False)
#             return JsonResponse("Failed to Update", status=400, safe=False)
#         else:
#             return JsonResponse("User not found", status=404, safe=False)
    
#     elif request.method == 'DELETE':
#         user = User.objects.filter(userId=id).first()
#         if user:
#             user.delete()
#             return JsonResponse("Deleted Successfully", safe=False)
#         else:
#             return JsonResponse("User not found", status=404, safe=False)


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
            except Article.DoesNotExist:
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
            return Response("Failed to Update", status=400)
        except User.DoesNotExist:
            raise NotFound("Article not found")
    
    def delete(self, request, id):
        try:
            user = User.objects.get(userId=id)
            user.delete()
            return Response("Deleted Successfully")
        except User.DoesNotExist:
            raise NotFound("Article not found")



# @csrf_exempt
# def ArticleApi(request, id=0):
#     if request.method == 'GET':
#         if id == 0:
#             articles = Article.objects.all()
#             articles_serializer = ArticleSerializer(articles, many=True)
#             return JsonResponse(articles_serializer.data, safe=False)
#         else:
#             article = Article.objects.filter(articleId=id).first()
#             if article:
#                 article_serializer = ArticleSerializer(article)
#                 return JsonResponse(article_serializer.data, safe=False)
#             else:
#                 return JsonResponse("User not found", status=404, safe=False)
    
#     elif request.method == 'POST':
#         article_data = JSONParser().parse(request)
#         articles_serializer = ArticleSerializer(data=article_data)
#         if articles_serializer.is_valid():
#             articles_serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
    
#     elif request.method == 'PUT':
#         article_data = JSONParser().parse(request)
#         article = Article.objects.filter(articleId=article_data['articleId']).first()
#         if article:
#             articles_serializer = ArticleSerializer(article, data=article_data)
#             if articles_serializer.is_valid():
#                 articles_serializer.save()
#                 return JsonResponse("Updated Successfully", safe=False)
#             return JsonResponse("Failed to Update", status=400, safe=False)
#         else:
#             return JsonResponse("User not found", status=404, safe=False)
    
#     elif request.method == 'DELETE':
#         article = Article.objects.filter(articleId=id).first()
#         if article:
#             article.delete()
#             return JsonResponse("Deleted Successfully", safe=False)
#         else:
#             return JsonResponse("User not found", status=404, safe=False)
    
@method_decorator(csrf_exempt, name='dispatch')
class ArticleAPIView(APIView):
    def get(self, request, id=0):
        if id == 0:
            articles = Article.objects.all()
            articles_serializer = ArticleSerializer(articles, many=True)
            return Response(articles_serializer.data)
        else:
            try:
                article = Article.objects.get(articleId=id)
                article_serializer = ArticleSerializer(article)
                return Response(article_serializer.data)
            except Article.DoesNotExist:
                raise NotFound("Article not found")
    
    def post(self, request):
        article_data = JSONParser().parse(request)
        articles_serializer = ArticleSerializer(data=article_data)
        if articles_serializer.is_valid():
            articles_serializer.save()
            return Response("Added Successfully")
        return Response("Failed to Add", status=400)
    
    def put(self, request, id):
        article_data = JSONParser().parse(request)
        try:
            article = Article.objects.get(pk=id)

            articles_serializer = ArticleSerializer(article, data=article_data)
            if articles_serializer.is_valid():
                articles_serializer.save()
                return Response("Updated Successfully")
            return Response("Failed to Update", status=400)
        except Article.DoesNotExist:
            raise NotFound("Article not found")
    
    def delete(self, request, id):
        try:
            article = Article.objects.get(articleId=id)
            article.delete()
            return Response("Deleted Successfully")
        except Article.DoesNotExist:
            raise NotFound("Article not found")

# @csrf_exempt
# def QuoteApi (request, id=0):
#     if request.method == 'GET':
#         if id == 0:
#             quotes = Quote.objects.all()
#             quotes_serializer = QuoteSerializer(quotes, many=True)
#             return JsonResponse(quotes_serializer.data, safe=False)
#         else:
#             quote = Quote.objects.filter(quoteId=id).first()
#             if quote:
#                 quote_serializer = QuoteSerializer(quote)
#                 return JsonResponse(quote_serializer.data, safe=False)
#             else:
#                 return JsonResponse("User not found", status=404, safe=False)
    
#     elif request.method == 'POST':
#         quote_data = JSONParser().parse(request)
#         quotes_serializer = QuoteSerializer(data=quote_data)
#         if quotes_serializer.is_valid():
#             quotes_serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
    
#     elif request.method == 'PUT':
#         quote_data = JSONParser().parse(request)
#         quote = Quote.objects.filter(quoteId=quote_data['quoteId']).first()
#         if quote:
#             quotes_serializer = QuoteSerializer(quote, data=quote_data)
#             if quotes_serializer.is_valid():
#                 quotes_serializer.save()
#                 return JsonResponse("Updated Successfully", safe=False)
#             return JsonResponse("Failed to Update", status=400, safe=False)
#         else:
#             return JsonResponse("User not found", status=404, safe=False)
    
#     elif request.method == 'DELETE':
#         quote = Quote.objects.filter(quoteId=id).first()
#         if quote:
#             quote.delete()
#             return JsonResponse("Deleted Successfully", safe=False)
#         else:
#             return JsonResponse("User not found", status=404, safe=False)
@method_decorator(csrf_exempt, name='dispatch')
class QuoteAPIView(APIView):
    def get(self, request, id=0):
        if id == 0:
            quotes = Quote.objects.all()
            quotes_serializer = QuoteSerializer(quotes, many=True)
            return Response(quotes_serializer.data)
        else:
            try:
                quote = Quote.objects.get(quoteId=id)
                quote_serializer = QuoteSerializer(quote)
                return Response(quote_serializer.data)
            except Quote.DoesNotExist:
                raise NotFound("Quote not found")
    
    def post(self, request):
        quote_data = JSONParser().parse(request)
        quotes_serializer = QuoteSerializer(data=quote_data)
        if quotes_serializer.is_valid():
            quotes_serializer.save()
            return Response("Added Successfully")
        return Response("Failed to Add", status=400)
    
    def put(self, request, id):
        quote_data = JSONParser().parse(request)
        try:
            quote = Quote.objects.get(pk=id)

            quotes_serializer = QuoteSerializer(quote, data=quote_data)
            if quotes_serializer.is_valid():
                quotes_serializer.save()
                return Response("Updated Successfully")
            return Response("Failed to Update", status=400)
        except Quote.DoesNotExist:
            raise NotFound("Article not found")
    
    def delete(self, request, id):
        try:
            quote = Quote.objects.get(quoteId=id)
            quote.delete()
            return Response("Deleted Successfully")
        except Quote.DoesNotExist:
            raise NotFound("Article not found")
