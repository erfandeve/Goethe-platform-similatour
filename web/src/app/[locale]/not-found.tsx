import Link from "next/link";

export default function NotFound() {
  return (
    <div className="container-page flex min-h-[60vh] flex-col items-center justify-center text-center">
      <p className="font-display text-8xl font-semibold text-gradient">404</p>
      <h1 className="mt-4 font-display text-2xl font-semibold">Seite nicht gefunden</h1>
      <p className="text-muted mt-2 max-w-md text-sm">
        Diese Seite wurde verschoben oder hat nie existiert. · This page has moved or never
        existed. · این صفحه پیدا نشد.
      </p>
      <Link
        href="/"
        className="mt-8 rounded-full bg-linear-to-r from-violet-500 to-cyan-400 px-6 py-3 text-sm font-semibold text-ink-950"
      >
        Start · Home · خانه
      </Link>
    </div>
  );
}
