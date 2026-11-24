// Lets HT Dash work offline once it has been opened online (when hosted, e.g. on GitHub Pages).
// The game page itself is always fetched fresh when there's a connection, so updates show up
// the next time it's opened; the saved copy is only used offline. Pictures and other files are
// served from the device and quietly refreshed in the background.
const CACHE = "ht-dash-v2";
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => c.addAll(["./", "index.html"]))); });
self.addEventListener("activate", e => e.waitUntil(
  caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const isPage = e.request.mode === "navigate" || /\/(index\.html)?$/.test(new URL(e.request.url).pathname);
  e.respondWith(caches.open(CACHE).then(async cache => {
    const saved = await cache.match(e.request, { ignoreSearch: true });
    const fresh = fetch(e.request, { cache: "no-cache" }).then(res => {
      if (res.ok) cache.put(e.request, res.clone());
      return res;
    });
    if (isPage) return fresh.catch(() => saved || cache.match("index.html"));
    fresh.catch(() => {});
    return saved || fresh.catch(() => saved);
  }));
});
