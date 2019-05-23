from django.urls import path

from . import views

app_name = 'shop'


urlpatterns = [
    path('', views.main_view, name='home'),
    path('page/<int:page>/', views.main_view),
    path('login/', views.user_login, name="login"),
    path('register/', views.user_registration, name="register"),
    path('waranty/', views.waranty, name="waranty"),
    path('add_to_basket/<int:pk>', views.add_to_basket, name='add_to_basket'),
    path('remove_from_basket', views.remove, name='remove'),
    path('logout/', views.user_logout, name="logout"),
    path('contacts/', views.contacts, name="contacts"),
    path('reviews/', views.rewiews, name="reviews"),
    path('order/', views.order, name="order"),
    path('status/', views.status, name="status"),
    path('order_confirm/', views.order_confirm, name="order_confirm"),
    path('basket/', views.basket, name="basket"),
    path('<int:pk>', views.details, name="detail"),
    path('allreviews/<int:pk>', views.all_reviews, name="allreviews"),
]