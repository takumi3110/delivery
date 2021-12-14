from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .models import Category, Item, Menu, SetMenu, OrderItem, Order, Invoice


class CategoryListView(ListView):
	model = Category
	template_name = 'sukiya/category_list.html'


class ItemListView(ListView):
	model = Item
	template_name = 'sukiya/Item_list.html'

	def get_queryset(self):
		obj = Item.objects.filter(category_id=self.kwargs['pk'])
		qs = obj.order_by('pk')
		return qs

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		return get_context(context)


class MenuListView(ListView):
	model = Menu
	template_name = 'sukiya/menu_list.html'

	def get_queryset(self):
		obj = Menu.objects.filter(item_id=self.kwargs['pk']).order_by('calorie')
		return obj

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		item = Item.objects.get(pk=self.kwargs['pk'])
		context['item'] = item
		return get_context(context)


def get_context(context):
	set_menu_list = SetMenu.objects.all()
	size_choices = Menu.size_choice
	size_dict = {}
	for size in size_choices:
		size_dict[size[0]] = size[1]
	context['size_dict'] = size_dict
	context['set_menu_list'] = set_menu_list
	return context
