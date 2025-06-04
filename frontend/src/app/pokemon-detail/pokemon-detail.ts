import { AfterViewInit, ChangeDetectorRef, Component, Input, OnChanges, signal, SimpleChanges } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { switchMap } from 'rxjs';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { log } from 'console';

@Component({
  selector: 'app-pokemon-detail',
  imports: [CommonModule],
  templateUrl: './pokemon-detail.html',
  styleUrl: './pokemon-detail.css',
  standalone: true,
})
/**
 * Component responsible for displaying detailed information about a specific Pokémon.
 *
 * This class handles fetching Pokémon data from the backend API based on the route parameter,
 * manages loading and error states, and updates the view accordingly.
 *
 * @remarks
 * - Uses Angular's `HttpClient` to retrieve Pokémon data.
 * - Subscribes to route parameter changes to dynamically load the requested Pokémon.
 * - Implements `AfterViewInit` to ensure data loading occurs after the view is initialized.
 *
 * @example
 * // Usage in a template:
 * <app-pokemon-detail></app-pokemon-detail>
 *
 * @see {@link https://angular.io/guide/lifecycle-hooks}
 */
export class PokemonDetail implements AfterViewInit {
  pokemon = signal<Pokemon | null>(null);
  loading = signal(true);
  error = signal<string | null>(null);
  constructor(
    private http: HttpClient,
    private route: ActivatedRoute, private cd: ChangeDetectorRef
  ) { }

  /**
   * Lifecycle hook that is called after Angular has initialized all data-bound properties
   * of a directive. Use this method to perform component initialization, such as fetching
   * data or setting up subscriptions.
   *
   * @remarks
   * This method is part of the Angular OnInit lifecycle interface.
   *
   * @see {@link https://angular.io/api/core/OnInit}
   */
  ngOnInit() {





  }
  ngAfterViewInit() {


    this.loadPokemon();
    // Ensure change detection runs after the async operation



    // This lifecycle hook is not needed for this component, but can be used if you need to perform actions after the view is initialized.
  }

  /**
   * Loads Pokémon details based on the route parameter 'name'.
   * 
   * This method subscribes to changes in the route parameters, retrieves the Pokémon name,
   * and fetches the corresponding Pokémon data from the backend API. It updates the component's
   * state with the fetched data or sets an error message if the request fails.
   * 
   * @throws {Error} If no Pokémon name is provided in the route parameters.
   */
  loadPokemon() {
    this.route.paramMap.pipe(
      switchMap(params => {
        const name = params.get('name');
        if (!name) {
          throw new Error('No Pokémon name provided in route');
        }
        return this.http.get<Pokemon>(`http://localhost:8000/pokemon/${name.toLowerCase()}`);
      })
    ).subscribe({
      next: data => {
        console.log('Pokemon data:', data);
        this.pokemon.set(data);
        this.loading.set(false);
      },
      error: err => {
        this.error.set(err.message || 'Failed to load');
        this.loading.set(false);
      }
    });
  }
}
