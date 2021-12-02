from django.urls import path
from . import views

app_name = 'sukiya'
urlpatterns = [
	path('', views.CategoryListView.as_view(), name='index'),
]
