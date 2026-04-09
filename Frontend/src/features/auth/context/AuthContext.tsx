import { createContext, useContext, useEffect, useState } from "react";
import type { PropsWithChildren } from "react";
import { login as loginApi, register as registerApi } from "../services/AuthService";

type AuthUser = {
  userId: string;
  username: string;
};

type AuthContextValue = {
  token: string | null;
  user: AuthUser | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
};

const TOKEN_KEY = "stock_broker_token";
const USER_KEY = "stock_broker_user";

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: PropsWithChildren): JSX.Element {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    const savedToken = localStorage.getItem(TOKEN_KEY);
    const savedUser = localStorage.getItem(USER_KEY);
    if (savedToken) {
      setToken(savedToken);
    }
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser) as AuthUser);
      } catch {
        setUser(null);
      }
    }
  }, []);

  const persist = (newToken: string, newUser: AuthUser): void => {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem(TOKEN_KEY, newToken);
    localStorage.setItem(USER_KEY, JSON.stringify(newUser));
  };

  const login = async (username: string, password: string): Promise<void> => {
    const result = await loginApi(username, password);
    persist(result.token, { userId: result.user_id, username: result.username });
  };

  const register = async (username: string, password: string): Promise<void> => {
    const result = await registerApi(username, password);
    persist(result.token, { userId: result.user_id, username: result.username });
  };

  const logout = (): void => {
    setToken(null);
    setUser(null);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  };

  return (
    <AuthContext.Provider value={{ token, user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuthContext(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuthContext must be used within AuthProvider.");
  }
  return context;
}

