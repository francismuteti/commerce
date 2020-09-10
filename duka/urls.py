from django.urls import path
from . import views
app_name ='duka'
urlpatterns = [
    path('', views.home, name='home'),
    path('mycart/', views.cartPage, name='cart'),
    path('product/', views.shopGrid, name='shop'),
    path('contact/', views.Contact, name='contact'),
    path('product/<int:id>/',views.product, name='details'),
    path('add-to-cart/<int:id>/',views.AddToCart, name='cart_add'),
    path('remove-from-cart/<int:id>/',views.removeFromCart, name='cart_remove'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('update-profile/',views.updateProfile, name='update-profile'),
]