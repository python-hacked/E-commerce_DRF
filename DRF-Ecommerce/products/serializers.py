
from .models import Products, Category, SubCategory, Collections,\
    Cart, Address
from rest_framework import serializers
from django_countries.serializer_fields import CountryField


class FeatureSerializer(serializers.ModelSerializer):
    """feature model serializer class"""

    class Meta:
        """ product serializer Meta class """
        model = Products
        fields = ['id', 'product_name', 'feature1', 'feature2', 'feature3', 'feature4', 'brand', 'specification',
                  'color', 'size']


class ProductsSerializer(serializers.ModelSerializer):
    """ Product serializer """
    seller = serializers.StringRelatedField(read_only=True)
    photo_url = serializers.SerializerMethodField()

    # feature = serializers.StringRelatedField()

    class Meta:
        """ product serializer Meta class """
        model = Products
        fields = ['id', 'title', 'photo_url', 'seller', 'actual_price',
                  'discount_price', 'feature', 'available_offer', 'description']
        # depth = 1

    def get_photo_url(self, products):
        requests = self.context.get('request')
        photo_url = requests.build_absolute_uri(products.image.url)
        return photo_url


class CategorySerializer(serializers.ModelSerializer):
    """ Category serializer """
    sub_category = serializers.StringRelatedField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        """ Category serializer Meta class """
        model = Category
        fields = ['id', 'name', 'photo_url', 'sub_category']

    def get_photo_url(self, category):
        requests = self.context.get('request')
        photo_url = requests.build_absolute_uri(category.icon.url)
        return photo_url


class SubCategorySerializer(serializers.ModelSerializer):
    """ SubCategory serializer """

    class Meta:
        """ SubCategory serializer Meta class """
        model = SubCategory
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    """ CollectionOfCategories serializer """
    photo_url = serializers.SerializerMethodField()

    class Meta:
        """ CollectionOfCategories serializer Meta class """
        model = Collections
        fields = ['id', 'collection_name', 'photo_url']

    def get_photo_url(self, collections):
        requests = self.context.get('request')
        photo_url = collections.image.url
        photo_url = requests.build_absolute_uri(photo_url)
        # print(requests.build_absolute_uri('/')[:-1] + collections.image.url)
        return photo_url


class CartSerializer(serializers.ModelSerializer):
    """ cart serializer """

    # user = serializers.StringRelatedField()
    # products = serializers.StringRelatedField()

    class Meta:
        """ cart serializer Meta class """
        model = Cart
        fields = ['id', 'user', 'products', 'total_amount', 'quantity']


class AddressSerializer(serializers.ModelSerializer):
    """ Address serializer model class
    """
    class Meta:
        """ address serializer Meta class """
        model = Address
        fields = ['id', 'user', 'house_building_number', 'land_mark', 'village_city', 'district',
                  'pin_code', 'state', 'country', 'full_address']
