from django.urls import path
from myshop.views import *

urlpatterns = [
    path('list/', PorductList),
    path('detail/<int:post_id>/', PorductDetail),
    path('cartCreate/<int:pdt_id>/', CartCreate),
    path('cartList/', CartList),
    path('cartDelete/<int:cart_id>/', CartDelete),
    path('cartOrderCreate/', cartOrderCreate),
    path('buyNow/<int:post_id>/', buyNow),
    path('orderList/', orderList)
]
