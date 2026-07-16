import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './header/header.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HeaderComponent, RouterOutlet],
  template: `
    <app-header></app-header>
    <main class="portal">
      <router-outlet></router-outlet>
    </main>
  `,
  styles: [`
    .portal {
      max-width: 1040px;
      margin: 0 auto;
      padding: 2rem 1rem;
    }
  `]
})
export class AppComponent {}
