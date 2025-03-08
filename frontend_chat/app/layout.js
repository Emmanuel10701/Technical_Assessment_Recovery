import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Footer from "./components/footer";
import Navbar from "./components/navbar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "AI Chat Assistant Pro",
  description:
    "Experience intelligent, real-time conversations with our AI chat assistant, built with Next.js and React.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased transition-all duration-300 bg-white text-gray-900 dark:bg-gray-900 dark:text-white`}
      >
          <Navbar />
          <main>{children}</main>
          <Footer />
      </body>
    </html>
  );
}
