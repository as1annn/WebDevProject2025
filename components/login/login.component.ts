import { Component } from '@angular/core';
import { AuthService } from '/Users/SystemX/Desktop/WebProject2025/frontend/src/app/services/auth.service';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  imports:[CommonModule, RouterModule, FormsModule]
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = ''; // ✅ используется в шаблоне

  constructor(private authService: AuthService, private router: Router) {}

  onLogin(): void {
    this.authService.login(this.username, this.password).subscribe(
      response => {
        this.authService.saveTokens(response.access, response.refresh);
        this.router.navigate(['/home']);
      },
      error => {
        this.errorMessage = 'Неверный логин или пароль';
      }
    );
  }
}
