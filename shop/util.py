import requests
from django.conf import settings
from .models import Product, ProductImage, ShopProvider


# Set up the Shopify API URL and access token
shopify_api_url = "https://{}:{}@{}.myshopify.com/admin/api/2020-01/products.json".format(settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD, settings.SHOPIFY_STORE_NAME)

# Make the API request to get the products
response = requests.get(shopify_api_url)

# Get the JSON data from the response
data = response.json()

# Iterate through the products in the JSON data
for product_data in data['products']:
    # Create a new Product object and save it to the database
    product = Product(name=product_data['title'],
                      price=product_data['price'],
                      sku=product_data['variants'][0]['sku'],
                      description=product_data['body_html'])
    product.save()
    # iterate through images and save it to product_image model
    for image in product_data['images']:
        product_image = ProductImage(product=product,
                                     image_url=image['src'],
                                     alt=image['alt'])
        product_image.save()

