import React, { Suspense, lazy, useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';

const Home = lazy(() => import('./pages/Home'));
const NewsDetail = lazy(() => import('./pages/NewsDetail'));

export default function App() {
  // Sidebar open state for shifting content
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <Header isOpen={isOpen} toggleMenu={() => setIsOpen(open => !open)} />

      {/* Main content shifts with sidebar */}
      <main
        className={`flex-1 transition-all duration-300 ease-in-out p-0 ${isOpen ? 'ml-2/5 sm:ml-1/12' : 'ml-0'}`}
      >
        <Suspense fallback={<div className="p-4 text-center">Loading...</div>}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/news/:id" element={<NewsDetail />} />
          </Routes>
        </Suspense>
      </main>
    </div>
  );
}