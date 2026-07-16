import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil } from 'rxjs';
import { CourseCardComponent } from '../course-card/course-card.component';
import { CourseService } from '../course.service';

interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
}

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [CommonModule, FormsModule, CourseCardComponent],
  template: `
    <section class="courses">
      <div class="heading">
        <h2>Courses</h2>
        <input
          type="search"
          [(ngModel)]="searchTerm"
          placeholder="Search by course or code"
          aria-label="Search courses">
      </div>

      <div class="spinner" *ngIf="loading" role="status">Loading courses…</div>

      <div class="course-grid" *ngIf="!loading && filteredCourses.length; else emptyState">
        <app-course-card
          *ngFor="let course of filteredCourses; trackBy: trackByCourseId"
          [name]="course.name"
          [code]="course.code"
          [credits]="course.credits">
        </app-course-card>
      </div>

      <ng-template #emptyState>
        <p class="empty" *ngIf="!loading">No courses found.</p>
      </ng-template>
    </section>
  `,
  styles: [`
    .courses {
      padding: 1.25rem;
      background: #eef3ff;
      border-radius: .75rem;
    }

    .heading {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      margin-bottom: 1rem;
    }

    h2 {
      margin: 0;
    }

    input {
      min-width: 250px;
      padding: .7rem .8rem;
      border: 1px solid #9fb0ca;
      border-radius: .35rem;
    }

    .course-grid {
      display: grid;
      gap: .75rem;
    }

    .spinner,
    .empty {
      margin: 0;
      padding: 1rem;
      color: #526078;
      background: white;
      border-radius: .5rem;
    }

    .spinner::before {
      display: inline-block;
      width: .9rem;
      height: .9rem;
      margin-right: .55rem;
      vertical-align: -2px;
      content: '';
      border: 2px solid #93a8ca;
      border-top-color: #1e40af;
      border-radius: 50%;
      animation: spin .7s linear infinite;
    }

    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }

    @media (max-width: 550px) {
      .heading {
        flex-direction: column;
        align-items: stretch;
      }

      input {
        min-width: 0;
      }
    }
  `]
})
export class CourseListComponent implements OnInit, OnDestroy {
  searchTerm = '';
  loading = false;
  courses: Course[] = [];
  private readonly destroy$ = new Subject<void>();

  constructor(private readonly courseService: CourseService) {}

  ngOnInit(): void {
    this.loading = true;
    this.courseService.getCourses()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (posts) => {
          this.courses = posts.map((post) => ({
            id: post.id,
            name: post.title,
            code: `COURSE-${post.id}`,
            credits: 3,
          }));
          this.loading = false;
        },
        error: () => {
          this.loading = false;
        }
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  get filteredCourses(): Course[] {
    const query = this.searchTerm.trim().toLowerCase();
    if (!query) return this.courses;
    return this.courses.filter((course) =>
      course.name.toLowerCase().includes(query) || course.code.toLowerCase().includes(query)
    );
  }

  trackByCourseId(_index: number, course: Course): number {
    return course.id;
  }
}
