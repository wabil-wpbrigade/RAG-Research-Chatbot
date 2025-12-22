import { useEffect, useState } from "react";
import {
    fetchUsers,
    toggleUserActive,
    createUser,
    getMe,
} from "../api/api";
import "../styles/AdminDashboard.css";

export default function AdminDashboard() {
    const [users, setUsers] = useState([]);
    const [currentUser, setCurrentUser] = useState(null);

    // 🔹 Filter state
    const [statusFilter, setStatusFilter] = useState("all");
    // "all" | "active" | "inactive"

    // 🔹 Create user form
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isAdmin, setIsAdmin] = useState(false);
    const [error, setError] = useState("");

    async function loadUsers() {
        try {
            const data = await fetchUsers(localStorage.getItem("token"));
            setUsers(data);
        } catch {
            setError("Failed to load users");
        }
    }

    async function loadCurrentUser() {
        try {
            const me = await getMe();
            setCurrentUser(me);
        } catch {
            setError("Failed to load current user");
        }
    }

    async function handleCreate(e) {
        e.preventDefault();
        setError("");

        try {
            await createUser(name, email, password, isAdmin);
            setName("");
            setEmail("");
            setPassword("");
            setIsAdmin(false);
            loadUsers();
        } catch (err) {
            setError(err.message);
        }
    }

    async function toggle(id) {
        setError("");

        try {
            await toggleUserActive(localStorage.getItem("token"), id);
            loadUsers();
        } catch (err) {
            setError(err.message || "Action not allowed");
        }
    }

    useEffect(() => {
        loadUsers();
        loadCurrentUser();
    }, []);

    // 🔹 Apply filter
    const filteredUsers = users.filter((u) => {
        if (statusFilter === "active") return u.is_active;
        if (statusFilter === "inactive") return !u.is_active;
        return true;
    });

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
                            name="role"
                            checked={!isAdmin}
                            onChange={() => setIsAdmin(false)}
                        />
                        User
                    </label>

                    <label className={isAdmin ? "active" : ""}>
                        <input
                            type="radio"
                            name="role"
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
            {/* 🔹 USER TABLE */}
            <div className="table-card">
                <h3>Users</h3>

                {/* 🔹 Status Filter */}
                <div className="filter-bar">
                    <span className="filter-label">Status:</span>

                    <label className={statusFilter === "all" ? "active" : ""}>
                        <input
                            type="radio"
                            name="statusFilter"
                            checked={statusFilter === "all"}
                            onChange={() => setStatusFilter("all")}
                        />
                        All
                    </label>

                    <label className={statusFilter === "active" ? "active" : ""}>
                        <input
                            type="radio"
                            name="statusFilter"
                            checked={statusFilter === "active"}
                            onChange={() => setStatusFilter("active")}
                        />
                        Active
                    </label>

                    <label className={statusFilter === "inactive" ? "active" : ""}>
                        <input
                            type="radio"
                            name="statusFilter"
                            checked={statusFilter === "inactive"}
                            onChange={() => setStatusFilter("inactive")}
                        />
                        Inactive
                    </label>
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
                            const isSelf =
                                currentUser && u.id === currentUser.id;

                            return (
                                <tr key={u.id}>
                                    <td>{u.id}</td>
                                    <td>{u.name}</td>
                                    <td>{u.email}</td>
                                    <td>{u.is_admin ? "Yes" : "No"}</td>
                                    <td>{u.is_active ? "Yes" : "No"}</td>
                                    <td>
                                        <button
                                            className={
                                                u.is_active
                                                    ? "danger"
                                                    : "success"
                                            }
                                            disabled={isSelf}
                                            title={
                                                isSelf
                                                    ? "You cannot deactivate your own account"
                                                    : ""
                                            }
                                            onClick={() => toggle(u.id)}
                                        >
                                            {u.is_active
                                                ? "Deactivate"
                                                : "Activate"}
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
