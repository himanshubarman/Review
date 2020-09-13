from django.contrib import admin
from django.urls import path
from reviewapp.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('check/', check),
    path('login/', user_login, name="login"),
    path('logout/',user_logout , name="logout"),
    path('signup/',sign_up , name="signup"),
    path('search/',search , name="search"),
    path('search_result/',search_result , name="search_result"),
    path('review/<str:pk>/', review, name='review'),
    path('review_submission/', review_submission, name='review_submission'),
    path('evaluation_of_review/', evaluation_of_review.as_view(), name='evaluation_of_review'),
    path('activity_log/', activity_log.as_view(), name='activity_log'),
    path('product_review/<str:pk>/', product_review.as_view(), name='product_review'),
]