//--------------------Alan---------------------------
import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class LoginComponent {
  username = '';
  password = '';
  error = '';
  loading = false;

constructor(
  private authService: AuthService,
  private router: Router,
  private cdr: ChangeDetectorRef   
) {}


  onSubmit(): void {
    if (!this.username || !this.password) {
      this.error = 'Заполните все поля';
      return;
    }
    this.loading = true;
    this.error = '';

    this.authService.login({ username: this.username, password: this.password }).subscribe({
      next: (res) => {
        console.log('LOGIN SUCCESS');
        this.loading = false;
        this.router.navigate(['/home']);
      },
      error: (err) => {
        this.loading = false;

        if (err.status === 401) {
        this.error = 'Неверный логин или пароль';
        } else {
          this.error = 'Ошибка сервера. Попробуйте позже';
        }

        this.cdr.detectChanges(); 
      }
    });
  }
}
//--------------------Alan---------------------------