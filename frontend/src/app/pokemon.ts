import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

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
}
