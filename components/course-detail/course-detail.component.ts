import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { CourseService } from '/Users/SystemX/Desktop/WebProject2025/frontend/src/app/services/course.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-course-detail',
  templateUrl: './course-detail.component.html',
  styleUrls: ['./course-detail.component.css'],
  imports:[CommonModule, RouterModule]
})
export class CourseDetailComponent implements OnInit {
  course: any;

  constructor(
    private route: ActivatedRoute,
    private courseService: CourseService
  ) {}

  ngOnInit(): void {
    const courseId = this.route.snapshot.paramMap.get('id');
    
    if (courseId) {
      const courseIdNumber = Number(courseId);
      this.courseService.getCourse(courseIdNumber).subscribe(course => {
        this.course = course;
      });
    }
  }

enroll() {
  alert('Вы успешно записались на курс!');
}
}