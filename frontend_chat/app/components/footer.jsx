"use client";
import { FaRobot, FaShieldAlt, FaGlobe, FaEnvelope } from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="py-6 text-center bg-gray-100 text-gray-700">
      <div className="max-w-5xl mx-auto px-6 flex flex-col items-center space-y-4">
        <FaRobot className="text-blue-600 text-3xl" />
        <p className="text-sm">&copy; {new Date().getFullYear()} AI Chat Assistant. All rights reserved.</p>
        <div className="flex space-x-6">
          <a href="/privacy" className="flex items-center space-x-2 hover:text-blue-500 transition-all">
            <FaShieldAlt />
            <span>Privacy Policy</span>
          </a>
          <a href="/terms" className="flex items-center space-x-2 hover:text-blue-500 transition-all">
            <FaGlobe />
            <span>Terms of Service</span>
          </a>
          <a href="/contact" className="flex items-center space-x-2 hover:text-blue-500 transition-all">
            <FaEnvelope />
            <span>Contact Us</span>
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
