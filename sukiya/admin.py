from django.contrib import admin
from .models import Category, Item, Menu, SetMenu, OrderItem, Order, Invoice


class MenuInline(admin.TabularInline):
	model = Menu
	extra = 0
	fields = ('item', 'size', 'tax_price', 'price', 'calorie')
	readonly_fields = ('price', 'tax')
	ordering = ('calorie',)


class SetMenuAdmin(admin.ModelAdmin):
	list_display = ('name', 'price')
	list_display_links = ('name', 'price')
	list_filter = ('name',)
	search_fields = ('name', 'price')


class ItemAdmin(admin.ModelAdmin):
	inlines = [MenuInline]
	extra = 0


class ItemInline(admin.TabularInline):
	model = Item
	extra = 0


class CategoryAdmin(admin.ModelAdmin):
	inlines = [MenuInline]


class MenuAdmin(admin.ModelAdmin):
	list_display = ('item', 'size', 'tax_price',)
	list_filter = ('size',)

	def change_view(self, request, object_id, form_url='', extra_context=None):
		self.readonly_fields = ('item', 'size', 'tax_price', 'price', 'tax', 'calorie')
		return self.changeform_view(request, object_id, form_url, extra_context)


class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('menu', 'quantity', 'price')
	list_display_links = ('menu', 'quantity', 'price')
	list_filter = ('menu', 'quantity', 'price')
	search_fields = ('menu', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
	list_display = ('table', 'number', 'order_item', 'total_price', 'date', 'ordered')
	list_display_links = ('table', 'number', 'order_item', 'total_price', 'date', 'ordered')
	list_filter = ('table', 'number', 'order_item', 'total_price', 'date', 'ordered')
	search_fields = ('table', 'number', 'order_item', 'total_price', 'date', 'ordered')


class InvoiceAdmin(admin.ModelAdmin):
	list_display = ('contact_user', 'order', 'leaved_date')
	list_display_links = ('contact_user', 'order', 'leaved_date')
	list_filter = ('contact_user', 'order', 'leaved_date')
	search_fields = ('contact_user', 'order', 'leaved_date')

	def change_view(self, request, object_id, form_url='', extra_context=None):
		self.readonly_fields = ('menu', 'size', 'tax_price', 'price', 'tax', 'calorie')
		return self.changeform_view(request, object_id, form_url, extra_context)

	def add_view(self, request, form_url='', extra_context=None):
		self.readonly_fields = ()
		return self.changeform_view(request, None, form_url, extra_context)


admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(SetMenu, SetMenuAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order)
