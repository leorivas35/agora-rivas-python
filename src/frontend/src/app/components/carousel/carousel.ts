import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  OnInit,
  inject,
  signal,
} from '@angular/core';

interface Slide {
  title: string;
  description: string;
  color: string;
}

@Component({
  selector: 'app-carousel',
  templateUrl: './carousel.html',
  styleUrl: './carousel.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Carousel implements OnInit {
  private readonly destroyRef = inject(DestroyRef);
  private readonly intervalMs = 5000;

  protected readonly slides: Slide[] = [
    { title: 'Welcome', description: 'A Django backend with a clean architecture.', color: '#2563eb' },
    { title: 'Clean Architecture', description: 'Domain, application, infrastructure, and interfaces.', color: '#059669' },
    { title: 'Angular Frontend', description: 'A standalone Angular app with signals.', color: '#d97706' },
  ];
  protected readonly currentIndex = signal(0);

  ngOnInit(): void {
    const timer = setInterval(() => this.next(), this.intervalMs);
    this.destroyRef.onDestroy(() => clearInterval(timer));
  }

  protected next(): void {
    this.currentIndex.update((index) => (index + 1) % this.slides.length);
  }

  protected previous(): void {
    this.currentIndex.update((index) => (index - 1 + this.slides.length) % this.slides.length);
  }

  protected goTo(index: number): void {
    this.currentIndex.set(index);
  }
}
