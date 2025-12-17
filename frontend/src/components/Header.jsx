function Header({ user, onLogout }) {
    return (
        <header className="header">
            <div>
                <strong>{user.name}</strong>
                <span className="email">{user.email}</span>
                {user.is_admin && <span className="badge">Admin</span>}
            </div>

            <button onClick={onLogout}>Logout</button>
        </header>
    );
}

export default Header;
