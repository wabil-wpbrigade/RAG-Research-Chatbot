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

    // Create user form
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

    return (
        <div className="admin-container">
            <h2>Admin Dashboard</h2>

            {/* 🔹 CREATE USER */}
            <form className="create-user-card" onSubmit={handleCreate}>
                <h3>Create User</h3>

                {error && <p className="error">{error}</p>}

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

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <div className="radio-group">
                    <label>
                        <input
                            type="radio"
                            name="role"
                            checked={!isAdmin}
                            onChange={() => setIsAdmin(false)}
                        />
                        User
                    </label>

                    <label>
                        <input
                            type="radio"
                            name="role"
                            checked={isAdmin}
                            onChange={() => setIsAdmin(true)}
                        />
                        Admin
                    </label>
                </div>

                <button type="submit">Create</button>
            </form>

            {/* 🔹 USER TABLE */}
            <div className="table-card">
                <h3>Users</h3>

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
                        {users.map((u) => {
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

                        {users.length === 0 && (
                            <tr>
                                <td
                                    colSpan="6"
                                    style={{ textAlign: "center" }}
                                >
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
