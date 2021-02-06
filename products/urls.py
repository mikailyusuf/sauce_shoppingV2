from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from .views import UploadProductView, ProductDetail, GetProductsView, GetProductsCategoryView

urlpatterns = [
    path('upload_product', UploadProductView.as_view(), name="upload-product"),
    path('product_detail/<int:pk>/', ProductDetail.as_view(), name="upload-product"),
    path('products', GetProductsView.as_view(), name="products"),
    path('products_category', GetProductsCategoryView.as_view(), name="products"),

]