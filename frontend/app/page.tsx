export interface Product {
  external_id: string;
  title: string;
  image_link: string;
  link: string;
  cleaned_link: null | string;
  price: Price;
  merchant_name: string;
  brand: string;
  sale_price: Price | null;
  gtin: null | string;
  mpn: null | string;
}

export interface Price {
  value: number;
  currency: Currency;
}

export enum Currency {
  Eur = "EUR",
}

export default async function Home() {
  const products = (await (
    await fetch("http://localhost:8000/adstrong/")
  ).json()) as Product[];

  const formatPrice = (price: Price) => {
    return new Intl.NumberFormat("fr-FR", {
      style: "currency",
      currency: price.currency,
    }).format(price.value);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-6 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Products</h1>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 sm:gap-4">
          {products.map((product) => {
            if (!product.cleaned_link) {
              return;
            }

            const hasDiscount =
              product.sale_price &&
              product.sale_price.value < product.price.value;

            return (
              <a
                key={product.external_id}
                href={product.cleaned_link}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow duration-300 overflow-hidden group"
              >
                <div className="relative aspect-square bg-gray-100">
                  <img
                    src={product.image_link}
                    alt={product.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  {hasDiscount && (
                    <div className="absolute top-1 right-1 bg-red-500 text-white px-1.5 py-0.5 rounded text-xs font-semibold">
                      Sale
                    </div>
                  )}
                </div>

                <div className="p-3">
                  {product.brand && (
                    <p className="text-xs text-gray-500 mb-1 truncate">
                      {product.brand}
                    </p>
                  )}

                  <h2 className="text-sm font-medium text-gray-900 mb-1.5 line-clamp-2 min-h-[2.5rem]">
                    {product.title}
                  </h2>

                  <div className="flex items-baseline gap-1.5 mb-1">
                    {hasDiscount ? (
                      <>
                        <span className="text-base font-bold text-red-600">
                          {formatPrice(product.sale_price!)}
                        </span>
                        <span className="text-xs text-gray-500 line-through">
                          {formatPrice(product.price)}
                        </span>
                      </>
                    ) : (
                      <span className="text-base font-bold text-gray-900">
                        {formatPrice(product.price)}
                      </span>
                    )}
                  </div>

                  <p className="text-xs text-gray-600 truncate">
                    {product.merchant_name}
                  </p>
                </div>
              </a>
            );
          })}
        </div>

        {products.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No products found</p>
          </div>
        )}
      </div>
    </div>
  );
}
