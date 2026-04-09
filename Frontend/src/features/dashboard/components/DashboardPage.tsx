import { MarketPanel } from "./MarketPanel";
import { OrdersPanel } from "./OrdersPanel";
import { TradePanel } from "./TradePanel";
import { WatchlistsPanel } from "./WatchlistsPanel";
import { useDashboardData } from "../hooks/useDashboardData";

export function DashboardPage(): JSX.Element {
  const dashboard = useDashboardData();
  const selectSymbol = async (symbol: string): Promise<void> => {
    const ticker = symbol.toUpperCase();
    await dashboard.loadQuote(ticker);
    await dashboard.loadHistory(ticker);
    await dashboard.loadCompany(ticker);
  };

  return (
    <div className="dashboard-grid">
      {dashboard.error ? <p className="error">{dashboard.error}</p> : null}
      {dashboard.loading ? <p className="muted">Loading...</p> : null}

      <WatchlistsPanel
        watchlists={dashboard.watchlists}
        activeWatchlistId={dashboard.activeWatchlistId}
        searchResults={dashboard.searchResults}
        setActiveWatchlistId={dashboard.setActiveWatchlistId}
        createWatchlist={dashboard.createWatchlist}
        addStockToWatchlist={dashboard.addStockToWatchlist}
        findSymbols={dashboard.findSymbols}
        selectSymbol={selectSymbol}
      />

      <MarketPanel
        quote={dashboard.quote}
        history={dashboard.history}
        company={dashboard.company}
        loadQuote={dashboard.loadQuote}
        loadHistory={dashboard.loadHistory}
        loadCompany={dashboard.loadCompany}
      />

      <TradePanel
        funds={dashboard.funds}
        portfolio={dashboard.portfolio}
        placeOrder={dashboard.placeOrder}
      />

      <OrdersPanel orders={dashboard.orders} />
    </div>
  );
}

