import { Card } from "../../../app/components/Card";
import type { Order } from "../hooks/useDashboardData";
import { formatCurrency, formatDate } from "../../../utils/formatters";

type OrdersPanelProps = {
  orders: Order[];
};

export function OrdersPanel({ orders }: OrdersPanelProps): JSX.Element {
  return (
    <Card title="Order Book">
      {orders.length === 0 ? (
        <p className="muted">No orders placed yet.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Symbol</th>
              <th>Side</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Total</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>{formatDate(order.created_at)}</td>
                <td>{order.symbol}</td>
                <td>{order.side}</td>
                <td>{order.quantity}</td>
                <td>{order.price}</td>
                <td>{formatCurrency(order.total_amount)}</td>
                <td>{order.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Card>
  );
}

