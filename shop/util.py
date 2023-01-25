import requests
from django.conf import settings
from .models import Product, ProductImage, ShopProvider


def getProducts():
    getProvider = ShopProvider.objects.get()

    if getProvider.name == "Shopify":
        # set without defaults for now
        SHOPIFY_API_KEY = getProvider.api_key
        SHOPIFY_API_PASSWORD = getProvider.api_password
        SHOPIFY_STORE_NAME = getProvider.store_name

        # Set up the Shopify API URL and access token
        shopify_api_url = "https://{}:{}@{}.myshopify.com/admin/api/2020-01/products.json".format(SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD, SHOPIFY_STORE_NAME)

        # Make the API request to get the products
        response = requests.get(shopify_api_url)

        # Get the JSON data from the response
        data = response.json()

        products_added = 0

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
            products_added = products_added + 1
    
    return products_added + " " + getProvider.name + " Products Added!"

