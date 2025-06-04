import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EtlTrigger } from './etl-trigger';

describe('EtlTrigger', () => {
  let component: EtlTrigger;
  let fixture: ComponentFixture<EtlTrigger>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EtlTrigger]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EtlTrigger);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
