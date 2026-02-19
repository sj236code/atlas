"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Workspace, Suggestion } from "@/types/workspace";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function WorkspacePage() {
  const params = useParams();
  const router = useRouter();
  const workspaceId = params.id as string;
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Try to fetch workspace data from backend
    // For now, if workspaceId starts with "ws_", try to fetch it
    // Otherwise, treat it as a query and create a new workspace
    const fetchWorkspace = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        if (workspaceId.startsWith("ws_")) {
          // TODO: Implement GET endpoint for fetching existing workspace
          // For now, we'll need to store workspace data or recreate it
          setError("Workspace fetching not yet implemented. Creating new workspace...");
          // Fallback: treat as query
          const query = decodeURIComponent(workspaceId);
          const response = await fetch(`${BACKEND_URL}/api/workspace/create`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ query }),
          });
          
          if (response.ok) {
            const data = await response.json();
            console.log("Workspace data received:", data);
            console.log("Suggestions:", data.suggestions);
            setWorkspace(data);
          } else {
            throw new Error("Failed to create workspace");
          }
        } else {
          // Treat as query and create workspace
          const query = decodeURIComponent(workspaceId);
          const response = await fetch(`${BACKEND_URL}/api/workspace/create`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ query }),
          });
          
          if (response.ok) {
            const data = await response.json();
            console.log("Workspace data received:", data);
            console.log("Suggestions:", data.suggestions);
            setWorkspace(data);
          } else {
            throw new Error("Failed to create workspace");
          }
        }
      } catch (err) {
        console.error("Error fetching workspace:", err);
        const errorMessage = err instanceof Error ? err.message : "Failed to load workspace";
        setError(errorMessage);
        console.error("Full error details:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchWorkspace();
  }, [workspaceId]);

  if (isLoading) {
    return (
      <main className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
          <p className="mt-4 text-gray-600 font-medium">Creating your workspace...</p>
          <p className="mt-2 text-sm text-gray-400">This may take a few seconds</p>
        </div>
      </main>
    );
  }

  if (error && !workspace) {
    return (
      <main className="min-h-screen bg-gray-50 flex items-center justify-center p-8">
        <div className="max-w-md w-full bg-white rounded-xl shadow-lg border border-red-200 p-8 text-center">
          <div className="inline-block p-3 bg-red-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Workspace</h2>
          <p className="text-red-600 mb-6">{error}</p>
          <button
            onClick={() => router.push("/")}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Go Back to Search
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {workspace?.schema?.title || "Workspace"}
              </h1>
              <p className="text-sm text-gray-500 mt-1">
                {workspace?.query || decodeURIComponent(workspaceId)}
              </p>
            </div>
            <button
              onClick={() => router.push("/")}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            >
              ← Back to Search
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Workspace layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
          {/* Left Sidebar: Sources */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="font-semibold text-lg mb-4 text-gray-900">Sources</h2>
              <div className="space-y-3">
                {workspace?.enabled_sources?.map((source) => (
                  <label key={source} className="flex items-center gap-3 cursor-pointer group">
                    <input 
                      type="checkbox" 
                      defaultChecked 
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700 group-hover:text-gray-900">
                      {source.charAt(0).toUpperCase() + source.slice(1)}
                    </span>
                  </label>
                )) || (
                  <>
                    {["Web", "Reddit", "YouTube", "Maps", "Academic"].map((source) => (
                      <label key={source} className="flex items-center gap-3 cursor-pointer group">
                        <input 
                          type="checkbox" 
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span className="text-sm text-gray-700 group-hover:text-gray-900">{source}</span>
                      </label>
                    ))}
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Center: Main Tools */}
          <div className="lg:col-span-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 min-h-[400px]">
              <h2 className="font-semibold text-lg mb-4 text-gray-900">Workspace Tools</h2>
              <div className="text-center py-12">
                <div className="inline-block p-4 bg-blue-50 rounded-full mb-4">
                  <svg className="w-12 h-12 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <p className="text-gray-500 text-sm">
                  Workspace content will be generated here based on query type.
                </p>
              </div>
            </div>
          </div>

          {/* Right Sidebar: Saved */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="font-semibold text-lg mb-4 text-gray-900">Saved</h2>
              {workspace?.saved_items && workspace.saved_items.length > 0 ? (
                <div className="space-y-3">
                  {workspace.saved_items.map((item, index) => (
                    <div key={index} className="p-3 bg-gray-50 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors">
                      <p className="font-medium text-sm text-gray-900">{item.title}</p>
                      {item.notes && <p className="text-xs text-gray-500 mt-1">{item.notes}</p>}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-sm text-gray-400">Your saved items will appear here.</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Bottom: AI Suggestions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-6">
            <div className="p-2 bg-purple-100 rounded-lg">
              <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h2 className="font-semibold text-lg text-gray-900">AI Suggestions</h2>
            <span className="ml-auto text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
              {(() => {
                const suggestionsArray = Array.isArray(workspace?.suggestions) ? workspace.suggestions : [];
                return `${suggestionsArray.length} suggestions`;
              })()}
            </span>
          </div>
          
          {(() => {
            const suggestionsArray = Array.isArray(workspace?.suggestions) 
              ? workspace.suggestions 
              : [];
            
            return suggestionsArray.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {suggestionsArray.map((suggestion: Suggestion, index: number) => (
                  <div 
                    key={index} 
                    className="p-5 border-2 border-gray-200 rounded-xl hover:border-blue-300 hover:shadow-md transition-all bg-gradient-to-br from-white to-gray-50"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="font-semibold text-gray-900 text-base leading-tight">
                        {suggestion.title}
                      </h3>
                      {suggestion.category && (
                        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full ml-2 whitespace-nowrap">
                          {suggestion.category}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mb-4 leading-relaxed">
                      {suggestion.reason}
                    </p>
                    {suggestion.evidence && suggestion.evidence.length > 0 && (
                      <div className="mb-4">
                        <p className="text-xs font-medium text-gray-500 mb-2">Evidence Sources:</p>
                        <div className="flex flex-wrap gap-2">
                          {suggestion.evidence.map((evidence, idx) => (
                            <a
                              key={idx}
                              href={evidence.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-xs text-blue-600 hover:text-blue-700 hover:underline bg-blue-50 px-2 py-1 rounded"
                            >
                              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                              </svg>
                              {evidence.label}
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                    <button className="w-full mt-4 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-sm hover:shadow-md">
                      Save to Workspace
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="inline-block p-4 bg-gray-100 rounded-full mb-4">
                  <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <p className="text-sm text-gray-400">Evidence-linked suggestions will appear here.</p>
              </div>
            );
          })()}
        </div>
      </div>
    </main>
  );
}
