from django.urls import path
from .views import LoginAPIView,LogoutAPIview

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIview.as_view(), name='logout'),
    # path('admin_login/', AdminLoginAPIView.as_view(), name='admin_login'),
]
