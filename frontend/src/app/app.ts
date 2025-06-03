import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { listenerCount } from 'process';
import { PokemonListComponent } from './pokemon-list/pokemon-list';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,PokemonListComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
  standalone: true

})
export class App {
  protected title = 'frontend';
}
