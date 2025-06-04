import { Routes } from '@angular/router';
import { PokemonDetail } from './pokemon-detail/pokemon-detail';
import { App } from './app';
import { PokemonListComponent } from './pokemon-list/pokemon-list';
import { PokemonFilter } from './pokemon-filter/pokemon-filter';


export const routes: Routes = [
   { path: '', component: PokemonFilter },
  { path: 'pokemon/:name', component: PokemonDetail
  }
];