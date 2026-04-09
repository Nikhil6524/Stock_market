type SidebarProps = {
  userName: string;
  onLogout: () => void;
};

export function Sidebar({ userName, onLogout }: SidebarProps): JSX.Element {
  return (
    <aside className="sidebar">
      <div>
        <h1 className="brand">Stock Broker</h1>
        <p className="muted">Virtual Trading Desk</p>
      </div>
      <div className="sidebar-user">
        <p>{userName}</p>
        <button className="ghost-btn" onClick={onLogout}>
          Logout
        </button>
      </div>
    </aside>
  );
}

