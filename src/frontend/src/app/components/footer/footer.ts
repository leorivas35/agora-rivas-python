import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.html',
  styleUrl: './footer.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Footer implements OnInit {
  private readonly http = inject(HttpClient);

  protected readonly year = new Date().getFullYear();
  protected readonly backendStatus = signal<'checking' | 'online' | 'offline'>('checking');

  ngOnInit(): void {
    this.http.get<{ status: string }>('/api/health').subscribe({
      next: () => this.backendStatus.set('online'),
      error: () => this.backendStatus.set('offline'),
    });
  }
}
