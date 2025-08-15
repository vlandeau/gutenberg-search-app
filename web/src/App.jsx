import { useState } from 'react'

const API_BASE = import.meta.env.DEV ? 'http://localhost:8000' : '';

function App() {
  const [query, setQuery] = useState('')
  const [activeTab, setActiveTab] = useState('autocomplete')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [suggestions, setSuggestions] = useState([])

  const handleSearch = async () => {
    if (!query.trim()) return
    
    setLoading(true)
    try {
      let url
      switch (activeTab) {
        case 'autocomplete':
          url = `${API_BASE}/autocomplete?q=${encodeURIComponent(query)}&limit=10`
          break
        case 'regex':
          url = `${API_BASE}/search/regex?pattern=${encodeURIComponent(query)}&case_insensitive=true`
          break
        case 'fuzzy':
          url = `${API_BASE}/search/fuzzy?term=${encodeURIComponent(query)}&k=1`
          break
      }
      
      const response = await fetch(url)
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Search error:', error)
      setResults({ error: 'Search failed' })
    } finally {
      setLoading(false)
    }
  }

  const handleAutocomplete = async (value) => {
    if (value.length < 1) {
      setSuggestions([])
      return
    }
    
    try {
      const response = await fetch(`${API_BASE}/autocomplete?q=${encodeURIComponent(value)}&limit=5`)
      const data = await response.json()
      setSuggestions(data.suggestions || [])
    } catch (error) {
      setSuggestions([])
    }
  }

  const renderResults = () => {
    if (!results) return null
    
    if (results.error) {
      return <div className="text-red-500 p-4 bg-red-50 rounded">Error: {results.error}</div>
    }

    switch (activeTab) {
      case 'autocomplete':
        return (
          <div className="space-y-2">
            <h3 className="font-semibold text-lg">Suggestions:</h3>
            {results.suggestions?.length > 0 ? (
              <ul className="list-disc list-inside space-y-1">
                {results.suggestions.map((suggestion, i) => (
                  <li key={i} className="text-blue-600 hover:underline cursor-pointer"
                      onClick={() => setQuery(suggestion)}>
                    {suggestion}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No suggestions found</p>
            )}
          </div>
        )
        
      case 'regex':
        return (
          <div className="space-y-4">
            <h3 className="font-semibold text-lg">Regex Matches:</h3>
            {results.results?.length > 0 ? (
              results.results.map((book, i) => (
                <div key={i} className="border rounded p-4 bg-gray-50">
                  <h4 className="font-semibold text-blue-600">{book.title}</h4>
                  <div className="mt-2 space-y-2">
                    {book.hits.map((hit, j) => (
                      <div key={j} className="text-sm bg-yellow-100 p-2 rounded">
                        <span className="text-gray-600">Position {hit.start}-{hit.end}:</span>
                        <div className="mt-1 font-mono text-xs">{hit.context}</div>
                      </div>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500">No matches found</p>
            )}
          </div>
        )
        
      case 'fuzzy':
        return (
          <div className="space-y-4">
            <h3 className="font-semibold text-lg">Fuzzy Matches:</h3>
            {results.results?.length > 0 ? (
              <div className="space-y-2">
                {results.results.map((result, i) => (
                  <div key={i} className="border rounded p-3 bg-gray-50">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-blue-600">{result.title}</span>
                      <span className="text-xs text-gray-500">Distance: {result.distance}</span>
                    </div>
                    <div className="text-sm text-gray-600 mt-1">
                      Token: "{result.token}" ({result.count} occurrences)
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No fuzzy matches found</p>
            )}
          </div>
        )
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
            Gutenberg Search Engine
          </h1>
          
          {/* Search Input */}
          <div className="relative mb-6">
            <input
              type="text"
              value={query}
              onChange={(e) => {
                setQuery(e.target.value)
                if (activeTab === 'autocomplete') {
                  handleAutocomplete(e.target.value)
                }
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSearch()
                }
              }}
              placeholder={`Enter your ${activeTab} query...`}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            
            {/* Live Autocomplete Dropdown */}
            {activeTab === 'autocomplete' && suggestions.length > 0 && (
              <div className="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-lg mt-1 shadow-lg z-10">
                {suggestions.map((suggestion, i) => (
                  <div
                    key={i}
                    className="px-4 py-2 hover:bg-blue-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                    onClick={() => {
                      setQuery(suggestion)
                      setSuggestions([])
                    }}
                  >
                    {suggestion}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Tab Navigation */}
          <div className="flex space-x-1 mb-6 bg-gray-200 p-1 rounded-lg">
            {['autocomplete', 'regex', 'fuzzy'].map((tab) => (
              <button
                key={tab}
                onClick={() => {
                  setActiveTab(tab)
                  setResults(null)
                  setSuggestions([])
                }}
                className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
                  activeTab === tab
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>

          {/* Search Button */}
          <button
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>

          {/* Results */}
          {results && (
            <div className="mt-8">
              {renderResults()}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App