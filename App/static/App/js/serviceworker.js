/*
* Sample service woker file
*
* This uses workbox to implement some recommended strategies for making an app 'progressive'
*
* Workbox is a library that bakes in a set of best practices and removes the boilerplate every developer writes
* when working with service workers.
*
* for a description of the various strategies consult
* https://developers.google.com/web/tools/workbox/modules/workbox-strategies
*
* */

console.log('Hello from service-worker.js');
importScripts('https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js');

if (workbox) {
    console.log("Workbox is loaded.");
} else {
    console.log("Workbox didn't load");
}

workbox.setConfig({debug: true});

// This will trigger the importScripts() for workbox.strategies and its dependencies:
const {strategies} = workbox;


// Cache the Google Fonts stylesheets with a stale-while-revalidate strategy.
workbox.routing.registerRoute(
    /^https:\/\/fonts\.googleapis\.com/,
    new workbox.strategies.StaleWhileRevalidate({
        cacheName: 'google-fonts-stylesheets',
    })
);

// Cache the underlying font files with a cache-first strategy for 1 year.
workbox.routing.registerRoute(
    /^https:\/\/fonts\.gstatic\.com/,
    new workbox.strategies.CacheFirst({
        cacheName: 'google-fonts-webfonts',
        plugins: [
            new workbox.cacheableResponse.Plugin({
                statuses: [0, 200],
            }),
            new workbox.expiration.Plugin({
                maxAgeSeconds: 60 * 60 * 24 * 365,
                maxEntries: 30,
            }),
        ],
    })
);

// Cache CSS and javaScript assets with a stale-while-revalidate strategy.
workbox.routing.registerRoute(
    /\.(?:js|css)$/,
    new workbox.strategies.StaleWhileRevalidate({
        cacheName: 'static-resources',
    })
);

// Cache image files with a cache-first strategy for 30 days.
workbox.routing.registerRoute(
    /\.(?:png|gif|jpg|jpeg|webp|svg)$/,
    new workbox.strategies.CacheFirst({
        cacheName: 'images',
        plugins: [
            new workbox.expiration.Plugin({
                maxEntries: 60,
                maxAgeSeconds: 30 * 24 * 60 * 60,
            }),
        ],
    })
);

// Cache pages prefixed by '/app/' with a stale-while-revalidate strategy.
workbox.routing.registerRoute(
    new RegExp('/app/'),
    new workbox.strategies.StaleWhileRevalidate({
        cacheName: 'app-pages',
    })
);

// Cache the manifest.json with a stale-while-revalidate strategy.
workbox.routing.registerRoute(
    /manifest.json$/,
    // new RegExp('/app/'),
    new workbox.strategies.StaleWhileRevalidate({
        cacheName: 'app-pages',
    })
);

// Cache js and css from external sources with a stale-while-revalidate strategy.
// This will generally be from CDNs such as unpkg.com or tackpath.bootstrapcdn.com
// to load libraries such as Bootstrap, jQuery, LeafletJS etc.
workbox.routing.registerRoute(
    /^https:\/\/unpkg\.com/,
    new workbox.strategies.StaleWhileRevalidate({
        cacheName: 'static-resources',
    })
);

workbox.routing.registerRoute(
    /^https:\/\/stackpath\.bootstrapcdn\.com/,
    new workbox.strategies.StaleWhileRevalidate({
        cacheName: 'static-resources',
    })
);
