// Yerdaulet's part
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MovieService } from '../../services/movie.service';
import { Movie, Genre } from '../../models/movie.model'; // Changed by Yegor
import { MovieCard } from '../../components/movie-card/movie-card';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, MovieCard], // Changed by Yegor
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {
  movies: Movie[] = [];
  filteredMovies: Movie[] = [];
  loading = true;
  searchQuery = '';
  genres: Genre[] = []; // Yegor

  constructor(
    private movieService: MovieService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadGenres(); // Yegor
    this.loadMovies(); // Yegor
  }

  loadMovies(): void { // Yegor
    this.movieService.getMovies().subscribe({
      next: (data) => {
        this.movies = data;
        this.mapGenres(); // Yegor
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

  loadGenres(): void { // Yegor
    this.movieService.getGenres().subscribe({
      next: (data) => {
        this.genres = data;
        this.mapGenres(); // Yegor
        this.filteredMovies = this.movies;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Ошибка загрузки жанров', err);
      }
    });
  }

  mapGenres(): void { // Yegor
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

  deleteMovie(id: number): void { // Yegor
    const confirmed = confirm('Удалить этот фильм?'); // Yegor
    if (!confirmed) return; // Yegor

    this.movieService.deleteMovie(id).subscribe({
      next: () => {
        this.movies = this.movies.filter(movie => movie.id !== id); // Yegor
        this.filteredMovies = this.filteredMovies.filter(movie => movie.id !== id); // Yegor
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Ошибка удаления фильма', err); // Yegor
        alert('Не удалось удалить фильм'); // Yegor
      }
    });
  }
}