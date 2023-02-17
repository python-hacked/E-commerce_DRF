from .models import Products, Category, SubCategory, Collections, \
    Cart, User, Address
from .serializers import ProductsSerializer, CategorySerializer, \
    SubCategorySerializer, CollectionSerializer, CartSerializer, AddressSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


# from .serializers import UserSerializer
# Create your views here.


class CollectionsView(APIView):
    """list top deal products"""

    def get(self, request, pk=None):
        category = Category.objects.filter(collections_id=pk)
        for i in category:
            products = Products.objects.filter(sub_category_id=i.id).order_by("?")[0:10]
        if pk:
            collection = Collections.objects.filter(pk=pk)
            print("category", category)
            if not collection:
                return Response({"status": "category not found"},
                                status=status.HTTP_404_NOT_FOUND)
            collection_serializer = CollectionSerializer(collection, many=True)
            category_serializer = CategorySerializer(category, many=True)
            products = ProductsSerializer(products, many=True)
            context_with_id = {'collections': collection_serializer.data,
                               'category': category_serializer.data,
                               'products': products.data}
            return Response(context_with_id, status=status.HTTP_200_OK)
        top_deal = Products.objects.filter().order_by("?")[0:10]
        product_serializer = ProductsSerializer(top_deal, context={"request": request}, many=True)

        collect_serializer = CollectionSerializer(Collections.objects.all(),
                                                  context={"request": request}, many=True)
        context = {'collections': collect_serializer.data,
                   'products': product_serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    """product detail"""

    def get(self, request, pk=None):
        if pk:
            product = Products.objects.filter(pk=pk)
            if not product:
                return Response({"status": "invalid user or id"})
            serializer = ProductsSerializer(Products.objects.get(pk=pk))
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        product = Products.objects.all().order_by('id')
        serializer = ProductsSerializer(product, context={"request": request}, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class CategoryView(APIView):
    """ Category view """

    def get(self, request, pk=None):
        if pk:
            category = Category.objects.get(pk=pk)
            if not category:
                return Response({"status": "category not found"},
                                status=status.HTTP_404_NOT_FOUND)
            serializer = CategorySerializer(category, context={"request": request}, )
            return Response(serializer.data, status=status.HTTP_200_OK)
        top_deal = Products.objects.filter().order_by("?")[0:20]

        cat_serializer = CategorySerializer(Category.objects.all().order_by('id'),
                                            context={"request": request}, many=True)
        product_serializer = ProductsSerializer(top_deal, context={"request": request}, many=True)
        context = {'products': product_serializer.data,
                   'categories': cat_serializer.data
                   }

        return Response(context, status=status.HTTP_200_OK)


class SubCategoryView(APIView):
    """ Sub categories view """

    def get(self, request, pk=None):
        if pk:
            sub_category = SubCategory.objects.filter(pk=pk)
            products = Products.objects.filter(sub_category_id=pk).order_by("?")[0:10]

            if not sub_category:
                return Response({"status": "product not available"},
                                status=status.HTTP_404_NOT_FOUND)
            sub_category_serializer = SubCategorySerializer(sub_category, many=True)
            products_serializer = ProductsSerializer(products, context={"request": request}, many=True)
            context_with_id = {'sub_category': sub_category_serializer.data,
                               'products': products_serializer.data}

            return Response(context_with_id, status=status.HTTP_200_OK)
        top_deal = Products.objects.filter().order_by("?")[0:10]
        product_serializer = ProductsSerializer(top_deal, context={"request": request}, many=True)

        cat_serializer = SubCategorySerializer(SubCategory.objects.all().order_by('id'), many=True)
        context = {'categories': cat_serializer.data,
                   'products': product_serializer.data
                   }
        return Response(context, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    """add item to cart"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        """cart item get detail"""
        if pk:
            cart = Cart.objects.filter(pk=pk)
            if not cart:
                return Response({'error': 'product not available'}, status=status.HTTP_400_BAD_REQUEST)
            cart = Cart.objects.get(pk=pk)
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        """add item in cart"""
        if pk:
            if Cart.objects.filter(pk=pk).exists():
                return Response({'exist': 'product is already exist in cart'}, status=status.HTTP_400_BAD_REQUEST)
            products = Products.objects.get(pk=pk)
            user1 = User.objects.get(email=request.user)
            print("user_id", user1.id)
            serializer = CartSerializer(data={'user': user1.id, 'products': products.id})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'product is not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """delete cart item """
        if pk:
            cart = Cart.objects.filter(pk=pk)
            if not cart:
                return Response({'status': 'cart id not found'}, status=status.HTTP_404_NOT_FOUND)
            cart.delete()
            return Response({"data": "item removed"}, status=status.HTTP_200_OK)
        return Response({'error': 'cart id not found'})


class AddressView(APIView):
    """ user can create address , view, delete and update address """
    # permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        """ get address detail"""
        if pk:
            address = Address.objects.filter(pk=pk)
            if not address:
                return Response({'error': 'address not available'}, status=status.HTTP_400_BAD_REQUEST)
            address = Address.objects.get(pk=pk)
            serializer = CartSerializer(address, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        address = Address.objects.all()
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ create address"""
        data = {}
        user1 = User.objects.get(email=request.user)
        data['user'] = user1.id
        data.update(request.data)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'address is not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """delete address """
        if pk:
            address = Address.objects.filter(pk=pk)
            if not address:
                return Response({'status': 'address not found'}, status=status.HTTP_404_NOT_FOUND)
            address.delete()
            return Response({"data": "address removed"}, status=status.HTTP_200_OK)
        return Response({'error': 'address id not found'})

    # def post(self, request):
    #     print(request.data)
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def patch(self, request, pk=None):
    #     if pk:
    #         try:
    #             serializer_data = UserSerializer(User.objects.get(id=pk), data=request.data, partial=True)
    #         except Exception as e:
    #             return HttpResponse(e)
    #         print(serializer_data)
    #         if serializer_data.is_valid():
    #             serializer_data.save()
    #             return Response({"status": "success", "data": serializer_data.data})
    #         else:
    #             return Response({"status": "error", "data": serializer_data.errors})
    #     else:
    #         return Response({"status": "invalid detail or attribute"})
    #
    # def delete(self, request, pk=None):
    #     if pk:
    #         user = User.objects.filter(pk=pk)
    #         if not user:
    #             return Response({'status': 'page not found'})
    #         user.delete()
    #         return Response({"status": "success", "data": "Item Deleted"})
    #     else:
    #         return Response({'error': 'user id not found'})
