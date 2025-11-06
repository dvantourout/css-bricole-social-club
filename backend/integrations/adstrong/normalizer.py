from integrations.adstrong.schemas import ProductInputSchema
from shared.schemas import NormalizedProduct
from shared.utils import clean_link


class AdstrongNormalizer:
    @staticmethod
    def normalize(product: ProductInputSchema) -> NormalizedProduct:
        clean_product_link = clean_link(product.url)

        price = product.price.value
        sale_price = None

        if product.marketing_price and product.marketing_price.original_price:
            sale_price = price
            price = product.marketing_price.original_price

        return NormalizedProduct(
            external_id=product.id,
            title=product.title,
            image_link=product.image,
            link=product.url,
            cleaned_link=clean_product_link,
            price=product.price.value,
            currency=product.price.currency,
            merchant_name=product.seller,
            brand=product.brand,
            sale_price=sale_price,
            gtin=product.gtin,
            mpn=product.mpn,
        )
