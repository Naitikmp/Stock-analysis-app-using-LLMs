'use client';

import { useState } from 'react';

interface AnalysisResponse {
  analysis: string;
  error?: string;
}

export default function StockAnalyzer() {
  const [apiKey, setApiKey] = useState('');
  const [stock, setStock] = useState('');
  const [analysis, setAnalysis] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const analyzeStock = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setAnalysis('');

    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          apiKey,
          stock,
        }),
      });

      const data: AnalysisResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to analyze stock');
      }

      setAnalysis(data.analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-100 py-12 px-4">
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-md p-6">
        <h1 className="text-2xl font-bold text-center mb-8 text-slate-800">Stock Analyzer</h1>
        
        <form onSubmit={analyzeStock} className="space-y-6">
          <div>
            <label htmlFor="apiKey" className="block text-sm font-medium text-slate-950">
              OpenAI API Key
            </label>
            <input
              type="password"
              id="apiKey"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="mt-1 block w-full rounded-lg border border-slate-300 p-2.5 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              required
            />
          </div>
          
          <div>
            <label htmlFor="stock" className="block text-sm font-medium text-slate-950">
              Stock Name
            </label>
            <input
              type="text"
              id="stock"
              value={stock}
              onChange={(e) => setStock(e.target.value)}
              className="mt-1 block w-full rounded-lg border border-slate-300 text-slate-950 p-2.5 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              placeholder="Enter stock name"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className={`w-full flex justify-center py-2.5 px-4 rounded-lg text-sm font-semibold text-white transition-colors
              ${loading ? 'bg-slate-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
          >
            {loading ? 'Analyzing...' : 'Analyze Stock'}
          </button>
        </form>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        {analysis && (
          <div className="mt-6 p-4 bg-slate-50 rounded-lg">
            <h2 className="text-lg font-medium mb-2 text-slate-800">Analysis Result:</h2>
            <div className="whitespace-pre-wrap text-sm text-slate-600">
              {analysis}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}