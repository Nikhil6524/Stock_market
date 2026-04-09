import type { PropsWithChildren } from "react";

type CardProps = PropsWithChildren<{
  title: string;
  rightSlot?: JSX.Element;
}>;

export function Card({ title, rightSlot, children }: CardProps): JSX.Element {
  return (
    <section className="card">
      <div className="card-header">
        <h3>{title}</h3>
        {rightSlot}
      </div>
      {children}
    </section>
  );
}

