const CACHE_NAME = 'tea-shop-cache-v1';
const urlsToCache = [
  '/main.html',
  '/about.html',
  '/checkout.html',
  '/guestcheckout.html',
  '/payment.html',
  '/dashboard.html',
  '/manager.html',
  '/orders.html',
  '/login.html',
  '/static/assets/styles.css',
  '/static/db.js',
  '/static/assets/greentea.jpeg',
  '/static/assets/blacktea.jpeg',
  '/static/assets/pepperminttea.jpeg',
  '/static/assets/chamomiletea.jpeg',
  '/static/assets/hibiscustea.jpeg',
  '/static/assets/minttea.jpeg',
  '/static/assets/chaitea.jpeg',
  '/static/assets/whitetea.jpeg',
  '/static/assets/oolongtea.jpeg',
  '/static/assets/cinnamonbuns.jpeg'
];

// Install service worker and cache everything
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Serve cached files if offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
