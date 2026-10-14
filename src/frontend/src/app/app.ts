import { ChangeDetectionStrategy, Component } from '@angular/core';
import { MenuBar } from './components/menu-bar/menu-bar';
import { Carousel } from './components/carousel/carousel';
import { Footer } from './components/footer/footer';

@Component({
  selector: 'app-root',
  imports: [MenuBar, Carousel, Footer],
  templateUrl: './app.html',
  styleUrl: './app.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App {}
