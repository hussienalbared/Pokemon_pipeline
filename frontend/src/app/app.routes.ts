import { Routes } from '@angular/router';
import { PokemonDetail } from './components/pokemon-detail/pokemon-detail';
import { App } from './app';
import { PokemonListComponent } from './components/pokemon-list/pokemon-list';
import { PokemonFilter } from './components/pokemon-filter/pokemon-filter';
import { Home } from './components/home/home';


export const routes: Routes = [
   { path: '', component: Home },
   { path: 'search', component: PokemonFilter },
  {
    path: 'pokemon/:name', component: PokemonDetail
  },
  { path: 'trigger-etl', loadComponent: () => import('./components/etl-trigger/etl-trigger').then(m => m.EtlTriggerComponent) },
];