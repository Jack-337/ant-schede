// Crea la cartella del sito (app installabile, offline) e la versione file singolo
import { readFileSync, writeFileSync, mkdirSync, copyFileSync, readdirSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
const HERE = dirname(fileURLToPath(import.meta.url));
process.chdir(HERE);
const VERSION = process.argv[2];
if (!VERSION) { console.error("Uso: node build-site.mjs <versione>  (es. 1.2.1)"); process.exit(1); }
const OUT = resolve(HERE, "..") + "/"; // radice del repo = sito pubblicato
const IMGS = readdirSync(OUT + "img/s").filter(f => f.endsWith(".jpg")).sort().map(f => JSON.stringify("./img/s/" + f)).join(", ");
const tpl = readFileSync("app.template.html", "utf8");
const sdk = readFileSync("fitsdk.min.js", "utf8").replace(/<\/script/gi, "<\\/script");
const logo = "data:image/png;base64," + readFileSync("logo_dark.png").toString("base64");
const cat = readFileSync("catalog-full.json", "utf8");
const html = tpl.replace("__LOGO__", () => logo).replace("__CATALOG__", () => cat).replace("/*FITSDK*/", () => sdk).replaceAll("__VERSION__", VERSION);
mkdirSync(OUT, { recursive: true });
writeFileSync(OUT + "index.html", html);
// la guida PDF si rigenera con guide/make_pdf.py e finisce già in OUT
writeFileSync(OUT + "manifest.webmanifest", JSON.stringify({
  name: "ANT · Schede allenamento", short_name: "ANT", description: "Schede di allenamento, timer e diario della home gym ANT",
  lang: "it", start_url: "./", scope: "./", display: "standalone", orientation: "portrait", background_color: "#0d0d0e", theme_color: "#000000",
  icons: [
    { src: "icons/icon-192.png", sizes: "192x192", type: "image/png" },
    { src: "icons/icon-512.png", sizes: "512x512", type: "image/png" },
    { src: "icons/icon-maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
  ],
}, null, 2));
writeFileSync(OUT + "sw.js", `// Copia offline dell'app ANT. Cambiare VERSION a ogni aggiornamento.
const VERSION = "ant-${VERSION}";
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-maskable-512.png", "./icons/apple-touch-icon.png", "./guida-ANT.pdf", ${IMGS}];
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
`);
writeFileSync(OUT + ".nojekyll", "");
writeFileSync(OUT + "README.md", `# ANT · Schede allenamento

App per creare schede di allenamento della home gym ANT, allenarsi con timer di serie e recupero, tenere un diario dei progressi ed esportare le schede sull'orologio Garmin (file .fit).

- Funziona offline una volta installata sul telefono (Aggiungi alla schermata Home).
- I dati di ognuno restano salvati solo sul proprio dispositivo.
- Versione ${VERSION}
`);
console.log("OK versione", VERSION, (html.length / 1024).toFixed(0), "KB");
