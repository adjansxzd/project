import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { AuthResponse, LoginRequest, RegisterRequest } from '../models/auth.model';


@Injectable({ providedIn: 'root' })
export class AuthService {
    private baseUrl = 'http://localhost:8000/api';

    constructor(private http: HttpClient) { }

    login(data: LoginRequest): Observable<AuthResponse> {
        return this.http.post<AuthResponse>(`${this.baseUrl}/login/`, data).pipe(
            tap(response => {
                this.saveToken(response.access, data.username);
            })
        );
    }

    register(data: RegisterRequest): Observable<AuthResponse> {
        return this.http.post<AuthResponse>(`${this.baseUrl}/register/`, data);
    }

    logout(): Observable<any> {
        return this.http.post(`${this.baseUrl}/logout/`, {}).pipe(
            tap(() => this.clearToken())
        );
    }

    saveToken(token: string, username: string): void {
        if (typeof window !== 'undefined' && window.localStorage) {
            localStorage.setItem('token', token);
            localStorage.setItem('username', username);
        }
    }

    clearToken(): void {
        if (typeof window !== 'undefined' && window.localStorage) {
            localStorage.removeItem('token');
            localStorage.removeItem('username');
        }
    }

    isLoggedIn(): boolean {
        if (typeof window !== 'undefined' && window.localStorage) {
            return !!localStorage.getItem('token');
        }
        return false;
    }

    getUsername(): string {
        if (typeof window !== 'undefined' && window.localStorage) {
            return localStorage.getItem('username') || '';
        }
        return '';
    }

    getToken(): string | null {
        if (typeof window !== 'undefined' && window.localStorage) {
            return localStorage.getItem('token');
        }
        return null;
    }
}