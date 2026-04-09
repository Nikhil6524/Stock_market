import { FormEvent, useState } from "react";
import { useAuth } from "../hooks/useAuth";

export function LoginForm(): JSX.Element {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (mode === "login") {
        await login(username, password);
      } else {
        await register(username, password);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-shell">
      <form className="auth-card" onSubmit={onSubmit}>
        <h2>{mode === "login" ? "Login" : "Register"}</h2>
        <p className="muted">
          {mode === "login"
            ? "Sign in to access your virtual trading wallet."
            : "Create a user and start virtual trading."}
        </p>
        <label>
          Username
          <input
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            minLength={3}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            minLength={6}
            required
          />
        </label>
        {error ? <p className="error">{error}</p> : null}
        <button type="submit" disabled={loading}>
          {loading ? "Please wait..." : mode === "login" ? "Login" : "Register"}
        </button>
        <button
          className="ghost-btn"
          type="button"
          onClick={() => setMode(mode === "login" ? "register" : "login")}
        >
          {mode === "login" ? "Need an account? Register" : "Already a user? Login"}
        </button>
      </form>
    </div>
  );
}

