from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('popular/', views.PopularListView.as_view(), name='popular'),
    path('vote/<int:quote_id>/<str:value>/', views.vote, name='vote'),
    path('add_quote/', views.add_quote, name='add_quote')
]