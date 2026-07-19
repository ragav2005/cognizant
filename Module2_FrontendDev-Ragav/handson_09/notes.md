```html
1. Flexbox `gap` property
    https://caniuse.com/?search=flexbox%20gap
    -------------------------------------------------
    Browser          |  Minimum version with full support
    -----------------|------------------------------------
    Chrome           | 84  (released Jul 2020)
    Firefox          | 63  (released Oct 2018)
    Edge (Chromium)  | 84  (same as Chrome)
    Safari           | 14.1 (released Apr 2021)
    Safari on iOS    | 14.5
    Opera            | 70
    -----------------|------------------------------------
    Result:   All target browsers (Chrome, Firefox, Edge, Safari) support `gap`
    in Flexbox without prefixes. No polyfill required.

2. CSS Grid Layout
    https://caniuse.com/?search=css%20grid
    -------------------------------------------------
    Browser          |  Minimum version with full support
    -----------------|------------------------------------
    Chrome           | 57  (Mar 2017)
    Firefox          | 52  (Mar 2017)
    Edge (Chromium)  | 16  (Oct 2018) – earlier EdgeHTML had partial support
    Safari           | 10.1 (Mar 2017)
    Safari on iOS    | 10.3
    Opera            | 44
    -----------------|------------------------------------
    Result:   Fully supported in every modern browser we target.

3. `clamp()` function (used for fluid typography / spacing)
    https://caniuse.com/?search=clamp
    -------------------------------------------------
    Browser          |  Minimum version with full support
    -----------------|------------------------------------
    Chrome           | 79  (Jan 2020)
    Firefox          | 75  (Apr 2020)
    Edge (Chromium)  | 79
    Safari           | 13.1 (Mar 2021)
    Safari on iOS    | 13.4
    Opera            | 66
    -----------------|------------------------------------
    Result:   Supported in all current browsers. If you must support
    legacy browsers (IE 11, old Edge), a small JS polyfill can be added,
    but it is not required for the supported matrix.


Overall conclusion
------------------
All three features—Flexbox `gap`, CSS Grid, and `clamp()`—are green across the
browser matrix we care about (latest Chrome, Firefox, Edge, Safari). The only
extra safety net we added is the **css‑vars‑ponyfill** (for CSS custom properties)
loaded via CDN in `index.html` for very old environments.

```
