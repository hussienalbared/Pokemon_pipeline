import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { PokemonService } from '../../services/pokemon';
import { PokemonListComponent } from '../pokemon-list/pokemon-list';

@Component({
  selector: 'app-pokemon-filter',
  imports: [CommonModule, FormsModule, PokemonListComponent],
  templateUrl: './pokemon-filter.html',
  styleUrl: './pokemon-filter.css'
})
export class PokemonFilter implements OnInit {
  pokemons: Pokemon[] = [];
  filters = {
    name: '',
    type: '',
    id: ''
  };
  types: string[] = ['Fire', 'Water', 'Grass', 'Electric', 'Rock', 'Ground', 'Psychic', 'Ghost', 'Dragon'];

  constructor(private pokemonService: PokemonService) { }

  ngOnInit() {
    this.loadPokemons();
  }

  loadPokemons() {
    this.pokemonService.getPokemons(this.filters).subscribe(data => {
      this.pokemons = data;
    });
  }

  onFilterChange() {
    this.loadPokemons();
  }
}
