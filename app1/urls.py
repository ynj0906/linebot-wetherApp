from django.urls import path
from . import views

app_name = "app1"
urlpatterns =[
    path("hello", views.Hello.as_view(),name="hello" ),
    path("sample", views.Sample.as_view(), name="sample"),
    path("handle_push_message", views.Hello.as_view(),name="handle_push_message" ),
]