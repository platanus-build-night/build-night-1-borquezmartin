// src/components/NewsCard.jsx
import React from 'react';

export default function NewsCard({ article }) {
  return (
    <div className="bg-base-05 border rounded-lg overflow-hidden shadow hover:shadow-lg transition-shadow p-4">
      {/* News title */}
      <h2 className="text-xl font-slab mb-2">
        {article.title}
      </h2>

      {/* Description snippet */}
      <p className="text-sm mb-4">
        {article.description || 'No description available.'}
      </p>

      {/* URL link */}
      <a
        href={article.url}
        className="text-purple-600 hover:underline break-all"
        target="_blank"
        rel="noopener noreferrer"
      >
        {article.url}
      </a>
    </div>
  );
}
