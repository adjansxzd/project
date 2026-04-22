
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Movie, Genre, Review } from '../models/movie.model';

const API = 'http://localhost:8000/api';

@Injectable({ providedIn: 'root' })
export class MovieService {
  constructor(private http: HttpClient) {}

  getMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${API}/movies/`);
  }

  getMovie(id: number): Observable<Movie> {
    return this.http.get<Movie>(`${API}/movies/${id}/`);
  }

  getGenres(): Observable<Genre[]> {
    return this.http.get<Genre[]>(`${API}/genres/`);
  }

  getReviews(movieId: number): Observable<Review[]> {
    return this.http.get<Review[]>(`${API}/reviews/?movie_id=${movieId}`);
  }

  createReview(movieId: number, text: string, rating: number): Observable<Review> {
    return this.http.post<Review>(`${API}/reviews/create/`, {
      movie_id: movieId,
      text,
      rating
    });
  }
 
    deleteMovie(id: number): Observable<any> {
      return this.http.delete(`${API}/movies/${id}/`);
  }

    createMovie(formData: FormData): Observable<Movie> {
      return this.http.post<Movie>(`${API}/movies/`, formData);
  }

    updateMovie(id: number, formData: FormData): Observable<Movie> {
      return this.http.put<Movie>(`${API}/movies/${id}/`, formData);
  }
}
