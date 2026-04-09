import { FormEvent, useMemo, useState } from "react";
import { Card } from "../../../app/components/Card";
import type { SearchResult, Watchlist } from "../hooks/useDashboardData";

type WatchlistsPanelProps = {
  watchlists: Watchlist[];
  activeWatchlistId: string | null;
  searchResults: SearchResult[];
  setActiveWatchlistId: (id: string) => void;
  createWatchlist: (title: string) => Promise<void>;
  addStockToWatchlist: (watchlistId: string, symbol: string) => Promise<void>;
  findSymbols: (query: string) => Promise<void>;
  selectSymbol: (symbol: string) => Promise<void>;
};

export function WatchlistsPanel({
  watchlists,
  activeWatchlistId,
  searchResults,
  setActiveWatchlistId,
  createWatchlist,
  addStockToWatchlist,
  findSymbols,
  selectSymbol,
}: WatchlistsPanelProps): JSX.Element {
  const [watchlistName, setWatchlistName] = useState("");
  const [stockSymbol, setStockSymbol] = useState("");

  const activeWatchlist = useMemo(
    () => watchlists.find((item) => item.id === activeWatchlistId) ?? null,
    [watchlists, activeWatchlistId],
  );

  const onCreateWatchlist = async (event: FormEvent): Promise<void> => {
    event.preventDefault();
    if (!watchlistName.trim()) return;
    await createWatchlist(watchlistName);
    setWatchlistName("");
  };

  const onAddStock = async (event: FormEvent): Promise<void> => {
    event.preventDefault();
    if (!activeWatchlistId || !stockSymbol.trim()) return;
    await addStockToWatchlist(activeWatchlistId, stockSymbol);
    setStockSymbol("");
  };

  return (
    <Card title="Watchlists">
      <form className="inline-form" onSubmit={onCreateWatchlist}>
        <input
          placeholder="New watchlist name"
          value={watchlistName}
          onChange={(event) => setWatchlistName(event.target.value)}
        />
        <button type="submit">Add</button>
      </form>

      <div className="watchlists-row">
        {watchlists.map((watchlist) => (
          <button
            key={watchlist.id}
            className={watchlist.id === activeWatchlistId ? "chip chip-active" : "chip"}
            onClick={() => setActiveWatchlistId(watchlist.id)}
          >
            {watchlist.title}
          </button>
        ))}
      </div>

      {activeWatchlist ? (
        <>
          <form className="inline-form" onSubmit={onAddStock}>
            <input
              placeholder="Add stock symbol"
              value={stockSymbol}
              onChange={async (event) => {
                const value = event.target.value.toUpperCase();
                setStockSymbol(value);
                await findSymbols(value);
              }}
            />
            <button type="submit">Add Stock</button>
          </form>

          {searchResults.length > 0 ? (
            <div className="suggestions">
              {searchResults.map((item) => (
                <button
                  key={item.symbol}
                  className="suggestion-btn"
                  onClick={() => setStockSymbol(item.symbol)}
                >
                  {item.display_name}
                </button>
              ))}
            </div>
          ) : null}

          <ul className="simple-list">
            {activeWatchlist.stocks.map((stock) => (
              <li key={stock}>
                <button type="button" className="link-button" onClick={() => selectSymbol(stock)}>
                  {stock}
                </button>
              </li>
            ))}
          </ul>
        </>
      ) : null}
    </Card>
  );
}

