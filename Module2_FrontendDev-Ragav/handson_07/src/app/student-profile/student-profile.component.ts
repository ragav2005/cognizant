import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-student-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <section class="profile">
      <h2>Student Profile</h2>
      <p>Update your profile details below.</p>

      <form [formGroup]="profileForm" (ngSubmit)="onSubmit()" novalidate>
        <label for="name">Name</label>
        <input id="name" type="text" formControlName="name">
        <small class="error" *ngIf="name.invalid && name.touched">Name is required</small>

        <label for="email">Email</label>
        <input id="email" type="email" formControlName="email">
        <small class="error" *ngIf="email.invalid && email.touched">Enter a valid email</small>

        <label for="semester">Semester</label>
        <input id="semester" type="number" min="1" max="8" formControlName="semester">
        <small class="error" *ngIf="semester.invalid && semester.touched">
          Semester must be between 1 and 8
        </small>

        <button type="submit" [disabled]="profileForm.invalid">Save profile</button>
      </form>
    </section>
  `,
  styles: [`
    .profile {
      max-width: 560px;
      padding: 1.5rem;
      background: white;
      border: 1px solid #dbe3f0;
      border-radius: .75rem;
    }

    h2,
    p {
      margin-top: 0;
    }

    p {
      color: #526078;
    }

    form {
      display: grid;
      gap: .5rem;
    }

    label {
      margin-top: .75rem;
      font-weight: 600;
    }

    input {
      padding: .7rem .8rem;
      border: 1px solid #9fb0ca;
      border-radius: .35rem;
    }

    input.ng-touched.ng-invalid {
      border-color: #dc2626;
    }

    .error {
      color: #b91c1c;
    }

    button {
      width: fit-content;
      margin-top: 1rem;
      padding: .7rem 1rem;
      color: white;
      background: #1e40af;
      border: 0;
      border-radius: .35rem;
      cursor: pointer;
    }

    button:disabled {
      cursor: not-allowed;
      opacity: .55;
    }
  `]
})
export class StudentProfileComponent {
  readonly profileForm = new FormGroup({
    name: new FormControl('', { nonNullable: true, validators: [Validators.required] }),
    email: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.email] }),
    semester: new FormControl<number | null>(null, [Validators.required, Validators.min(1), Validators.max(8)])
  });

  get name(): FormControl<string> {
    return this.profileForm.controls.name;
  }

  get email(): FormControl<string> {
    return this.profileForm.controls.email;
  }

  get semester(): FormControl<number | null> {
    return this.profileForm.controls.semester;
  }

  onSubmit(): void {
    if (this.profileForm.invalid) {
      this.profileForm.markAllAsTouched();
      return;
    }

    console.log(this.profileForm.value);
  }
}
