# commerce/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
]


urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),  # Blog detail view
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('cart/', views.cart_view, name='cart'),
    path('register/', views.register_view, name='register'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('allauth.urls')),  # Include the allauth URLs for authentication
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),  # Add a URL for the sign-up view
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
]
