"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { FaUserCircle, FaSignOutAlt, FaComments, FaRobot, FaCogs, FaTimes, FaPaperPlane } from "react-icons/fa";
import { FaUsers, FaLightbulb, FaLock, FaSlidersH } from "react-icons/fa";
import axios from "axios";
import { CircularProgress } from "@mui/material";
  import "react-toastify/dist/ReactToastify.css";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [userDetails, setUserDetails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [message, setMessage] = useState("");
  const [sending, setSending] = useState(false);
  const router = useRouter();

  // Features list
  const features = [
    { title: "Real-Time Collaboration", description: "Work together with team members seamlessly.", icon: <FaRobot className="text-blue-500 text-4xl" /> },
    { title: "AI-Powered Recommendations", description: "Get smart suggestions tailored to your workflow.", icon: <FaLightbulb className="text-blue-500 text-4xl" /> },
    { title: "Secure Data Storage", description: "Your data is safely stored with end-to-end encryption.", icon: <FaLock className="text-blue-500 text-4xl" /> },
    { title: "Customizable Dashboard", description: "Personalize your workspace to fit your needs.", icon: <FaSlidersH className="text-blue-500 text-4xl" /> },
  ];



  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      router.push("/login");
      return;
    }

    axios
      .get("http://127.0.0.1:8000/api/user/details/", {
        headers: { Authorization: `Token ${token}` },
      })
      .then((response) => {
        setUserDetails(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching user details:", error);
        localStorage.removeItem("accessToken");
        router.push("/login");
      });
  }, [router]);


  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      router.push("/login");
      return;
    }
    fetchUserProfile(token);
  }, []);

  // Fetch user profile
  async function fetchUserProfile(token) {  
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/users/", {
        headers: { Authorization: `Token ${token}` },
      });
      setUser(response.data);
    } catch (error) {
      console.error("Error fetching user:", error);
      localStorage.removeItem("accessToken");
      router.push("/login");
    } finally {
      setLoading(false);
    }
  }

  
  async function sendMessage() {
    if (!message.trim()) return;
  
    if (user.tokens === 0) {
      console.warn("We don't have sufficient tokens to send a message.");
      toast.warning("We can't send the message. Please renew your tokens.");
      return;
    }
  
    if (user.tokens <= 100) {
      toast.warning("Warning: Your tokens are below 100. Consider renewing soon.");
    }
  
    const token = localStorage.getItem("accessToken");
  
    // Create a chat bubble for the user's message
    const userMessage = {
      text: `You: ${message}`,
      sender: "user",
      timestamp: new Date().toLocaleTimeString(),
    };
    setChatMessages((prev) => [...prev, userMessage]);
    setMessage("");
    setSending(true);
  
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/chat/send_message/",
        { message },
        { headers: { Authorization: `Token ${token}` } }
      );
  
      // Update user tokens after a successful request
      setUser((prev) => ({ ...prev, tokens: response.data.remaining_tokens }));
  
      // Add AI response to chat
      const aiMessage = {
        text: `AI: ${response.data.response} (Tokens Left: ${response.data.remaining_tokens})`,
        sender: "ai",
        timestamp: new Date().toLocaleTimeString(),
      };
      setChatMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      toast.error("Failed to send message. Try again.");
    } finally {
      setSending(false);
    }
  }
  
  
  // Logout function
  function logout() {
    localStorage.removeItem("accessToken");
    setUser(null);
    router.push("/login");
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen text-gray-900 text-2xl">
        <CircularProgress />
      </div>
    );
  }

  return (
    <div className="bg-white text-gray-900 min-h-screen">
      <div className="flex flex-col items-center p-6 pt-20">
        <header className="w-full max-w-4xl flex justify-between items-center p-4 shadow-md rounded-lg">
          <div className="flex items-center space-x-4">
            <FaUserCircle className="text-3xl" />
            <h1 className="text-2xl font-bold">AI Chat Dashboard</h1>
          </div>
          <button
            onClick={logout}
            className="flex items-center space-x-2 px-4 py-2 rounded-full border border-gray-500 text-gray-700 hover:shadow-lg hover:bg-gray-100 transition"
          >
            <FaSignOutAlt />
            <span>Logout</span>
          </button>
        </header>

        {/* User Data Cards */}
        {user && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6 w-full max-w-4xl my-10">
            <div className="p-4 bg-blue-500 text-white rounded-lg shadow-md">
              <h2 className="text-lg font-semibold">Username</h2>
              Welcome, <strong>{userDetails.username}</strong>!
              </div>
            <div className="p-4 bg-purple-500 text-white rounded-lg shadow-md">
              <h2 className="text-lg font-semibold">Tokens Balance</h2>
              <strong>{userDetails.tokens}</strong>            </div>
          </div>
        )}

        <h2 className="text-center text-2xl font-bold mb-10">
          Why Choose <span className="text-green-600">Our AI Chat</span>?
        </h2>
        <p className="text-center text-gray-600 mb-8 max-w-2xl mx-auto my-10">
          Experience seamless, intelligent, and instant AI-powered conversations. Our chat system is designed to enhance productivity, engagement, and problem-solving with ease.
        </p>
        <div className="md:w-[70%] w-[83%] mx-auto">
          <div className="px-10 md:px-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="w-full aspect-square shadow-md rounded-lg transform hover:scale-102 transition-transform flex flex-col items-center justify-center bg-white text-gray-900 p-6"
              >
                <span className="flex items-center justify-center mb-4 p-4 rounded-full bg-blue-100 text-blue-500">
                  {feature.icon}
                </span>
                <h4 className="mb-2 text-lg font-bold text-center">{feature.title}</h4>
                <p className="text-gray-500 text-center">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Chat Icon */}
        <div
          className="fixed bottom-16 right-6 bg-blue-500 p-4 rounded-full cursor-pointer shadow-lg"
          onClick={() => setChatOpen(true)}
        >
          <FaComments className="text-white text-4xl" />
        </div>

        {/* Chat Window */}
        {chatOpen && (
          <div className="fixed bottom-16 right-6 bg-gray-800 text-white p-4 w-80 rounded-lg shadow-lg flex flex-col">
            {/* Chat Header */}
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-lg font-semibold bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
                Chat with Chat
              </h3>
              <button onClick={() => setChatOpen(false)} className="text-white text-xl">
                <FaTimes />
              </button>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto max-h-60 space-y-2 p-2 scrollbar-hide">
              {chatMessages.map((msg, index) => (
                <div
                  key={index}
                  className={`p-2 rounded-lg ${
                    msg.sender === "user"
                      ? "bg-blue-500 text-right rounded-tr-none ml-auto"
                      : "bg-gray-700 rounded-bl-none"
                  }`}
                >
                  <p>{msg.text}</p>
                  <small className="block text-xs text-gray-300">{msg.timestamp}</small>
                </div>
              ))}
            </div>

            {/* Chat Input */}
            <div className="flex mt-2 space-x-2">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                placeholder="Type a message..."
                className="flex-1 p-2 rounded bg-gray-900 text-white"
              />
              <button onClick={sendMessage} disabled={sending} className="bg-blue-500 p-2 rounded">
                <FaPaperPlane className="text-white" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
