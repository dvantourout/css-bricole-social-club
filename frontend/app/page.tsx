import { SearchBar } from "./components/search-bar";
import { ProductGrid } from "./components/product-grid";

export interface Product {
  link: string;
  title: string;
  price: number;
  sale_price: number | null;
  merchant_name: string;
  gtin: null | string;
  source: Source;
  created_at: Date;
  cleaned_link: string;
  image_link: string;
  id: string;
  currency: Currency;
  brand: string;
  mpn: null | string;
  external_id: string;
  updated_at: Date;
}

export enum Currency {
  Eur = "EUR",
}

export enum Source {
  Adstrong = "adstrong",
}

// Server-side function - runs on Next.js server, not in browser
async function fetchProducts(searchQuery: string = ""): Promise<Product[]> {
  const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

  try {
    const url = `${BACKEND_URL}/api/v1/?query=${encodeURIComponent(
      searchQuery
    )}&page_size=50`;

    console.log(`[Server] Fetching from: ${url}`); // Server log only

    const response = await fetch(url, {
      // Don't cache search results, cache empty query
      cache: searchQuery ? "no-store" : "default",
      next: { revalidate: searchQuery ? 0 : 3600 }, // Cache 1 hour for homepage
    });

    if (!response.ok) {
      console.error(`[Server] Backend error: ${response.status}`);
      return [];
    }

    const data = await response.json();
    console.log(`[Server] Fetched ${data.length} products`); // Server log only

    return data;
  } catch (error) {
    console.error("[Server] Error fetching products:", error);
    return [];
  }
}

// Page component - receives searchParams from URL
interface PageProps {
  searchParams: Promise<{ query?: string }>;
}

export default async function Home({ searchParams }: PageProps) {
  // Await searchParams (Next.js 15 requirement)
  const params = await searchParams;
  const searchQuery = params.query || "";

  // Fetch products on server - HTML generated server-side!
  const products = await fetchProducts(searchQuery);

  return (
    <div className="min-h-screen bg-gray-50 py-6 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Products</h1>

          {/* Client Component for search input */}
          <SearchBar initialQuery={searchQuery} />

          {/* Search Results Info */}
          {searchQuery && (
            <div className="mt-4 text-sm text-gray-600">
              Found {products.length} result{products.length !== 1 ? "s" : ""}{" "}
              for "{searchQuery}"
            </div>
          )}
        </div>

        {/* Server-rendered product grid */}
        <ProductGrid products={products} />

        {/* Empty State */}
        {products.length === 0 && (
          <div className="text-center py-12">
            {searchQuery ? (
              <>
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
                <p className="mt-4 text-gray-500 text-lg">
                  No products found for "{searchQuery}"
                </p>
              </>
            ) : (
              <p className="text-gray-500 text-lg">No products available</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
