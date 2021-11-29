from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    fields = [
        ('username', 'Position'),
        ('screenname'),
        ('Department'),
        ('email'),
        ('is_staff', 'is_superuser',),
        ('groups'),
    ]

    list_display = (
        'username',
        'screenname',
        'Department',
        'Position',
        'is_staff',
        'is_superuser',
    )
    list_filter = ('Department',)
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)