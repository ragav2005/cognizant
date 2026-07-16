import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-course-card',
  standalone: true,
  template: `
    <article class="course-card">
      <div>
        <p class="code">{{ code }}</p>
        <h3>{{ name }}</h3>
      </div>
      <div class="details">
        <span>{{ credits }} credits</span>
      </div>
    </article>
  `,
  styles: [`
    .course-card {
      display: flex;
      justify-content: space-between;
      gap: 1rem;
      padding: 1rem;
      background: white;
      border: 1px solid #dbe3f0;
      border-radius: .5rem;
    }

    h3,
    p {
      margin: 0;
    }

    .code {
      color: #526078;
      font-size: .85rem;
    }

    .details {
      display: grid;
      align-content: center;
      gap: .4rem;
      text-align: right;
    }
  `]
})
export class CourseCardComponent {
  @Input({ required: true }) name = '';
  @Input({ required: true }) code = '';
  @Input({ required: true }) credits = 0;
}
