from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy

from .models import Category, Item, Menu, OrderItem, Order, Invoice


class CategoryListView(ListView):
	model = Category
	template_name = 'sukiya/category_list.html'
