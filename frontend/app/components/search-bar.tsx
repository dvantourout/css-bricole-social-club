"use client";

import { useRouter } from "next/navigation";
import { useState, useEffect, useTransition } from "react";

interface SearchBarProps {
  initialQuery?: string;
}

export function SearchBar({ initialQuery = "" }: SearchBarProps) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [searchQuery, setSearchQuery] = useState(initialQuery);

  // Debounced search - navigates after 300ms of no typing
  useEffect(() => {
    const timer = setTimeout(() => {
      startTransition(() => {
        if (searchQuery.trim()) {
          // Navigate with query parameter - triggers server re-render
          router.push(`/?query=${encodeURIComponent(searchQuery)}`);
        } else {
          router.push("/");
        }
      });
    }, 300); // 300ms debounce

    return () => clearTimeout(timer);
  }, [searchQuery, router]);

  const handleClearSearch = () => {
    setSearchQuery("");
  };

  return (
    <div className="relative max-w-2xl">
      <div className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search products by name, brand, merchant, GTIN..."
          className="w-full px-4 py-3 pl-12 pr-12 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
        />

        {/* Search Icon or Loading Spinner */}
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
          {isPending ? (
            <div className="animate-spin h-5 w-5 border-2 border-gray-300 border-t-gray-600 rounded-full"></div>
          ) : (
            <svg
              className="w-5 h-5"
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
          )}
        </div>

        {/* Clear Button */}
        {searchQuery && (
          <button
            type="button"
            onClick={handleClearSearch}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}
