//--------Alan----------
import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { ProfileService } from '../../services/profile.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './profile.html'
})
export class ProfileComponent implements OnInit {

  profile: any = null;
  editMode = false;

  selectedFile: File | null = null;
  previewUrl: string | null = null;

  loading = false;
  error = '';

  constructor(
    private authService: AuthService,
    private router: Router,
    private profileService: ProfileService
  ) {}

  ngOnInit() {
    this.loadProfile();
  }

  loadProfile() {
    this.loading = true;
    this.profileService.getProfile().subscribe({
      next: (data) => {
        this.profile = data;

        if (this.profile?.avatar) {
          this.previewUrl = 'http://localhost:8000' + this.profile.avatar;
        }

        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.error = 'Failed to load profile';
        this.loading = false;
      }
    });
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (!file) return;

    this.selectedFile = file;

    const reader = new FileReader();
    reader.onload = () => {
      this.previewUrl = reader.result as string;
    };
    reader.readAsDataURL(file);
  }

  save() {
    if (!this.selectedFile) {
      this.error = 'Choose a file first';
      return;
    }

    const formData = new FormData();
    formData.append('avatar', this.selectedFile);

    this.loading = true;

    this.profileService.updateProfile(formData).subscribe({
      next: (res: any) => {
        this.profile = res;
        this.selectedFile = null;
        this.editMode = false;
        this.loading = false;

        if (res.avatar) {
          this.previewUrl = 'http://localhost:8000' + res.avatar;
        }
      },
      error: (err) => {
        console.error(err);
        this.error = 'Upload failed';
        this.loading = false;
      }
    });
  }

  logout() {
    this.authService.logout().subscribe(() => {
      this.router.navigate(['/login']);
    });
  }
}