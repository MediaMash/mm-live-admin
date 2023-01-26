import requests
from django.conf import settings
from .models import Product, ProductImage, ShopProvider
# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)


def getProducts():
    getProvider = ShopProvider.objects.get()

    if getProvider.name == "Shopify":
        # set without defaults for now
        SHOPIFY_API_KEY = getProvider.api_key
        SHOPIFY_API_PASSWORD = getProvider.api_password
        SHOPIFY_STORE_NAME = getProvider.store_name
        ACCESS_TOKEN = getProvider.api_token

        # Set up the Shopify API URL and access token
        shopify_api_url = "https://{shop}.myshopify.com/admin/api/2023-01/products.json".format(shop=SHOPIFY_STORE_NAME)

        """
        LINK TO GET TOKEN: https://nullrecords.myshopify.com/admin/settings/apps/development/26071564289/api_credentials
        https://{shop}.myshopify.com/admin/api/2023-01/products.json \
            -H 'Content-Type: application/json' \
            -H 'X-Shopify-Access-Token: {access_token}'
        """
        print(shopify_api_url)
        # Make the API request to get the products
        response = requests.get(shopify_api_url, headers={'X-Shopify-Access-Token': ACCESS_TOKEN })
        print(response)
        if response.status_code != 200:
            logger.warning("ERROR:" + str(response.status_code) + "-" + str(response.content))
            return str(response.status_code)
        else:
            # Get the JSON data from the response
            data = response.json()

        products_added = 0

        # Iterate through the products in the JSON data
        for product_data in data['products']:
            # first build the link to the product
            product_link = "https://{}.myshopify.com/products/{}".format(SHOPIFY_STORE_NAME, product_data['handle'])
            
            print(product_link)

            # Create a new Product object and save it to the database
            product = Product(name=product_data['title'],
                            price=product_data['variants'][0]['price'],
                            sku=product_data['variants'][0]['sku'],
                            description=product_data['body_html'],
                            link=product_link,)
            product.save()
            # iterate through images and save it to product_image model
            for image in product_data['images']:
                product_image = ProductImage(product=product,
                                            image_url=image['src'],
                                            alt=image['alt'])
                product_image.save()
            products_added = products_added + 1
    
    return products_added

