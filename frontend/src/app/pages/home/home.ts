// Yerdaulet's part
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MovieService } from '../../services/movie.service';
import { Movie, Genre } from '../../models/movie.model'; 
import { MovieCard } from '../../components/movie-card/movie-card';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, MovieCard], 
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {
  movies: Movie[] = [];
  filteredMovies: Movie[] = [];
  loading = true;
  searchQuery = '';
  genres: Genre[] = [];

  constructor(
    private movieService: MovieService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadGenres();
    this.loadMovies();
  }

  loadMovies(): void {
    this.movieService.getMovies().subscribe({
      next: (data) => {
        this.movies = data;
        this.mapGenres();
        this.filteredMovies = this.movies;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Ошибка загрузки фильмов', err);
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  loadGenres(): void {
    this.movieService.getGenres().subscribe({
      next: (data) => {
        this.genres = data;
        this.mapGenres();
        this.filteredMovies = this.movies;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Ошибка загрузки жанров', err);
      }
    });
  }

  mapGenres(): void {
    if (!this.movies.length || !this.genres.length) return;

    const genreMap = new Map(this.genres.map(g => [g.id, g]));

    this.movies = this.movies.map(movie => {
      if (typeof movie.genre === 'number') {
        return {
          ...movie,
          genre: genreMap.get(movie.genre) ?? movie.genre
        };
      }
      return movie;
    });
  }

  onSearch(query: string): void {
    this.searchQuery = query;
    this.filteredMovies = this.movies.filter(m =>
      m.title.toLowerCase().includes(query.toLowerCase())
    );
    this.cdr.detectChanges();
  }

  deleteMovie(id: number): void {
    const confirmed = confirm('Удалить этот фильм?');
    if (!confirmed) return;

    this.movieService.deleteMovie(id).subscribe({
      next: () => {
        this.movies = this.movies.filter(movie => movie.id !== id);
        this.filteredMovies = this.filteredMovies.filter(movie => movie.id !== id);
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Ошибка удаления фильма', err);
        alert('Не удалось удалить фильм');
      }
    });
  }
}