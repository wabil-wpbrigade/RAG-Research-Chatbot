import { useEffect, useState } from "react";
import { Routes, Route } from "react-router-dom";
import { getMe } from "./api/api";
import RequestMagicLink from "./pages/RequestMagicLink";
import VerifyMagicLink from "./pages/VerifyMagicLink";
import AdminDashboard from "./components/AdminDashboard";
import RagChat from "./components/RagChat";
import "./styles/App.css";

/**
 * Root application component.
 *
 * Handles authentication restoration, routing,
 * and top-level UI state such as tabs and logout.
 */
function App() {
  /** Auth & UI state */
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("chat");

  /**
   * Restore user session using stored JWT token.
   */
  async function loadUser() {
    const token = getStoredToken();
    if (!token) return stopLoading();
    await fetchCurrentUser();
  }

  /**
   * Fetch authenticated user from backend.
   */
  async function fetchCurrentUser() {
    try {
      setUser(await getMe());
    } catch {
      clearSession();
    } finally {
      stopLoading();
    }
  }

  /**
   * Clear auth session and log out user.
   */
  function logout() {
    clearSession();
    setUser(null);
  }

  /** Helpers */
  function getStoredToken() {
    return localStorage.getItem("token");
  }

  function clearSession() {
    localStorage.removeItem("token");
  }

  function stopLoading() {
    setLoading(false);
  }

  useEffect(() => {
    loadUser();
  }, []);

  if (loading) return <div className="center">Loading…</div>;

  return (
    <Routes>
      {/* Magic link verification */}
      <Route path="/auth/magic" element={<VerifyMagicLink />} />

      {/* Main app */}
      <Route
        path="/"
        element={
          !user ? (
            <div className="center">
              <RequestMagicLink onLogin={loadUser} />
            </div>
          ) : (
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

                <Tabs
                  user={user}
                  activeTab={activeTab}
                  setActiveTab={setActiveTab}
                />

                <section className="section">
                  {activeTab === "chat" && <RagChat />}
                  {activeTab === "admin" && user.is_admin && (
                    <AdminDashboard />
                  )}
                </section>
              </div>
            </div>
          )
        }
      />
    </Routes>
  );
}

/**
 * Tab navigation component.
 */
function Tabs({ user, activeTab, setActiveTab }) {
  return (
    <div className="tabs">
      <TabButton
        label="Chat"
        active={activeTab === "chat"}
        onClick={() => setActiveTab("chat")}
      />

      {user.is_admin && (
        <TabButton
          label="Admin"
          active={activeTab === "admin"}
          onClick={() => setActiveTab("admin")}
        />
      )}
    </div>
  );
}

/**
 * Reusable tab button.
 */
function TabButton({ label, active, onClick }) {
  return (
    <button
      className={`tab ${active ? "active" : ""}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
}

export default App;
