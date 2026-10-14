import { ChangeDetectionStrategy, Component, signal } from '@angular/core';

interface MenuItem {
  label: string;
  href: string;
}

@Component({
  selector: 'app-menu-bar',
  templateUrl: './menu-bar.html',
  styleUrl: './menu-bar.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MenuBar {
  protected readonly brand = 'Agora Rivas';
  protected readonly items: MenuItem[] = [
    { label: 'Home', href: '#home' },
    { label: 'About', href: '#about' },
    { label: 'Services', href: '#services' },
    { label: 'Contact', href: '#contact' },
  ];
  protected readonly menuOpen = signal(false);

  protected toggleMenu(): void {
    this.menuOpen.update((open) => !open);
  }

  protected closeMenu(): void {
    this.menuOpen.set(false);
  }
}
