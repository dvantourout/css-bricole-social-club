"use client";

import { useRouter } from "next/navigation";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  hasMore: boolean;
  searchQuery?: string;
}

export function Pagination({
  currentPage,
  totalPages,
  hasMore,
  searchQuery = "",
}: PaginationProps) {
  const router = useRouter();

  const buildUrl = (page: number) => {
    const params = new URLSearchParams();
    if (searchQuery) {
      params.set("query", searchQuery);
    }
    params.set("page", page.toString());
    return `/?${params.toString()}`;
  };

  const handlePrevious = () => {
    if (currentPage > 1) {
      router.push(buildUrl(currentPage - 1));
    }
  };

  const handleNext = () => {
    if (hasMore) {
      router.push(buildUrl(currentPage + 1));
    }
  };

  const handlePageClick = (page: number) => {
    router.push(buildUrl(page));
  };

  const handleFirstPage = () => {
    router.push(buildUrl(1));
  };

  const handleLastPage = () => {
    router.push(buildUrl(totalPages));
  };

  // Generate page numbers to display
  const generatePageNumbers = () => {
    const pages: (number | "ellipsis")[] = [];
    const maxVisible = 7; // Maximum number of page buttons to show

    if (totalPages <= maxVisible) {
      // Show all pages if total is small
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else if (currentPage <= 4) {
      // Near the start
      for (let i = 1; i <= 5; i++) {
        pages.push(i);
      }
      pages.push("ellipsis");
      pages.push(totalPages);
    } else if (currentPage >= totalPages - 3) {
      // Near the end
      pages.push(1);
      pages.push("ellipsis");
      for (let i = totalPages - 4; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // In the middle
      pages.push(1);
      pages.push("ellipsis");

      // Show current page and neighbors
      for (let i = currentPage - 1; i <= currentPage + 1; i++) {
        pages.push(i);
      }

      pages.push("ellipsis");
      pages.push(totalPages);
    }

    return pages;
  };

  const pageNumbers = generatePageNumbers();

  // Don't show pagination if there's only one page
  if (totalPages <= 1) {
    return null;
  }

  return (
    <div className="mt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
      {/* Page info and navigation controls */}
      <div className="flex items-center gap-2">
        {/* First/Previous buttons */}
        <div className="flex gap-1">
          <button
            onClick={handleFirstPage}
            disabled={currentPage === 1}
            className={`px-3 py-2 rounded-lg font-medium transition-colors ${
              currentPage === 1
                ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                : "bg-white text-gray-700 hover:bg-gray-50 border border-gray-300"
            }`}
          >
            First
          </button>
          <button
            onClick={handlePrevious}
            disabled={currentPage === 1}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              currentPage === 1
                ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                : "bg-white text-gray-700 hover:bg-gray-50 border border-gray-300"
            }`}
          >
            Previous
          </button>
        </div>

        {/* Page Numbers */}
        <div className="hidden sm:flex gap-1">
          {pageNumbers.map((page, index) => {
            if (page === "ellipsis") {
              return (
                <span
                  key={`ellipsis-${index}`}
                  className="px-4 py-2 text-gray-500"
                >
                  ...
                </span>
              );
            }

            const isActive = page === currentPage;

            return (
              <button
                key={page}
                onClick={() => handlePageClick(page)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "bg-white text-gray-700 hover:bg-gray-50 border border-gray-300"
                }`}
              >
                {page}
              </button>
            );
          })}
        </div>

        {/* Next/Last buttons */}
        <div className="flex gap-1">
          <button
            onClick={handleNext}
            disabled={!hasMore}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              !hasMore
                ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                : "bg-white text-gray-700 hover:bg-gray-50 border border-gray-300"
            }`}
          >
            Next
          </button>
          <button
            onClick={handleLastPage}
            disabled={currentPage === totalPages}
            className={`px-3 py-2 rounded-lg font-medium transition-colors ${
              currentPage === totalPages
                ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                : "bg-white text-gray-700 hover:bg-gray-50 border border-gray-300"
            }`}
          >
            Last
          </button>
        </div>
      </div>

      {/* Page info (Mobile and Desktop) */}
      <div className="text-sm text-gray-600">
        <span className="sm:hidden">
          Page {currentPage} of {totalPages}
        </span>
        <span className="hidden sm:inline">
          Page {currentPage} of {totalPages.toLocaleString()}
        </span>
      </div>
    </div>
  );
}
