from django.urls import path
from . import views

app_name = 'sukiya'
urlpatterns = [
	path('', views.CategoryListView.as_view(), name='index'),
	path('item/<int:pk>', views.ItemListView.as_view(), name='item_list'),
	path('menu/<int:pk>', views.MenuListView.as_view(), name='menu_list')
]
