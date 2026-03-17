
## 2024-05-19 - Cloudflare Worker Memory Allocation Overhead
**Learning:** In Cloudflare Workers (like `public/_worker.js`), dynamic arrays defined within the `fetch` handler (e.g. `['.html', '/index.html']` or `path.split('.')`) allocate memory on *every* request. This incurs unnecessary garbage collection overhead and significantly slows down the worker response time for highly concurrent routes.
**Action:** Always move static arrays, mappings, and configuration objects outside the `fetch` handler to the module scope. Replace memory-allocating operations like `split()` with non-allocating operations like `lastIndexOf` and `indexOf` combined with `slice` when parsing paths. Use `Set` instead of arrays for `O(1)` lookups.
