import { FormEvent, useState } from "react";
import { Card } from "../../../app/components/Card";
import type { Funds, Portfolio } from "../hooks/useDashboardData";
import { formatCurrency } from "../../../utils/formatters";

type TradePanelProps = {
  funds: Funds | null;
  portfolio: Portfolio | null;
  placeOrder: (symbol: string, side: "BUY" | "SELL", quantity: number) => Promise<void>;
};

export function TradePanel({ funds, portfolio, placeOrder }: TradePanelProps): JSX.Element {
  const [symbol, setSymbol] = useState("AAPL");
  const [side, setSide] = useState<"BUY" | "SELL">("BUY");
  const [quantity, setQuantity] = useState(1);

  const onSubmit = async (event: FormEvent): Promise<void> => {
    event.preventDefault();
    await placeOrder(symbol.toUpperCase(), side, quantity);
  };

  return (
    <Card title="Wallet & Trading">
      <div className="stats-grid">
        <div className="stat-item">
          <span>Cash</span>
          <strong>{formatCurrency(funds?.available_cash ?? 0)}</strong>
        </div>
        <div className="stat-item">
          <span>Total Value</span>
          <strong>{formatCurrency(portfolio?.total_value ?? 0)}</strong>
        </div>
      </div>

      <form className="inline-form" onSubmit={onSubmit}>
        <input
          value={symbol}
          onChange={(event) => setSymbol(event.target.value)}
          placeholder="Symbol"
        />
        <select value={side} onChange={(event) => setSide(event.target.value as "BUY" | "SELL")}>
          <option value="BUY">BUY</option>
          <option value="SELL">SELL</option>
        </select>
        <input
          type="number"
          min={1}
          value={quantity}
          onChange={(event) => setQuantity(Number(event.target.value))}
        />
        <button type="submit">Place Order</button>
      </form>

      {portfolio?.holdings?.length ? (
        <table className="table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Qty</th>
              <th>Avg</th>
              <th>Current</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {portfolio.holdings.map((item) => (
              <tr key={item.symbol}>
                <td>{item.symbol}</td>
                <td>{item.quantity}</td>
                <td>{item.average_price}</td>
                <td>{item.current_price}</td>
                <td>{formatCurrency(item.market_value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className="muted">No holdings yet. Place an order to start trading.</p>
      )}
    </Card>
  );
}

