from django.contrib import admin
from .models import Category, Menu, Item, Order


class ItemInline(admin.TabularInline):
	model = Item
	extra = 0
	readonly_fields = ('menu', 'size', 'tax_price', 'price', 'tax', 'calorie')


admin.site.register(Category)


class MenuAdmin(admin.ModelAdmin):
	inlines = [ItemInline]


admin.site.register(Menu, MenuAdmin)


class ItemAdmin(admin.ModelAdmin):
	list_display = ('menu', 'size', 'tax_price',)
	list_filter = ('size',)

	def change_view(self, request, object_id, form_url='', extra_context=None):
		self.readonly_fields = ('menu', 'size', 'tax_price', 'price', 'tax', 'calorie')
		return self.changeform_view(request, object_id,form_url,extra_context)

admin.site.register(Item, ItemAdmin)

admin.site.register(Order)