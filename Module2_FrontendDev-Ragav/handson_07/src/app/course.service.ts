import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class CourseService {
  constructor(private readonly http: HttpClient) {}

  getCourses(): Observable<any[]> {
    return this.http.get<any[]>('https://jsonplaceholder.typicode.com/posts?_limit=5');
  }
}
