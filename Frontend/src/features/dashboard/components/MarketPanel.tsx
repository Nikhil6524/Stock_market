import { FormEvent, useState } from "react";
import { Card } from "../../../app/components/Card";
import type { Candle, CompanyInfo, Quote } from "../hooks/useDashboardData";
import { formatDate } from "../../../utils/formatters";

type MarketPanelProps = {
  quote: Quote | null;
  history: Candle[];
  company: CompanyInfo | null;
  loadQuote: (symbol: string) => Promise<void>;
  loadHistory: (symbol: string) => Promise<void>;
  loadCompany: (symbol: string) => Promise<void>;
};

export function MarketPanel({
  quote,
  history,
  company,
  loadQuote,
  loadHistory,
  loadCompany,
}: MarketPanelProps): JSX.Element {
  const [symbol, setSymbol] = useState("AAPL");

  const onLoad = async (event: FormEvent): Promise<void> => {
    event.preventDefault();
    const ticker = symbol.toUpperCase();
    await loadQuote(ticker);
    await loadHistory(ticker);
    await loadCompany(ticker);
  };

  return (
    <Card title="Market Data">
      <form className="inline-form" onSubmit={onLoad}>
        <input
          value={symbol}
          onChange={(event) => setSymbol(event.target.value)}
          placeholder="Symbol (AAPL / INFY.NS)"
        />
        <button type="submit">Load</button>
      </form>

      {quote ? (
        <div className="block">
          <strong>{quote.symbol}</strong> {quote.price} {quote.currency}
          <p className="muted">{formatDate(quote.timestamp)}</p>
        </div>
      ) : null}

      {company ? (
        <div className="block">
          <p>
            <strong>{company.name}</strong>
          </p>
          <p className="muted">
            {company.sector} / {company.industry}
          </p>
          <p className="muted clamp">{company.description}</p>
        </div>
      ) : null}

      {history.length > 0 ? (
        <table className="table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Open</th>
              <th>High</th>
              <th>Low</th>
              <th>Close</th>
              <th>Vol</th>
            </tr>
          </thead>
          <tbody>
            {history.slice(-5).reverse().map((row) => (
              <tr key={row.date}>
                <td>{formatDate(row.date)}</td>
                <td>{row.open}</td>
                <td>{row.high}</td>
                <td>{row.low}</td>
                <td>{row.close}</td>
                <td>{row.volume}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </Card>
  );
}

