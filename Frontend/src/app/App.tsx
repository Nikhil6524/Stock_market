import { AppProvider } from "../context/AppContext";
import { AuthProvider } from "../features/auth/context/AuthContext";
import { AppRoutes } from "./routes/AppRoutes";

export function App(): JSX.Element {
  return (
    <AuthProvider>
      <AppProvider>
        <AppRoutes />
      </AppProvider>
    </AuthProvider>
  );
}

