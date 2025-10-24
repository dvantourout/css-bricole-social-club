from ikom.schemas import ProductInput
from shared.schemas import NormalizedPrice, NormalizedProduct
from shared.utils import clean_link


class IkomNormalizer:
    @staticmethod
    def normalize(product: ProductInput) -> NormalizedProduct:
        clean_product_link = clean_link(product.link)

        return NormalizedProduct(
            title=product.title,
            image_link=product.image_link,
            link=clean_product_link,
            price=NormalizedPrice(
                value=product.price.value,
                currency=product.price.currency,
            ),
            merchant_name=product.merchant_name,
            sale_price=NormalizedPrice(
                value=product.price.value,
                currency=product.price.currency,
            ),
            gtin=product.gtin,
            mpn=product.mpn,
        )
