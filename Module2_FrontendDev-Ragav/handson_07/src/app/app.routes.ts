import { Routes } from '@angular/router';
import { CourseListComponent } from './course-list/course-list.component';
import { StudentProfileComponent } from './student-profile/student-profile.component';

export const routes: Routes = [
  { path: '', component: CourseListComponent, pathMatch: 'full' },
  { path: 'profile', component: StudentProfileComponent },
  { path: '**', redirectTo: '' }
];
