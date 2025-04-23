import { Component } from '@angular/core';
import { AuthService } from '/Users/SystemX/Desktop/WebProject2025/frontend/src/app/services/auth.service';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  imports: [CommonModule, RouterModule, FormsModule]
})
export class RegisterComponent {
  username = '';
  password = '';
  error = '';

  constructor(private authService: AuthService, private router: Router) {}

  register(): void {
    this.authService.register(this.username, this.password).subscribe({
      next: () => {
        alert('Регистрация прошла успешно!');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.error = err.error?.message || 'Ошибка регистрации';
      }
    });
  }
}
