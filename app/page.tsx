"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function Home() {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      setIsLoading(true);
      try {
        console.log("Calling backend API:", `${BACKEND_URL}/api/workspace/create`);
        console.log("Query:", query.trim());
        
        // Call backend API to create workspace
        const response = await fetch(`${BACKEND_URL}/api/workspace/create`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: query.trim() }),
        });

        console.log("Response status:", response.status);
        
        if (!response.ok) {
          const errorText = await response.text();
          console.error("API Error:", errorText);
          throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const workspace = await response.json();
        console.log("Workspace created:", workspace);
        
        // Navigate to workspace page with workspace ID
        router.push(`/workspace/${workspace.id}`);
      } catch (error) {
        console.error("Error creating workspace:", error);
        alert(`Error: ${error instanceof Error ? error.message : "Failed to create workspace. Check console for details."}`);
        // Fallback: navigate with query if API fails
        router.push(`/workspace/${encodeURIComponent(query)}`);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const promptChips = [
    "Plan a Japan trip focused on food & affordability",
    "Find a gym routine for beginners",
    "Choose a laptop for CS student under $900",
    "Build a 4-week React learning plan",
  ];

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 md:p-24 bg-gradient-to-b from-gray-50 to-white">
      <div className="z-10 w-full max-w-5xl items-center justify-center">
        {/* Logo */}
        <div className="text-center mb-12">
          <h1 className="text-7xl md:text-8xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Atlas
          </h1>
          <p className="text-gray-600 text-lg">AI-powered research workspace</p>
        </div>
        
        {/* Search Bar */}
        <form onSubmit={handleSubmit} className="w-full mb-8">
          <div className="flex flex-col items-center gap-4">
            <div className="relative w-full max-w-2xl">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for anything..."
                className="w-full px-6 py-4 pr-32 text-lg text-gray-900 bg-white border-2 border-gray-200 rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
              <button
                type="submit"
                disabled={isLoading}
                className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
              >
                {isLoading ? "..." : "Search"}
              </button>
            </div>
          </div>
        </form>

        {/* Prompt Chips */}
        <div className="flex flex-wrap justify-center gap-3 mt-8">
          {promptChips.map((prompt, index) => (
            <button
              key={index}
              onClick={async () => {
                setQuery(prompt);
                setIsLoading(true);
                try {
                  const response = await fetch(`${BACKEND_URL}/api/workspace/create`, {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ query: prompt }),
                  });

                  if (response.ok) {
                    const workspace = await response.json();
                    router.push(`/workspace/${workspace.id}`);
                  } else {
                    router.push(`/workspace/${encodeURIComponent(prompt)}`);
                  }
                } catch (error) {
                  console.error("Error creating workspace:", error);
                  router.push(`/workspace/${encodeURIComponent(prompt)}`);
                } finally {
                  setIsLoading(false);
                }
              }}
              className="px-5 py-2.5 text-sm bg-white border border-gray-200 hover:border-blue-300 hover:bg-blue-50 rounded-full transition-all shadow-sm hover:shadow-md text-gray-700 hover:text-blue-700"
            >
              {prompt}
            </button>
          ))}
        </div>

        {/* Navigation */}
        <nav className="flex justify-center gap-6 mt-16 text-sm text-gray-600">
          <a href="#" className="hover:text-gray-900 transition-colors">Workspaces</a>
          <a href="#" className="hover:text-gray-900 transition-colors">Premium</a>
          <a href="#" className="hover:text-gray-900 transition-colors">About</a>
        </nav>
      </div>
    </main>
  );
}
