from uuid import uuid4

from core.models import Product
from shared.repository import BaseRepository
from shared.schemas import NormalizedProduct
from sqlalchemy import Select, case, func, insert, literal, or_, select, text


class ProductRepository(BaseRepository):
    def upsert(self, *, source: str, products: list[NormalizedProduct]):
        products_to_insert: list = []

        products_external_id = [product.external_id for product in products]

        stmt = select(Product.external_id).where(
            Product.source == source,
            Product.external_id.in_(
                products_external_id,
            ),
        )
        existing_producs_ids = self.db.scalars(stmt).all()

        for product in products:
            if product.external_id in existing_producs_ids:
                continue

            products_to_insert.append(
                {
                    "id": uuid4(),
                    "source": source,
                    "title": product.title,
                    "image_link": product.image_link,
                    "link": product.link,
                    "cleaned_link": product.cleaned_link,
                    "price": product.price,
                    "sale_price": product.sale_price if product.sale_price else None,
                    "currency": product.currency,
                    "merchant_name": product.merchant_name,
                    "brand": product.brand,
                    "gtin": product.gtin,
                    "mpn": product.mpn,
                    "external_id": product.external_id,
                }
            )

        if products_to_insert:
            self.db.execute(
                insert(Product),
                products_to_insert,
            )

    def _search(self, *, stmt: Select, query: str) -> Select:
        query_stripped = query.strip()
        query_lower = query_stripped.lower()
        query_pattern = f"%{query_lower}%"

        query_for_tsquery = query_stripped.replace(" ", " & ")

        combined_query = func.to_tsquery(
            "french",
            func.concat(
                func.unaccent(query_for_tsquery),
                " | ",
                func.unaccent(query_for_tsquery),
            ),
        )

        rank_expression = case(
            # Tier 1: Exact GTIN/MPN (highest priority)
            (
                or_(Product.gtin == query_stripped, Product.mpn == query_stripped),
                literal(1000),
            ),
            # Tier 2: Exact brand/merchant (case-insensitive)
            (
                or_(
                    func.lower(func.unaccent(Product.brand)) == query_lower,
                    func.lower(func.unaccent(Product.merchant_name)) == query_lower,
                ),
                literal(100),
            ),
            # Tier 3: Prefix match ("autodoc" matches "autodoc.fr")
            (
                or_(
                    func.lower(func.unaccent(Product.brand)).like(query_pattern),
                    func.lower(func.unaccent(Product.merchant_name)).like(
                        query_pattern
                    ),
                ),
                literal(50),
            ),
            # Tier 4: Full-text search (ts_rank uses A/B/C weights automatically)
            # Weight A (title) will score higher than B (brand) and C (merchant)
            (
                Product.search_vector.op("@@")(combined_query),
                # Multiply by 40 to keep FTS scores below Tier 3
                # ts_rank returns 0-1, so * 40 gives 0-40 range
                func.ts_rank(Product.search_vector, combined_query) * 40,
            ),
            else_=literal(0),
        ).label("rank")

        stmt = select(Product, rank_expression)

        # Search conditions
        search_condition = or_(
            # Exact matches
            Product.gtin == query_stripped,
            Product.mpn == query_stripped,
            func.lower(func.unaccent(Product.brand)) == func.unaccent(query_lower),
            func.lower(func.unaccent(Product.merchant_name))
            == func.unaccent(query_lower),
            # Prefix matches (uses idx_product_brand_lower, idx_product_merchant_lower)
            func.lower(func.unaccent(Product.brand)).like(func.unaccent(query_pattern)),
            func.lower(func.unaccent(Product.merchant_name)).like(
                func.unaccent(query_pattern)
            ),
            # Full-text search (uses idx_product_search_vector)
            Product.search_vector.op("@@")(combined_query),
        )

        stmt = stmt.where(search_condition)
        stmt = stmt.order_by(text("rank DESC"), Product.updated_at.desc())

        return stmt

    def _filters(
        self,
        *,
        stmt: Select,
        query: str = None,
        filter_cleaned_link: bool = True,
    ) -> Select:
        if query:
            stmt = self._search(stmt=stmt, query=query)

        if filter_cleaned_link:
            stmt = stmt.where(Product.cleaned_link.isnot(None))

        return stmt

    def _paginate(
        self,
        *,
        stmt: Select,
        limit: int = 100,
        offset: int = 0,
    ) -> Select:
        stmt = stmt.limit(limit).offset(offset)

        return stmt

    def _build_base_query(self, **kwargs):
        stmt = select(Product)
        stmt = self._filters(stmt=stmt, **kwargs)

        return stmt

    def count(self, **kwargs):
        base_stmt = self._build_base_query(**kwargs)
        count_stmt = select(func.count()).select_from(base_stmt.subquery())

        return self.db.scalar(count_stmt)

    def list(self, *, limit: int = 100, offset: int = 0, **kwargs):
        base_stmt = self._build_base_query(**kwargs)
        stmt = self._paginate(stmt=base_stmt, limit=limit, offset=offset)

        return self.db.scalars(stmt).all()

    def list_with_count(self, *, limit: int = 100, offset: int = 0, **kwargs):
        products = self.list(limit=limit, offset=offset, **kwargs)
        count = self.count(**kwargs)

        return products, count
