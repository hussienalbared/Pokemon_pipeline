import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PokemonFilter } from './pokemon-filter';

describe('PokemonFilter', () => {
  let component: PokemonFilter;
  let fixture: ComponentFixture<PokemonFilter>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PokemonFilter]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PokemonFilter);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
