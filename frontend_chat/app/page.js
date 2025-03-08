"use client";
import React from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { FaDatabase, FaRobot, FaComments, FaSearch } from "react-icons/fa";

const features = [
  {
    title: "Instant AI Responses",
    description: "Chat with our AI assistant to get quick and intelligent answers.",
    icon: <FaRobot className="text-blue-500 text-4xl" />, 
  },
  {
    title: "Seamless Conversations",
    description: "Engage in natural and interactive dialogues powered by AI.",
    icon: <FaComments className="text-blue-500 text-4xl" />,
  },
  {
    title: "Data-Driven Insights",
    description: "Receive insights and recommendations based on your chat history.",
    icon: <FaDatabase className="text-blue-500 text-4xl" />,
  },
  {
    title: "Advanced Search",
    description: "Quickly find relevant information during your conversation.",
    icon: <FaSearch className="text-blue-500 text-4xl" />,
  },
];

export default function Home({ data }) {
  const router = useRouter();

  return (
    <div className="font-poppins transition-all duration-300 bg-gray-50 text-gray-900">
      <header className="relative text-center py-16 bg-blue-50 transition-all duration-300">
        <div className="flex flex-col-reverse md:flex-row items-center mx-4 md:mx-40 mt-10">
          <div className="md:w-1/2">
            <h1 className="mb-4 text-5xl font-bold text-gray-900 transition-all duration-300">
              Experience <span className="text-blue-600">AI Chat</span>
            </h1>
            <p className="mb-8 max-w-xl mx-auto leading-relaxed text-gray-500 transition-all duration-300">
              Connect with our AI chat assistant for real-time conversations, intelligent responses, and a personalized experience.
            </p>
            <div className="flex justify-center gap-4">
              <button
                onClick={() => router.push("/login")}
                className="px-8 py-3 font-medium text-white bg-blue-600 rounded-full hover:bg-blue-700 transition duration-300"
              >
                Login
              </button>
              <a href="#features">
                <button className="px-8 py-3 font-medium text-blue-600 border-2 border-blue-600 rounded-full hover:bg-blue-100 transition duration-300">
                  Learn More
                </button>
              </a>
            </div>
          </div>
          <div className="md:w-1/2">
            <Image src="/lady.png" alt="AI Chat" width={500} height={500} />
          </div>
        </div>
      </header>

      <section id="features" className="py-16 px-4 mx-4 md:px-12 bg-gray-100 transition-all duration-300">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-8 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-green-500 transition-all duration-300">
            Why Choose <span className="text-green-600">Our AI Chat</span>?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 shadow-md rounded-lg transition-transform duration-500 transform hover:scale-105 flex flex-col items-center bg-white text-gray-900"
              >
                <span className="flex items-center justify-center mb-4 p-4 rounded-full bg-blue-100 text-blue-500">
                  {feature.icon}
                </span>
                <h4 className="mb-2 text-lg font-bold">{feature.title}</h4>
                <p className="text-gray-500">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
