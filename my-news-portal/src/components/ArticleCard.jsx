import React from 'react';

export default function ArticleCard({ article }) {
  return (
    <article style={{
      background: 'var(--card-bg)',
      borderRadius: '8px',
      overflow: 'hidden',
      boxShadow: '0 2px 6px rgba(0,0,0,0.5)'
    }}>
      <img
        src={article.imageUrl}
        alt={article.title}
        style={{ width: '100%', height: '180px', objectFit: 'cover' }}
      />
      <div style={{ padding: '1rem' }}>
        <h2 style={{ marginBottom: '.5rem', fontSize: '1.2rem' }}>
          {article.title}
        </h2>
        <p style={{ fontSize: '.9rem', color: '#ccc' }}>
          {article.description}
        </p>
        <a href="#" style={{ display: 'block', marginTop: '1rem' }}>
          Leer más →
        </a>
      </div>
    </article>
  );
}
