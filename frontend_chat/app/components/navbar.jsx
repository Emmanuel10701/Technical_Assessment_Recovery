"use client";
import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { FaBars, FaTimes } from "react-icons/fa";

const NavBar = () => {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="w-full p-4 shadow-lg border-b fixed top-0 left-0 right-0 z-50 bg-white text-gray-900 border-gray-300">
      <div className="container mx-auto flex justify-between items-center">
        {/* Title */}
        <h1 className="text-xl font-bold uppercase cursor-pointer">
          <Link href="/">AI Chat Assistant</Link>
        </h1>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center space-x-6">
          <NavLinks pathname={pathname} />
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden cursor-pointer"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden flex flex-col items-center gap-4 py-4 bg-gray-100 text-gray-900">
          <NavLinks pathname={pathname} />
        </div>
      )}
    </nav>
  );
};

// Navigation Links Component
const NavLinks = ({ pathname }) => (
  <>
    <Link href="/">
      <span
        className={`hover:text-blue-400 text-sm font-bold px-3 transition duration-200 uppercase cursor-pointer ${
          pathname === "/" ? "text-blue-800" : "text-gray-900"
        }`}
      >
        Home
      </span>
    </Link>
    <Link href="/dashboard">
      <span
        className={`hover:text-blue-400 text-sm font-bold px-3 transition duration-200 uppercase cursor-pointer ${
          pathname === "/dashboard" ? "text-blue-800" : "text-gray-900"
        }`}
      >
        Chat
      </span>
    </Link>
    <Link href="/about">
      <span
        className={`hover:text-blue-400 text-sm font-bold px-3 transition duration-200 uppercase cursor-pointer ${
          pathname === "/about" ? "text-blue-800" : "text-gray-900"
        }`}
      >
        About
      </span>
    </Link>
  </>
);

export default NavBar;
