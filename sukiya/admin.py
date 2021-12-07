from django.contrib import admin
from .models import Category, Item, Menu, OrderItem, Order, Invoice


class MenuInline(admin.TabularInline):
	model = Menu
	extra = 0
	readonly_fields = ('item', 'size', 'tax_price', 'price', 'tax', 'calorie')


class ItemAdmin(admin.ModelAdmin):
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


admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order)
