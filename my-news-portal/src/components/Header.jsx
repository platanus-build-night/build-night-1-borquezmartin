import React from 'react';

export default function Header() {
  return (
    <header style={{
      background: 'var(--bg)',
      padding: '1rem 2rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      <h1 style={{ color: 'var(--accent)' }}>NewsPortal</h1>
      <nav>
        <a href="#">Top Stories</a>
        <a href="#" style={{ marginLeft: '1rem' }}>Últimas</a>
        <a href="#" style={{ marginLeft: '1rem' }}>Contacto</a>
      </nav>
    </header>
  );
}
