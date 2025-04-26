import React from 'react';
import ArticleCard from './ArticleCard';

export default function ArticleList({ articles }) {
  return (
    <main style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(300px,1fr))',
      gap: '1.5rem',
      padding: '2rem'
    }}>
      {articles.map(a => (
        <ArticleCard key={a.id} article={a} />
      ))}
    </main>
  );
}
