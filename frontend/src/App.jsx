import { useEffect, useState } from "react";
import { getMe } from "./api/api";
import Login from "./pages/Login";
import AdminDashboard from "./components/AdminDashboard";
import RagChat from "./components/RagChat";
import "./styles/App.css";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("chat"); // chat | admin

  async function loadUser() {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      const me = await getMe(token);
      setUser(me);
    } catch {
      localStorage.removeItem("token");
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    localStorage.removeItem("token");
    setUser(null);
  }

  useEffect(() => {
    loadUser();
  }, []);

  if (loading) return <div className="center">Loading…</div>;

  if (!user) {
    return (
      <div className="center">
        <Login onLogin={loadUser} />
      </div>
    );
  }

  return (
    <div className="app-bg">
      <div className="app-card">
        <header className="app-header">
          <div>
            <h2>Research Assistant</h2>
            <p className="muted">{user.email}</p>
          </div>
          <button className="logout-btn" onClick={logout}>
            Logout
          </button>
        </header>

        {/* Tabs */}
        <div className="tabs">
          <button
            className={`tab ${activeTab === "chat" ? "active" : ""}`}
            onClick={() => setActiveTab("chat")}
          >
            Chat
          </button>

          {user.is_admin && (
            <button
              className={`tab ${activeTab === "admin" ? "active" : ""}`}
              onClick={() => setActiveTab("admin")}
            >
              Admin
            </button>
          )}
        </div>

        {/* Tab Content */}
        <section className="section">
          {activeTab === "chat" && <RagChat />}
          {activeTab === "admin" && user.is_admin && <AdminDashboard />}
        </section>
      </div>
    </div>
  );
}

export default App;
