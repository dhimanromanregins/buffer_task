from django.urls import path, include
from .views import *


urlpatterns = [
    path('home', items_display, name="home"),
    path('update_order', update_item, name='update'),
    path('additem', ItemAdd.as_view(), name='additem'),
]
