import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Search, MapPin, Phone, Package, ArrowRight, TrendingUp } from 'lucide-react';

interface Retailer {
  name: string;
  contact: string;
  place: string;
  moq: number;
  score: number;
  avg_quality: number;
  avg_unit_cost: number;
  total_past_orders: number;
}

interface ApiResponse {
  status: string;
  extracted_target: string;
  requested_quantity: number;
  ranked_leaderboard: Retailer[];
  markdown_report: string;
}

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [leaderboard, setLeaderboard] = useState<Retailer[] | null>(null);
  const [report, setReport] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [profile, setProfile] = useState<string>('Balanced');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setLeaderboard(null);
    setReport(null);

    try {
      let weight_price = 0.34;
      let weight_delivery = 0.33;
      let weight_quality = 0.33;

      if (profile === 'Lowest Cost Strategy') {
        weight_price = 0.70;
        weight_delivery = 0.15;
        weight_quality = 0.15;
      } else if (profile === 'Fastest Delivery Speed') {
        weight_price = 0.15;
        weight_delivery = 0.70;
        weight_quality = 0.15;
      }

      const response = await fetch('http://127.0.0.1:8000/api/procure/rank', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          user_query: query,
          weight_price,
          weight_delivery,
          weight_quality
        }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      const data: ApiResponse = await response.json();
      setLeaderboard(data.ranked_leaderboard);
      setReport(data.markdown_report);
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching data.');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'var(--accent)';
    if (score >= 70) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="app-container">
      <div className="top-bar">
        <form className="search-form" onSubmit={handleSubmit}>
          <input
            type="text"
            className="search-input"
            placeholder="Ask Procurement Agent (e.g. 'I need 50 laptops for the CS department')"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />
          <button type="submit" className="search-button" disabled={loading || !query.trim()}>
            {loading ? <div className="loader" /> : <Search size={20} />}
          </button>
        </form>
      </div>

      <div className="config-row">
        <span className="config-label">Optimization Profiles:</span>
        <div className="profile-tabs">
          {['Balanced', 'Lowest Cost Strategy', 'Fastest Delivery Speed'].map((p) => (
            <button
              key={p}
              type="button"
              className={`profile-tab ${profile === p ? 'active' : ''}`}
              onClick={() => setProfile(p)}
              disabled={loading}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      <div className="split-layout">
        <div className="left-column">
          <h2 className="column-title">
            <TrendingUp size={24} /> Ranked Suppliers
          </h2>
          
          {loading && (
            <div className="leaderboard-list">
              {[1, 2, 3].map((i) => (
                <div key={i} className="leaderboard-card skeleton" style={{ height: '100px' }}></div>
              ))}
            </div>
          )}

          {error && <div className="empty-state" style={{ color: '#ef4444' }}>{error}</div>}

          {!loading && !error && !leaderboard && (
            <div className="empty-state">
              <Package size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
              <p>Submit a query to see supplier rankings</p>
            </div>
          )}

          {!loading && leaderboard && leaderboard.length === 0 && (
            <div className="empty-state">
              <p>No suitable suppliers found for this request.</p>
            </div>
          )}

          {!loading && leaderboard && leaderboard.length > 0 && (
            <div className="leaderboard-list">
              {leaderboard.map((retailer, index) => (
                <div key={index} className="leaderboard-card">
                  <div className="score-badge" style={{ borderColor: getScoreColor(retailer.score), color: getScoreColor(retailer.score) }}>
                    {retailer.score}
                    <span>Score</span>
                  </div>
                  
                  <div className="card-content">
                    <h3 className="retailer-name">{retailer.name}</h3>
                    <div className="retailer-meta">
                      <span className="meta-item"><MapPin size={14} /> {retailer.place}</span>
                      <span className="meta-item"><Phone size={14} /> {retailer.contact}</span>
                      <span className="meta-item"><Package size={14} /> {retailer.total_past_orders} past orders</span>
                    </div>
                  </div>
                  
                  <div className="card-actions">
                    <ArrowRight size={20} color="var(--text-muted)" />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="right-column">
          <h2 className="column-title">
            <Package size={24} /> AI Analysis Report
          </h2>
          
          {loading && (
            <div className="skeleton" style={{ height: '100%', borderRadius: '12px' }}></div>
          )}

          {!loading && !report && !error && (
            <div className="empty-state">
              <p>AI report will appear here</p>
            </div>
          )}

          {!loading && report && (
            <div className="markdown-body">
              <ReactMarkdown>{report}</ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
