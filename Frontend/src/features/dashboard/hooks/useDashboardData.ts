import { useEffect, useState } from "react";
import { apiRequest } from "../../../lib/api";
import { useAuth } from "../../auth/hooks/useAuth";

export type Watchlist = {
  id: string;
  title: string;
  stocks: string[];
};

export type Quote = {
  symbol: string;
  price: number;
  timestamp: string;
  currency: string;
};

export type Candle = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

export type CompanyInfo = {
  symbol: string;
  name: string;
  sector: string;
  industry: string;
  description: string;
  website: string;
};

export type Holding = {
  symbol: string;
  quantity: number;
  average_price: number;
  current_price: number;
  market_value: number;
};

export type Portfolio = {
  holdings: Holding[];
  cash_balance: number;
  total_stock_value: number;
  total_value: number;
};

export type Funds = {
  available_cash: number;
};

export type Order = {
  id: string;
  user_id: string;
  symbol: string;
  side: "BUY" | "SELL";
  quantity: number;
  price: number;
  total_amount: number;
  status: string;
  created_at: string;
};

export type SearchResult = {
  symbol: string;
  display_name: string;
};

export function useDashboardData() {
  const { token } = useAuth();
  const [watchlists, setWatchlists] = useState<Watchlist[]>([]);
  const [activeWatchlistId, setActiveWatchlistId] = useState<string | null>(null);
  const [quote, setQuote] = useState<Quote | null>(null);
  const [history, setHistory] = useState<Candle[]>([]);
  const [company, setCompany] = useState<CompanyInfo | null>(null);
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [funds, setFunds] = useState<Funds | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const withLoading = async <T,>(task: () => Promise<T>): Promise<T> => {
    setLoading(true);
    setError(null);
    try {
      return await task();
    } catch (err) {
      const message = err instanceof Error ? err.message : "Request failed.";
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const refreshWatchlists = async (): Promise<void> => {
    if (!token) return;
    const items = await withLoading(() =>
      apiRequest<Watchlist[]>("/watchlists", { token }),
    );
    setWatchlists(items);
    if (items.length > 0 && !activeWatchlistId) {
      setActiveWatchlistId(items[0].id);
    }
  };

  const createWatchlist = async (title: string): Promise<void> => {
    if (!token) return;
    const created = await withLoading(() =>
      apiRequest<Watchlist>("/watchlists", {
        method: "POST",
        token,
        body: { title },
      }),
    );
    const next = [...watchlists, created];
    setWatchlists(next);
    setActiveWatchlistId(created.id);
  };

  const addStockToWatchlist = async (
    watchlistId: string,
    symbol: string,
  ): Promise<void> => {
    if (!token) return;
    const updated = await withLoading(() =>
      apiRequest<Watchlist>(`/watchlists/${watchlistId}/stocks`, {
        method: "POST",
        token,
        body: { symbol },
      }),
    );
    setWatchlists((prev) => prev.map((item) => (item.id === watchlistId ? updated : item)));
    setSearchResults([]);
  };

  const findSymbols = async (query: string): Promise<void> => {
    if (!query || query.length < 2) {
      setSearchResults([]);
      return;
    }
    const results = await apiRequest<SearchResult[]>(
      `/market/search?q=${encodeURIComponent(query)}`,
    );
    setSearchResults(results);
  };

  const loadQuote = async (symbol: string): Promise<void> => {
    const result = await withLoading(() =>
      apiRequest<Quote>(`/market/quote?symbol=${encodeURIComponent(symbol)}`),
    );
    setQuote(result);
  };

  const loadHistory = async (
    symbol: string,
    period = "1mo",
    interval = "1d",
  ): Promise<void> => {
    const result = await withLoading(() =>
      apiRequest<Candle[]>(
        `/market/history?symbol=${encodeURIComponent(symbol)}&period=${encodeURIComponent(period)}&interval=${encodeURIComponent(interval)}`,
      ),
    );
    setHistory(result);
  };

  const loadCompany = async (symbol: string): Promise<void> => {
    const result = await withLoading(() =>
      apiRequest<CompanyInfo>(`/market/company?symbol=${encodeURIComponent(symbol)}`),
    );
    setCompany(result);
  };

  const refreshTradingData = async (): Promise<void> => {
    if (!token) return;
    const [nextFunds, nextPortfolio, nextOrders] = await withLoading(async () => {
      const fundsResult = await apiRequest<Funds>("/trading/funds", { token });
      const portfolioResult = await apiRequest<Portfolio>("/trading/portfolio", { token });
      const ordersResult = await apiRequest<Order[]>("/trading/orders", { token });
      return [fundsResult, portfolioResult, ordersResult] as const;
    });
    setFunds(nextFunds);
    setPortfolio(nextPortfolio);
    setOrders(nextOrders);
  };

  const placeOrder = async (
    symbol: string,
    side: "BUY" | "SELL",
    quantity: number,
  ): Promise<void> => {
    if (!token) return;
    await withLoading(() =>
      apiRequest<Order>("/trading/orders", {
        method: "POST",
        token,
        body: { symbol, side, quantity },
      }),
    );
    await refreshTradingData();
  };

  useEffect(() => {
    if (!token) return;
    void refreshWatchlists();
    void refreshTradingData();
  }, [token]);

  return {
    loading,
    error,
    watchlists,
    activeWatchlistId,
    setActiveWatchlistId,
    quote,
    history,
    company,
    funds,
    portfolio,
    orders,
    searchResults,
    refreshWatchlists,
    createWatchlist,
    addStockToWatchlist,
    findSymbols,
    loadQuote,
    loadHistory,
    loadCompany,
    refreshTradingData,
    placeOrder,
  };
}

