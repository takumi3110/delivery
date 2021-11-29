from django.contrib import admin
from .models import Category, Menu, Item


class ItemInline(admin.TabularInline):
	model = Item
	extra = 0


admin.site.register(Category)


class MenuAdmin(admin.ModelAdmin):
	inlines = [ItemInline]


admin.site.register(Menu, MenuAdmin)


class ItemAdmin(admin.ModelAdmin):
	list_display = ('menu', 'size', 'tax_price',)
	list_filter = ('size',)

admin.site.register(Item, ItemAdmin)