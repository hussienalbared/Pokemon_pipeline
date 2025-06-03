import { Component, OnInit } from '@angular/core';
import { PokemonService } from '../pokemon';
import { FormsModule } from '@angular/forms'; // <-- ✅ Import FormsModule
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
@Component({
  selector: 'app-pokemon-list',
  standalone: true,
  imports: [FormsModule, CommonModule,
    CommonModule,
    FormsModule,
    MatTableModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    MatIconModule
  ],
  templateUrl: './pokemon-list.html',
  styleUrl: './pokemon-list.css'
})
export class PokemonListComponent implements OnInit {
  pokemons: any[] = [];
  search: string = '';
  displayedColumns: string[] = ['id', 'name', 'height', 'weight'];

  constructor(private service: PokemonService) { }

  ngOnInit() {
    this.load();
  }

  load() {
    this.service.fetchPokemon(this.search).subscribe(data => this.pokemons = data);
  }

  triggerETL() {
    this.service.triggerETL().subscribe(res => alert("ETL triggered!"));
  }
}
interface Pokemon {
  id: number;
  name: string;
  height: number;
  weight: number;
  types: string[];
  abilities: string[];
  stats: { name: string; value: number }[];
  spriteUrl: string;
}