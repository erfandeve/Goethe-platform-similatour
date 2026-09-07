"use client";

import { useState } from "react";

/** There is no inbox behind the API yet, so the form composes a mailto: —
 *  honest about where the message goes instead of pretending to send it. */
export function ContactForm({
  labels,
  mailto,
}: {
  labels: {
    name: string;
    email: string;
    subject: string;
    message: string;
    send: string;
    sent: string;
  };
  mailto: string;
}) {
  const [sent, setSent] = useState(false);

  const field =
    "w-full rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3 text-white placeholder:text-mist-600 focus:border-violet-400/60 focus:outline-none";

  return (
    <form
      className="flex flex-col gap-4"
      onSubmit={(event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const subject = encodeURIComponent(String(data.get("subject") ?? ""));
        const body = encodeURIComponent(
          `${data.get("name")} <${data.get("email")}>\n\n${data.get("message")}`,
        );
        window.location.href = `mailto:${mailto}?subject=${subject}&body=${body}`;
        setSent(true);
      }}
    >
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="flex flex-col gap-2">
          <span className="text-sm text-mist-400">{labels.name}</span>
          <input name="name" required className={field} />
        </label>
        <label className="flex flex-col gap-2">
          <span className="text-sm text-mist-400">{labels.email}</span>
          <input name="email" type="email" required className={field} />
        </label>
      </div>
      <label className="flex flex-col gap-2">
        <span className="text-sm text-mist-400">{labels.subject}</span>
        <input name="subject" required className={field} />
      </label>
      <label className="flex flex-col gap-2">
        <span className="text-sm text-mist-400">{labels.message}</span>
        <textarea name="message" rows={6} required className={field} />
      </label>
      <button
        type="submit"
        className="self-start rounded-full bg-white px-6 py-3 text-sm font-semibold text-ink-950 transition hover:bg-white/90"
      >
        {labels.send}
      </button>
      {sent && <p className="text-sm text-cyan-300">{labels.sent}</p>}
    </form>
  );
}
