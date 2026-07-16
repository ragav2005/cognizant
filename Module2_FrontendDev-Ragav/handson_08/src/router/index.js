import { createRouter, createWebHistory } from 'vue-router'
import CoursesView from '../views/CoursesView.vue'
import CourseDetailView from '../views/CourseDetailView.vue'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/courses',
      name: 'courses',
      component: CoursesView,
    },
    {
      path: '/courses/:id',
      name: 'course-detail',
      component: CourseDetailView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
  ],
})

router.beforeEach((to) => {
  console.log(`Navigating to: ${to.path}`)
})

export default router
