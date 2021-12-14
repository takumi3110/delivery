from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
app_name = "user"
urlpatterns = [
	# path('', views.Index.as_view(), name='index'),
	path('', indexView.as_view(), name='index'),
	path('mypage/<int:pk>', views.MyPage.as_view(), name='myp'),
	path('join/<int:uid>', views.group_join, name="group_join"),
	path('reject/<int:uid>', views.group_Reject, name="group_Reject"),
	path('remove/<int:uid>', views.group_remove, name="group_remove"),
]
