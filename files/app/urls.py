from django.urls import re_path
from app import views

urlpatterns = [
    # 图片分片上传
    re_path('load/',views.Api.as_view(),name='load/'),

    # 上传成功合并
    re_path('hebing/',views.Up.as_view(),name='hebing/'),

    re_path('zhan/', views.Zhan.as_view(), name='zhan/'),
]
