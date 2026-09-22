import type { NextConfig } from "next";

/** Sent with every page. Microphone stays allowed: the speaking lessons record answers. */
const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "X-Frame-Options", value: "SAMEORIGIN" },
  { key: "Permissions-Policy", value: "camera=(), geolocation=(), microphone=(self)" },
  // Browsers ignore this over plain http, so it is harmless in development.
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains" },
];

const longCache = [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }];
const dayCache = [{ key: "Cache-Control", value: "public, max-age=86400, stale-while-revalidate=604800" }];

const nextConfig: NextConfig = {
  // A self-contained server in .next/standalone, so a VPS needs only `node server.js`.
  output: "standalone",
  poweredByHeader: false,
  // Next streams <title>, description and canonical into the body when they
  // resolve late, trusting crawlers to run JavaScript. Not every crawler or
  // link-preview bot does, so anything that looks like one waits for the
  // full <head>. People still get the streamed, faster page.
  htmlLimitedBots:
    /bot|crawl|spider|slurp|google|bing|yandex|duckduck|baidu|seznam|facebook|twitter|telegram|whatsapp|linkedin|skype|discord|slack|pinterest|embedly|preview|lighthouse|pagespeed|screaming frog|ahrefs|semrush/i,
  compress: true,
  async headers() {
    return [
      { source: "/:path*", headers: securityHeaders },
      // Uploaded and shipped media never change under the same name.
      { source: "/media/:path*", headers: longCache },
      { source: "/:file(og-fa|og-de|og-en).jpg", headers: dayCache },
      { source: "/:file(icon-192|icon-512).png", headers: dayCache },
    ];
  },
};

export default nextConfig;
