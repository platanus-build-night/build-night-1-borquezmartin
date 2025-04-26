import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeftLong, faPodcast, faComments, faBook, faUser } from '@fortawesome/free-solid-svg-icons';

export default function Header() {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <>
      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 h-full bg-[#242424] p-4 shadow-lg transition-transform transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } w-1/5 sm:w-1/12 z-20`} // Reduce width to ~16.6% (1/6)
      >
        {/* Logo/title linking to Home */}
        <h1 className="text-2xl font-bold mb-8 font-sans text-white">
          <Link to="/">ReNews</Link> {/* Changed text and link */}
        </h1>

        {/* Navigation options with icons */}
        <nav className="space-y-4">
          <Link to="/podcast" className="flex items-center text-[#dadada] hover:text-purple-300">
            <FontAwesomeIcon icon={faPodcast} className="mr-2 text-[#dadada]" />&nbsp;
            Podcast
          </Link>
          <Link to="/social" className="flex items-center text-[#dadada] hover:text-purple-300">
            <FontAwesomeIcon icon={faComments} className="mr-2 text-[#dadada]" /> &nbsp;
            Social Media
          </Link>
          <Link to="/shelve" className="flex items-center text-[#dadada] hover:text-purple-300">
            <FontAwesomeIcon icon={faBook} className="mr-2 text-[#dadada]" /> &nbsp;
            Shelve
          </Link>
          <Link to="/profile" className="flex items-center text-[#dadada] hover:text-purple-300">
            <FontAwesomeIcon icon={faUser} className="mr-2 text-[#dadada]" />&nbsp;
            Profile
          </Link>
        </nav>        
      </aside>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-30 p-2 rounded-md bg-purple-600 text-white md:hidden focus:outline-none"
        aria-label="Toggle menu"
      >
        <FontAwesomeIcon icon={faArrowLeftLong} />
      </button>
    </>
  );
}