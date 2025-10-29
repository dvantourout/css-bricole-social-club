from integrations.external_db.models import Listing
from shared.schemas import NormalizedProduct


class ExternalDbNormalizer:
    @staticmethod
    def normalize(product: Listing) -> NormalizedProduct:
        return NormalizedProduct(
            external_id=str(product.id),
            title=product.title,
            image_link=product.feed_img_links[0] if product.feed_img_links else None,
            link=product.link,
            cleaned_link=product.link,
            price=product.price,
            currency=product.currency,
            merchant_name=product.catalogue.name,
            brand=product.brand,
            sale_price=product.sale_price,
            gtin=product.gtin,
            mpn=product.mpn,
        )
