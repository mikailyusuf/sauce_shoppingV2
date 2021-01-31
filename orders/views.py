from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response

from rest_framework import status, permissions, views, generics
from rest_framework.views import APIView

from orders.models import Orders, ShippingAddress, Cart
from orders.serializers import OrdersSerializer, ShippingAdrressSerializer, CartSerializer
from products.models import Products


class OrdersDetailsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrdersSerializer

    def get_object(self, pk):
        try:
            return Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = OrdersSerializer(snippet)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = OrdersSerializer(snippet, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateOrderView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrdersSerializer

    def post(self, request):
        user = request.user
        product_id = request.data['product']
        product = Products.objects.get(id=product_id)
        print(str(product))
        units = request.data['units']
        shipping_address = request.data['shipping_address']
        ship = ShippingAddress.objects.get(id=shipping_address)
        print(str(ship))
        try:
            order = Orders.objects.create(user=user, product=product, units=units, shipping_address=ship)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # self.serializer_class(order)
        # self.serializer_class.data,
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        try:
            orders = Orders.objects.filter(user=user)
            serializer = self.serializer_class(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except orders.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ShippingAdressView(generics.GenericAPIView):
    serializer_class = ShippingAdrressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        country = request.data['country']
        state = request.data['state']
        address = request.data['address']
        postal_code = request.data['postal_code']
        phone_number = request.data['phone_number']
        try:
            order = ShippingAddress.objects.create(user=user, country=country,
                                                   state=state, postal_code=postal_code,
                                                   address=address, phone_number=phone_number)
            serializer = self.serializer_class(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            message = {'error': str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        try:
            address = ShippingAddress.objects.filter(user=user)
            serializer = self.serializer_class(address, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ShippingAddress.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        address = ShippingAddress.objects.filter(user=user).delete()
        return Response(status=status.HTTP_200_OK)


class CartView(APIView):

    def post(self, request):
        user = request.user
        product_id = request.data['product']
        try:
            product = Products.objects.get(id=product_id)
            cart = Cart.objects.create(user=user, product=product)
            cart_data = CartSerializer(cart)

            return Response(cart_data.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            message = {
            "error":str(e)
            }
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        try:
            orders = Cart.objects.filter(user=user)
            serializer = self.serializer_class(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except orders.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
