import { Routes } from '@angular/router';

import { HomeComponent } from './components/home/home.component';
import { CourseDetailComponent } from './components/course-detail/course-detail.component';
import { CategoriesComponent } from './components/categories/categories.component';
import { CoursesComponent } from './components/courses/courses.component';
import { EnrollComponent } from './components/enroll/enroll.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { MyCoursesComponent } from './components/my-courses/my-courses.component';


export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },  
  { path: 'home', component: HomeComponent },           
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'courses', component: CoursesComponent },
  { path: 'courses/:id', component: CourseDetailComponent },
  { path: 'enroll/:id', component: EnrollComponent },
  { path: 'my-courses', component: MyCoursesComponent },
  { path: 'categories', component: CategoriesComponent },
  { path: 'categories/:id', component: CoursesComponent }
];