// Yerdaulet's part
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {
  username = '';
  password = '';
  error = '';
  loading = false;

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit(): void {
    if (!this.username || !this.password) {
      this.error = 'Заполните все поля';
      return;
    }
    this.loading = true;
    this.error = '';

    this.authService.register({ username: this.username, password: this.password }).subscribe({
      next: (res) => {
        this.authService.saveToken(res.access, this.username);
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.error = err.error?.username?.[0] || 'Ошибка регистрации';
        this.loading = false;
      }
    });
  }
}
