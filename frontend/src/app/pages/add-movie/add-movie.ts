import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { Genre } from '../../models/movie.model';

@Component({
  selector: 'app-add-movie',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './add-movie.html',
  styleUrl: './add-movie.css'
})
export class AddMovieComponent implements OnInit {
  genres: Genre[] = [];

  newMovie = {
    title: '',
    description: '',
    year: null as number | null,
    genre: null as number | null,
  };

  selectedVideoFile: File | null = null;
  selectedPreviewFile: File | null = null;

  constructor(
    private movieService: MovieService,
    private cdr: ChangeDetectorRef,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadGenres();
  }

  loadGenres(): void {
    this.movieService.getGenres().subscribe({
      next: (data) => {
        this.genres = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Ошибка загрузки жанров', err);
      }
    });
  }

  onVideoSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedVideoFile = input.files[0];
    }
  }

  onPreviewSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedPreviewFile = input.files[0];
    }
  }

  createMovie(): void {
    if (!this.newMovie.title || !this.newMovie.description || !this.newMovie.year || !this.newMovie.genre) {
      alert('Заполни title, description, year и genre');
      return;
    }

    const formData = new FormData();
    formData.append('title', this.newMovie.title);
    formData.append('description', this.newMovie.description);
    formData.append('year', String(this.newMovie.year));
    formData.append('genre', String(this.newMovie.genre));

    if (this.selectedVideoFile) {
      formData.append('video', this.selectedVideoFile);
    }

    if (this.selectedPreviewFile) {
      formData.append('preview', this.selectedPreviewFile);
    }

    this.movieService.createMovie(formData).subscribe({
      next: () => {
        alert('Фильм успешно создан');
        this.router.navigate(['/home']);
      },
      error: (err) => {
        console.error('Ошибка создания фильма', err);
        alert('Не удалось создать фильм');
      }
    });
  }
}