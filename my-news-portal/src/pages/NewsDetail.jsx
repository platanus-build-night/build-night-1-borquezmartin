import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function NewsDetail() {
  const { id } = useParams();
  const [article, setArticle] = useState(null);

  useEffect(() => {
    fetch('/data/news.json')
      .then(res => res.json())
      .then(data => {
        // Find by ID (string vs number)
        const found = data.find(item => item.id.toString() === id);
        setArticle(found);
      });
  }, [id]);

  if (!article) return <div className="p-4">Loading...</div>;

  return (
    <article className="container mx-auto py-6 px-4 prose">
      <h1 className="text-4xl font-bold mb-4 font-slab">
        {article.title}
      </h1>
      <img
        src={article.imageUrl}
        alt={article.title}
        className="w-full max-h-[400px] object-cover mb-6 rounded"
        loading="lazy"
      />
      <p>{article.content}</p>
      <Link to="/" className="mt-6 inline-block text-purple-600 hover:underline">
        ← Back to home
      </Link>
    </article>
  );
}