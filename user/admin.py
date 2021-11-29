from django.contrib import admin
from .models import User, conf, Unit, Unit_Member, Unit_history, Unit_request


class MemberInline(admin.TabularInline):
    model = Unit_Member
    extra = 0


class ConfInline(admin.TabularInline):
    model = conf
    readonly_fields = ('Default_stt', 'Default_conf',)


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
    inlines = [ConfInline, MemberInline]


admin.site.register(User, UserAdmin)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin')
    list_filter = ('name',)
    inlines = [MemberInline]


admin.site.register(Unit, UnitAdmin)


class MemberAdmin(admin.ModelAdmin):
    list_display = ('unit', 'user')


admin.site.register(Unit_Member, MemberAdmin)


class confAdmin(admin.ModelAdmin):
    list_display = ("user", "get_Default_stt_display", "Default_conf")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.readonly_fields = ("user", "Default_stt", "Default_conf",)
        return self.changeform_view(request, object_id, form_url, extra_context)


admin.site.register(conf, confAdmin)


class historyAdmin(admin.ModelAdmin):
    list_display = ("get_status_display", "Date", "user", "target",)
    list_filter = ("Date", "status",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.readonly_fields = ("status", "Date", "user", "target", "memo",)
        return self.changeform_view(request, object_id, form_url, extra_context)


admin.site.register(Unit_history, historyAdmin)


class request_admin(admin.ModelAdmin):
    list_display = ('user', 'join_Unit', 'Date',)
    list_filter = ('Date',)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.readonly_fields = ("user", "join_Unit", "Date", "end_Date", "memo", "Flg",)
        return self.changeform_view(request, object_id, form_url, extra_context)


admin.site.register(Unit_request, request_admin)
