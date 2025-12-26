import { useEffect, useState } from "react";
import {
    fetchUsers,
    toggleUserActive,
    createUser,
    getMe,
} from "../api/api";
import "../styles/AdminDashboard.css";

/**
 * Admin dashboard for managing users and roles.
 */
export default function AdminDashboard() {
    const [users, setUsers] = useState([]);
    const [currentUser, setCurrentUser] = useState(null);
    const [statusFilter, setStatusFilter] = useState("all");

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isAdmin, setIsAdmin] = useState(false);
    const [error, setError] = useState("");

    /**
     * Fetch all users from the backend.
     */
    async function loadUsers() {
        try {
            setUsers(await fetchUsers(localStorage.getItem("token")));
        } catch {
            setError("Failed to load users");
        }
    }

    /**
     * Fetch the currently authenticated user.
     */
    async function loadCurrentUser() {
        try {
            setCurrentUser(await getMe());
        } catch {
            setError("Failed to load current user");
        }
    }

    /**
     * Reset create-user form state.
     */
    function resetForm() {
        setName("");
        setEmail("");
        setPassword("");
        setIsAdmin(false);
    }

    /**
     * Handle user creation form submission.
     */
    async function handleCreate(e) {
        e.preventDefault();
        setError("");
        try {
            await createUser(name, email, password, isAdmin);
            resetForm();
            loadUsers();
        } catch (err) {
            setError(err.message);
        }
    }

    /**
     * Toggle a user's active status.
     */
    async function toggle(id) {
        setError("");
        try {
            await toggleUserActive(localStorage.getItem("token"), id);
            loadUsers();
        } catch (err) {
            setError(err.message || "Action not allowed");
        }
    }

    /**
     * Apply status-based user filtering.
     */
    function filterUsers(list) {
        if (statusFilter === "active") return list.filter(u => u.is_active);
        if (statusFilter === "inactive") return list.filter(u => !u.is_active);
        return list;
    }

    useEffect(() => {
        loadUsers();
        loadCurrentUser();
    }, []);

    const filteredUsers = filterUsers(users);

    return (
        <div className="admin-container">
            <h2>Admin Dashboard</h2>

            <form className="create-user-card" onSubmit={handleCreate}>
                <h3>Create User</h3>
                <p className="card-subtitle">Add a new user to the system</p>

                {error && <p className="error">{error}</p>}

                <div className="form-grid">
                    <input
                        placeholder="Full Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                    <input
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <div className="role-selector">
                    <span className="role-label">Role</span>

                    <label className={!isAdmin ? "active" : ""}>
                        <input
                            type="radio"
                            checked={!isAdmin}
                            onChange={() => setIsAdmin(false)}
                        />
                        User
                    </label>

                    <label className={isAdmin ? "active" : ""}>
                        <input
                            type="radio"
                            checked={isAdmin}
                            onChange={() => setIsAdmin(true)}
                        />
                        Admin
                    </label>
                </div>

                <button type="submit" className="primary">
                    Create User
                </button>
            </form>

            <div className="table-card">
                <h3>Users</h3>

                <div className="filter-bar">
                    <span className="filter-label">Status:</span>

                    {["all", "active", "inactive"].map((s) => (
                        <label
                            key={s}
                            className={statusFilter === s ? "active" : ""}
                        >
                            <input
                                type="radio"
                                checked={statusFilter === s}
                                onChange={() => setStatusFilter(s)}
                            />
                            {s.charAt(0).toUpperCase() + s.slice(1)}
                        </label>
                    ))}
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Admin</th>
                            <th>Active</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {filteredUsers.map((u) => {
                            const isSelf = currentUser && u.id === currentUser.id;

                            return (
                                <tr key={u.id}>
                                    <td>{u.id}</td>
                                    <td>{u.name}</td>
                                    <td>{u.email}</td>
                                    <td>{u.is_admin ? "Yes" : "No"}</td>
                                    <td>{u.is_active ? "Yes" : "No"}</td>
                                    <td>
                                        <button
                                            className={u.is_active ? "danger" : "success"}
                                            disabled={isSelf}
                                            title={isSelf ? "You cannot deactivate your own account" : ""}
                                            onClick={() => toggle(u.id)}
                                        >
                                            {u.is_active ? "Deactivate" : "Activate"}
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}

                        {filteredUsers.length === 0 && (
                            <tr>
                                <td colSpan="6" style={{ textAlign: "center" }}>
                                    No users found
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
