// WONTA Keyboard Service Worker — 오프라인 지원
const CACHE = 'wonta-v1';
const ASSETS = [
  '/demo/index.html',
  '/data/cangjie5.json',
  '/data/math_codes.json',
  '/data/chem_codes.json',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
