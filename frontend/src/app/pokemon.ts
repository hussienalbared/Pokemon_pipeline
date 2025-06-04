import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PokemonService {
  private api = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  fetchPokemon(query: string = '') {
    return this.http.get<any[]>(`${this.api}/pokemon?q=${query}`);
  }

  triggerETL() {
    return this.http.post(`${this.api}/etl`, {});
  }
  getPokemons(filters: { [key: string]: string }): Observable<Pokemon[]> {
    let apiUrl = `${this.api}/api/pokemons`;

    let params = new HttpParams();
    for (const key in filters) {
      if (filters[key]) {
        params = params.set(key, filters[key]);
      }
    }
    return this.http.get<Pokemon[]>(apiUrl, { params });
  }
}
