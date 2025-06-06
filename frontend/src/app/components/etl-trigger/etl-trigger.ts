import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-etl-trigger',
  templateUrl: './etl-trigger.html',
  styleUrls: ['./etl-trigger.css'],
  imports: [FormsModule,CommonModule,RouterModule ],
})
export class EtlTriggerComponent {
  idsInput = '';
  loading = false;
  output: string | null = null;
  error: string | null = null;

  constructor(private http: HttpClient,private router: Router) {}

  triggerETL() {
    this.loading = true;
    this.output = null;
    this.error = null;

    const ids = this.parseIds(this.idsInput);
    if (!ids.length) {
      this.error = 'Please enter at least one valid Pokémon ID.';
      this.loading = false;
      return;
    }

    this.http.post<any>('http://localhost:8000/etl', { ids })
      .subscribe({
        next: (res) => {
          console.log('ETL response:', res);
          this.output = 'ETL triggered successfully.';
          this.loading = false;
          this.router.navigate(['/search']);
        },
        error: (err) => {
          this.error = 'ETL request failed.';
          this.loading = false;
        }
      });
  }

  parseIds(input: string): number[] {
    // Parse comma-separated input like "1, 2, 5-7"
    const parts = input.split(',').map(s => s.trim());
    const ids: number[] = [];

    for (const part of parts) {
      if (/^\d+$/.test(part)) {
        ids.push(parseInt(part, 10));
      } else if (/^\d+-\d+$/.test(part)) {
        const [start, end] = part.split('-').map(Number);
        for (let i = start; i <= end; i++) {
          ids.push(i);
        }
      }
    }

    return Array.from(new Set(ids)); // Remove duplicates
  }
}
