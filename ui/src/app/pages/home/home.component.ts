import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Observable } from 'rxjs';
import { environment } from '../../environment';
import { NetworkingService } from '../../networking.service';
import { PiResponse, CloudResponse } from '../../models/data';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterModule, ReactiveFormsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent implements OnInit {
  private networkingService = inject(NetworkingService);
  cloudResponse!: CloudResponse;
  scannerId = '';
  scannerUrl = new FormControl('');
  showInput = false;
  showConnecting = false;
  ngOnInit() {
    this.networkingService.wsState.subscribe((state: boolean) => {
      this.showInput = !state;
      this.showConnecting = false;
    });

    this.networkingService.scannerId.subscribe((id: string) => {
      this.scannerId = id;
      this.showConnecting = false;
    });
    this.networkingService.connect();
    this.networkingService.errors.subscribe((errors: string[]) => {
      this.showConnecting = false;
    });
  }

  connectScanner() {
    console.log('connectScanner', this.scannerUrl.value);
    this.networkingService.wsUrl = this.scannerUrl.value as string;
    this.showConnecting = true;
  }
}
