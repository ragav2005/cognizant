import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  template: `
    <header>
      <div class="header-content">
        <div>
          <h1>Student Portal</h1>
          <p>Track your enrolled courses and grades</p>
        </div>
        <nav aria-label="Main navigation">
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: true }">Courses</a>
          <a [routerLink]="['/profile']" routerLinkActive="active">Profile</a>
        </nav>
      </div>
    </header>
  `,
  styles: [`
    header {
      background: #1e40af;
      color: white;
      padding: 1.25rem max(1rem, calc((100% - 1000px) / 2));
    }

    .header-content {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      max-width: 1000px;
      margin: 0 auto;
    }

    h1,
    p {
      margin: 0;
    }

    p {
      margin-top: .35rem;
      opacity: .85;
    }

    nav {
      display: flex;
      gap: 1rem;
    }

    a {
      color: white;
      text-decoration: none;
      opacity: .8;
    }

    a:hover,
    a.active {
      opacity: 1;
      text-decoration: underline;
    }
  `]
})
export class HeaderComponent {}
