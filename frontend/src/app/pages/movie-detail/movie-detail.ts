// Yerdaulet's part
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { MovieService } from '../../services/movie.service';
import { Movie, Review } from '../../models/movie.model';

@Component({
  selector: 'app-movie-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './movie-detail.html',
  styleUrl: './movie-detail.css',
})
export class MovieDetailComponent implements OnInit {
  movie: Movie | null = null;
  reviews: Review[] = [];
  loading = true;

  reviewText = '';
  reviewRating = 5;
  reviewError = '';
  reviewLoading = false;

  constructor(
    private route: ActivatedRoute,
    private movieService: MovieService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.movieService.getMovie(id).subscribe({
      next: (data) => {
        this.movie = data;
        
        // Fetch reviews independently
        this.movieService.getReviews(id).subscribe({
            next: (reviews_data) => {
                this.reviews = reviews_data;
                this.loading = false;
                this.cdr.detectChanges();
            },
            error: () => {
                this.reviews = [];
                this.loading = false;
                this.cdr.detectChanges();
            }
        });
        
        // Fetch genres independently
        this.movieService.getGenres().subscribe({
            next: (genres) => {
                const t = typeof this.movie!.genre;
                if (t === 'number' || t === 'string') {
                    const genreObj = genres.find(g => g.id === Number(this.movie!.genre));
                    if (genreObj) {
                        this.movie!.genre = genreObj;
                        this.cdr.detectChanges();
                    }
                }
            }
        });
      },
      error: () => {
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  getAvgRating(): number {
    if (!this.reviews.length) return 0;
    const sum = this.reviews.reduce((acc, r) => acc + r.rating, 0);
    return Math.round((sum / this.reviews.length) * 10) / 10;
  }
  getGenreName(): string { // Yegor
    if (!this.movie || !this.movie.genre) return 'Без жанра'; // Yegor
    if (typeof this.movie.genre === 'object') return this.movie.genre.name; // Yegor
    return 'Жанр'; // Yegor
  } // Yegor
  submitReview(): void {
    if (!this.reviewText.trim()) {
      this.reviewError = 'Напишите текст отзыва';
      this.cdr.detectChanges();
      return;
    }
    this.reviewLoading = true;
    this.reviewError = '';
    this.cdr.detectChanges();

    this.movieService.createReview(this.movie!.id, this.reviewText, this.reviewRating).subscribe({
      next: (review) => {
        this.reviews = [...this.reviews, review];
        this.reviewText = '';
        this.reviewRating = 5;
        this.reviewLoading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.reviewError = 'Ошибка при отправке отзыва';
        this.reviewLoading = false;
        this.cdr.detectChanges();
      }
    });
  }
}
