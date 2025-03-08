"use client";
import { useRouter } from "next/navigation";
import { FaArrowLeft } from "react-icons/fa";

const NotFound = () => {
  const router = useRouter();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white text-gray-900">
      <div className="text-center mb-8">
        <h1 className="text-6xl font-extrabold mb-4">404</h1>
        <h2 className="text-2xl text-gray-700 mb-4">
          Oops! The page you're looking for doesn't exist.
        </h2>
        <p className="text-base text-gray-600">
          It seems you've landed on a page that doesn't exist. You can either go back to the homepage or use the navigation to find what you're looking for.
        </p>
      </div>

      <button
        onClick={() => router.push("/")}
        className="flex items-center px-6 py-3 bg-transparent border border-gray-500 rounded-full shadow hover:bg-gray-500 hover:text-white transition-all text-gray-800"
      >
        <FaArrowLeft className="mr-2" /> Go Back to Home
      </button>
    </div>
  );
};

export default NotFound;
