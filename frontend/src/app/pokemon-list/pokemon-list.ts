import { AfterViewInit, Component, effect, Input, OnInit, signal, SimpleChanges } from '@angular/core';
import { PokemonService } from '../pokemon';
import { FormsModule } from '@angular/forms'; // <-- ✅ Import FormsModule
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { RouterModule } from '@angular/router';
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
    MatIconModule,
    RouterModule
  ],
  templateUrl: './pokemon-list.html',
  styleUrl: './pokemon-list.css'
})
export class PokemonListComponent implements  AfterViewInit {

  // pokemons = signal<any[]>([]);
  // search: string = '';
  // displayedColumns: string[] = ['id', 'name', 'height', 'weight'];
  // dataSource = new MatTableDataSource<any[]>();
  // constructor(private service: PokemonService) {
  //   effect(() => {
  //     this.dataSource.data = this.pokemons();
  //   });
  // }
  // ngAfterViewInit(): void {

  // }

  // ngOnInit() {
  //   this.load();
  // }

  // load() {
  //   this.service.fetchPokemon(this.search).subscribe(data => this.pokemons.set(data));

  // }

  // triggerETL() {
  //   this.service.triggerETL().subscribe(res => alert("ETL triggered!"));
  // }
   @Input() pokemons: any[] = [];

  displayedColumns: string[] = ['id', 'name', 'height', 'weight'];
  dataSource = new MatTableDataSource<any>();

  ngAfterViewInit(): void {
    this.dataSource.data = this.pokemons;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['pokemons']) {
      this.dataSource.data = this.pokemons;
    }
  }
}
