"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai";
import { CircularProgress } from "@mui/material";

const Login = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log("✅ API Response:", responseData);

        const token = responseData.token || responseData.access || responseData.authToken;
        
        if (!token) {
          console.error("❌ Token not found in response:", responseData);
          alert("Login failed: No token received.");
          return;
        }

        localStorage.setItem("accessToken", token);
        console.log("🔑 Token stored in localStorage:", token);

        alert("✅ Login successful! Redirecting...");
        router.push("/dashboard");
      } else {
        const errorData = await response.json();
        alert(errorData.detail || "Login failed. Please check your credentials.");
      }
    } catch (error) {
      console.error("❌ Fetch error:", error);
      alert("An error occurred. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 text-gray-900">
      <div className="w-full max-w-md p-8 rounded-lg shadow-lg bg-white text-gray-900">
        <h1 className="text-2xl font-bold text-center mb-8">Login to AI Chat Assistant</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-lg font-bold">Username</label>
            <input
              name="username"
              type="text"
              required
              value={formData.username}
              onChange={handleChange}
              className="mt-2 w-full p-4 border rounded-lg border-gray-300 text-lg"
            />
          </div>

          <div>
            <label className="block text-lg font-bold">Password</label>
            <div className="relative">
              <input
                name="password"
                type={showPassword ? "text" : "password"}
                required
                value={formData.password}
                onChange={handleChange}
                className="w-full p-4 border rounded-lg border-gray-300 text-lg"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-xl"
              >
                {showPassword ? <AiFillEyeInvisible /> : <AiFillEye />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-indigo-600 text-white p-4 rounded-lg hover:bg-indigo-500 text-lg"
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : "Login"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm">
          Don't have an account?{" "}
          <a href="/register" className="text-indigo-600 hover:underline">
            Sign up
          </a>
        </p>
      </div>
    </div>
  );
};

export default Login;
