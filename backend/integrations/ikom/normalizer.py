from integrations.ikom.schemas import ProductInputSchema
from shared.schemas import NormalizedPrice, NormalizedProduct
from shared.utils import clean_link


class IkomNormalizer:
    @staticmethod
    def normalize(product: ProductInputSchema) -> NormalizedProduct:
        clean_product_link = clean_link(product.link)

        return NormalizedProduct(
            external_id=product.gtin,
            title=product.title,
            image_link=product.image_link,
            link=product.link,
            cleaned_link=clean_product_link,
            price=product.price.value,
            currency=product.price.currency,
            merchant_name=product.merchant_name,
            brand=product.brand,
            sale_price=product.sale_price.value if product.sale_price else None,
            gtin=product.gtin,
            mpn=product.mpn,
        )
