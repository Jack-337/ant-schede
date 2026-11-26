// Copia offline dell'app ANT. Cambiare VERSION a ogni aggiornamento.
const VERSION = "ant-1.1.0";
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-maskable-512.png", "./icons/apple-touch-icon.png", "./guida-ANT.pdf"];
self.addEventListener("install", e => { e.waitUntil(caches.open(VERSION).then(c => c.addAll(CORE.map(u => new Request(u, { cache: "reload" }))))); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION && k !== "ant-fonts").map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("message", e => { if (e.data === "skip") self.skipWaiting(); });
self.addEventListener("fetch", e => {
  const r = e.request; if (r.method !== "GET") return;
  const u = new URL(r.url);
  if (u.origin === location.origin) {
    if (r.mode === "navigate") { e.respondWith(caches.match("./index.html", { cacheName: VERSION }).then(m => m || fetch(r))); return; }
    e.respondWith(caches.match(r, { ignoreSearch: true }).then(m => m || fetch(r)));
    return;
  }
  if (u.hostname === "fonts.googleapis.com" || u.hostname === "fonts.gstatic.com") {
    e.respondWith(caches.open("ant-fonts").then(c => c.match(r).then(m => m || fetch(r).then(res => { c.put(r, res.clone()); return res; }).catch(() => m))));
  }
});
