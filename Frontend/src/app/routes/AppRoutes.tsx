import { MainLayout } from "../../layouts/layout/MainLayout";
import { LoginForm } from "../../features/auth/components/LoginForm";
import { useAuth } from "../../features/auth/hooks/useAuth";
import { useAppContext } from "../../context/AppContext";
import { DashboardPage } from "../../features/dashboard/components/DashboardPage";

export function AppRoutes(): JSX.Element {
  const { token, logout, user } = useAuth();
  const { activeScreen } = useAppContext();

  if (!token) {
    return <LoginForm />;
  }

  return (
    <MainLayout userName={user?.username ?? "Trader"} onLogout={logout}>
      {activeScreen === "dashboard" ? <DashboardPage /> : <DashboardPage />}
    </MainLayout>
  );
}

