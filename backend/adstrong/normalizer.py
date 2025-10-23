from adstrong.schemas import ProductInput
from shared.schemas import NormalizedProduct
from shared.utils import clean_url


class AdstrongNormalizer:
    @staticmethod
    def normalize(product: ProductInput) -> NormalizedProduct:
        clean_product_url = clean_url(product.url)

        return NormalizedProduct(
            title=product.title,
            mpn=product.mpn,
            gtin=None,
            image_url=product.image,
            product_url=clean_product_url,
        )
