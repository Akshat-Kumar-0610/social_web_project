from django.urls import path
from .views import PostListView,PostDetailView,PostCreateView
from . import views

urlpatterns=[
    path('new/', PostCreateView.as_view(), name='post-create'),
]