
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  private apiUrl = 'http://127.0.0.1:8000/api/profile/';

  constructor(private http: HttpClient) {}

  getProfile() {
    return this.http.get('http://localhost:8000/api/profile/');
  }

  updateProfile(data: any) {
    return this.http.patch('http://localhost:8000/api/profile/', data);
  }
}