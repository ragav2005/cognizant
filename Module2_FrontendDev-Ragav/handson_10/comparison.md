# Framework Comparison – React (Redux Toolkit) vs Angular (NgRx) vs Vue (Pinia)

| Aspect | React + Redux Toolkit | Angular + NgRx | Vue + Pinia |
|--------|----------------------|----------------|-------------|
| **State container** | Single immutable store, reducers + middleware | Single immutable store, reducers + effects | Modular stores, each a composable function (Composition API) |
| **Async handling** | `createAsyncThunk` – auto‑generates `pending/fulfilled/rejected` actions | `@ngrx/effects` – separate effect classes listening to actions | `actions` inside store can be `async`; Pinia also ships `useStore` hooks for composables |
| **Boilerplate** | Low – `createSlice` + `createAsyncThunk` | Higher – actions, reducers, effects, selectors each in own file | Very low – `defineStore` with `state`, `getters`, `actions` in one place |
| **TypeScript support** | Excellent (RTK ships types) | First‑class (NgRx built for TS) | First‑class (Pinia typed via generics) |
| **DevTools** | Redux DevTools (time‑travel) | NgRx DevTools (time‑travel) | Pinia DevTools (Vue DevTools integration) |
| **Modularity / Code‑splitting** | Manual – split reducers / slices | Feature modules + lazy‑loaded effects | Built‑in – each store is its own module, auto‑code‑splits with Vite/webpack |
| **Learning curve** | Medium – Redux concepts + RTK shortcuts | Steeper – RxJS, Effects, facades | Low – looks like a composable, familiar Vue API |
| **Performance** | Immutable updates, memoised selectors | Immutable, memoised selectors via `createSelector` | Reactive proxies, automatic dependency tracking |
| **Community / Ecosystem** | Very large, many middleware | Large, Angular‑centric | Growing fast, official Vue recommendation |

### When to pick which?
* **React + Redux Toolkit** – If the team already uses React and wants a battle‑tested, highly‑typed state solution with great DevTools.
* **Angular + NgRx** – When you are in an Angular codebase and need RxJS‑based side‑effects, strong typing, and integration with Angular DI.
* **Vue + Pinia** – For Vue 3 projects; Pinia is the official store, requires the least boilerplate and works seamlessly with the Composition API and Vue DevTools.

All three follow the **centralised store** pattern, enforce **unidirectional data flow**, and provide **standardised async APIs** (thunks, effects, async actions) so that components stay thin and only dispatch / select.