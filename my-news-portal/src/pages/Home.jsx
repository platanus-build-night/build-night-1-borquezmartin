import React, { useState, useEffect } from 'react';
import NewsCard from '../components/NewsCard';

export default function Home() {
  const [news, setNews] = useState([]);

  useEffect(() => {
    fetch('/data/articles.json')
      .then(res => res.json())
      .then(batches => {
        // Flatten all batches into a single articles array
        const allArticles = batches.flatMap(batch => batch.batch_data);
        setNews(allArticles);
      })
      .catch(err => console.error('Failed to load articles:', err));
  }, []);

  return (
    <main className="container mx-auto py-6 px-4">
      <h1 className="text-3xl font-bold mb-6">Latest News</h1>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {news.map(article => (
          <NewsCard key={`${article.portal}-${article.news_id}`} article={article} />
        ))}
      </div>
    </main>
  );
}