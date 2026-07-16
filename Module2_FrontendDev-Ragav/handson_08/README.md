# Student Portal — Vue 3

A Vue 3 Composition API implementation of the Student Portal exercise.

## Run locally

```bash
npm install
npm run dev
```

## Task coverage

- `CourseCard.vue` uses `defineProps` for course details.
- `CoursesView.vue` uses `ref`, `onMounted`, and `computed` for reactive data and search filtering.
- Course cards render with `v-for`, a stable `:key`, and shorthand prop bindings.
- Vue Router and Pinia are configured in the application bootstrap.
