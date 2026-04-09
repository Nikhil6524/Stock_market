import { useState } from "react";

export function useApi(): {
  loading: boolean;
  error: string | null;
  run: <T>(task: () => Promise<T>) => Promise<T>;
  clearError: () => void;
} {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async <T,>(task: () => Promise<T>): Promise<T> => {
    setLoading(true);
    setError(null);
    try {
      return await task();
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unexpected error.";
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    run,
    clearError: () => setError(null),
  };
}

