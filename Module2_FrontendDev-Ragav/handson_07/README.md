# Student Portal — Angular

An Angular standalone implementation of the Student Portal component and data-binding exercise.

## Run locally

```bash
npm install
npm start
```

Open `http://localhost:4200`.

## Task coverage

- `CourseCardComponent` receives `name`, `code`, `credits`, and `grade` via `@Input()` and renders them with interpolation.
- `CourseListComponent` uses `*ngFor` with `trackBy`, property binding for each card input, and `*ngIf` for the empty state.
- The search field uses `[(ngModel)]` from `FormsModule` to filter courses by name or code.
