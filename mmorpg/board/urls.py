from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='post_all'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('response/add/', ResponseCreateView.as_view(), name='response_create'),
    path('private/', PrivateTemplateView.as_view(), name='private_page'),
    path('private/accepted/', Accepted, name='accepted_page'),
    path('private/unaccepted/', Unaccepted, name='unaccepted_page'),
    path('private/responseview/', Responseview, name='responseview_page'),
    path('private/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response_delete'),
]