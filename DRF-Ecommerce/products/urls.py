from .views import *
from django.urls import path, include
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register(r'views', AddressView, )

urlpatterns = [
    path('', CollectionsView.as_view(), name='collections_detail'),
    path('<int:pk>', CollectionsView.as_view(), name='collections_by_id'),
    path('product_detail/', ProductDetail.as_view(), name='products_detail'),
    path('product_detail/<int:pk>', ProductDetail.as_view(), name='products_detail'),
    path('category/', CategoryView.as_view(), name='category_view'),
    path('category/<int:pk>', CategoryView.as_view(), name='category_view_by_id'),
    path('subcategory/', SubCategoryView.as_view(), name='subcategory_view'),
    path('subcategory/<int:pk>', SubCategoryView.as_view(), name='subcategory_view_by_id'),
    path('cart/', AddToCartView.as_view(), name='cart_view'),
    path('cart/<int:pk>', AddToCartView.as_view(), name='cart_view'),
    path('address/', AddressView.as_view(), name='address view'),
    path('address/<int:pk>', AddressView.as_view(), name='address view')

]
