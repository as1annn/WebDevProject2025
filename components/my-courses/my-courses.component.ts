import { Component, OnInit } from '@angular/core';
import { CourseService } from '/Users/SystemX/Desktop/WebProject2025/frontend/src/app/services/course.service';
import { AuthService } from '/Users/SystemX/Desktop/WebProject2025/frontend/src/app/services/auth.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-my-courses',
  templateUrl: './my-courses.component.html',
  styleUrls: ['./my-courses.component.css'],
  imports:[CommonModule, RouterModule]
})
export class MyCoursesComponent implements OnInit {
  myCourses: any[] = [];

  constructor(
    private courseService: CourseService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.courseService.getMyCourses().subscribe(courses => {
      this.myCourses = courses;
    });
  }
}

