import type { ReactNode } from "react";

export function Empty({
  title,
  body,
  action,
  icon = "✳",
}: {
  title: string;
  body?: string;
  action?: ReactNode;
  icon?: string;
}) {
  return (
    <div className="glass flex flex-col items-center rounded-3xl px-8 py-16 text-center">
      <div className="mb-5 flex size-14 items-center justify-center rounded-2xl bg-violet-500/12 text-2xl text-violet-400">
        {icon}
      </div>
      <h3 className="font-display text-xl font-semibold">{title}</h3>
      {body ? <p className="text-muted mt-2 max-w-sm text-sm">{body}</p> : null}
      {action ? <div className="mt-6">{action}</div> : null}
    </div>
  );
}
