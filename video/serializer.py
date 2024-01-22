from rest_framework import serializers
from .models import Video, VideoProduct

from rest_framework import serializers
from shop.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'


class VideoProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = VideoProduct
        fields = ['id', 'product', 'show_timestamp', 'hide_timestamp']

class VideoSerializer(serializers.ModelSerializer):
    related_products = ProductSerializer(many=True)

    class Meta:
        model = Video
        fields = ['id', 'description','name', 'link', 'playback_hls','related_products']
