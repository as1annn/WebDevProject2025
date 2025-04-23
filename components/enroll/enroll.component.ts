import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CourseService } from '/Users/SystemX/Desktop/WebProject2025/frontend/src/app/services/course.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-enroll',
  templateUrl: './enroll.component.html',
  styleUrls: ['./enroll.component.css'],
  imports: [CommonModule, RouterModule]
})
export class EnrollComponent implements OnInit {
  courseId: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private courseService: CourseService
  ) {}

  ngOnInit(): void {
    this.courseId = this.route.snapshot.paramMap.get('id');

    if (this.courseId) {
      this.courseService.enrollInCourse(Number(this.courseId)).subscribe(
        (response) => {
          console.log('Успешно записан на курс:', response);
        },
        (error) => {
          console.error('Ошибка при записи на курс:', error);
        }
      );
    }
  }
}
