from django.urls import path
from .views import ArticleAPIView, QuoteAPIView, RegisterView, LoginView, LogoutView, UserAPIView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('user/', UserAPIView.as_view()),
    path('user/<int:id>/', UserAPIView.as_view()),
    
    path('article/', ArticleAPIView.as_view(), name='article-list'),
    path('article/<int:id>/', ArticleAPIView.as_view(), name='article-detail'),

    path('quote/', QuoteAPIView.as_view(), name='quote-list'),
    path('quote/<int:id>/', QuoteAPIView.as_view(), name='quote-detail'),    
]