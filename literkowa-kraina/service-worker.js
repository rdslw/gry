const PREFIX = "literkowa-kraina-";
const CACHE = `${PREFIX}v2`;
const FILES = ["./", "./index.html", "./manifest.webmanifest", "./icon-256.png"];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(FILES)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(names => Promise.all(
    names.filter(name => name.startsWith(PREFIX) && name !== CACHE).map(name => caches.delete(name))
  )));
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  if (event.request.method === "GET") {
    event.respondWith(caches.match(event.request).then(response => response || fetch(event.request)));
  }
});
