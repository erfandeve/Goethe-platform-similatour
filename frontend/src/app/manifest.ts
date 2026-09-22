import type { MetadataRoute } from "next";

/** Lets phones "add to home screen" with the right name, icon and colours. */
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Lexora · لکسورا",
    short_name: "Lexora",
    description: "سیمیلیتور زبان آلمانی و آموزش A1 تا C1",
    start_url: "/fa",
    display: "standalone",
    background_color: "#050510",
    theme_color: "#050510",
    lang: "fa",
    dir: "rtl",
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
  };
}
