const WORDS = [
  "Guten Morgen",
  "Wortschatz",
  "Hörverstehen",
  "Sprechen",
  "Grammatik",
  "Prüfung",
  "Alltag",
  "Konjunktiv II",
  "Nebensatz",
  "Aussprache",
];

export function Marquee() {
  const row = [...WORDS, ...WORDS];
  return (
    <div className="relative overflow-hidden border-y border-white/8 py-5">
      <div className="animate-marquee flex w-max gap-10 whitespace-nowrap">
        {row.map((word, index) => (
          <span
            key={`${word}-${index}`}
            className="font-display flex items-center gap-10 text-sm tracking-[0.3em] text-mist-600 uppercase"
          >
            {word}
            <span className="size-1 rounded-full bg-violet-500/60" aria-hidden />
          </span>
        ))}
      </div>
      <div className="pointer-events-none absolute inset-y-0 start-0 w-24 bg-linear-to-r from-ink-950 to-transparent" />
      <div className="pointer-events-none absolute inset-y-0 end-0 w-24 bg-linear-to-l from-ink-950 to-transparent" />
    </div>
  );
}
