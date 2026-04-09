import type { PropsWithChildren } from "react";
import { Sidebar } from "../ui/Sidebar";

type MainLayoutProps = PropsWithChildren<{
  userName: string;
  onLogout: () => void;
}>;

export function MainLayout({
  userName,
  onLogout,
  children,
}: MainLayoutProps): JSX.Element {
  return (
    <div className="app-shell">
      <Sidebar userName={userName} onLogout={onLogout} />
      <main className="content">{children}</main>
    </div>
  );
}

