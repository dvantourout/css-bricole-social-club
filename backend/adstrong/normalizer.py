from adstrong.schemas import ProductInputSchema
from shared.schemas import NormalizedPrice, NormalizedProduct
from shared.utils import clean_link


class AdstrongNormalizer:
    @staticmethod
    def normalize(product: ProductInputSchema) -> NormalizedProduct:
        clean_product_link = clean_link(product.url)

        price = NormalizedPrice(
            value=product.price.value,
            currency=product.price.currency,
        )
        sale_price = None

        if product.marketing_price and product.marketing_price.original_price:
            sale_price = price
            price = NormalizedPrice(
                value=product.marketing_price.original_price.value,
                currency=product.marketing_price.original_price.currency,
            )

        return NormalizedProduct(
            title=product.title,
            image_link=product.image,
            link=product.url,
            cleaned_link=clean_product_link,
            price=price,
            merchant_name=product.seller,
            brand=product.brand,
            sale_price=sale_price,
            gtin=product.gtin,
            mpn=product.mpn,
        )
