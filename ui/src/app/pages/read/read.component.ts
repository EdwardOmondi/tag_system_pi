import { Component, inject } from '@angular/core';
import { environment } from '../../environment';
import { DialogComponent } from './dialog/dialog.component';
import { Data, Response } from '../../models/data';
import { NetworkingService } from '../../networking.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-read',
  standalone: true,
  imports: [DialogComponent, HttpClientModule],
  templateUrl: './read.component.html',
  styleUrl: './read.component.scss',
})
export class ReadComponent {
  private networkingService = inject(NetworkingService);
  private http = inject(HttpClient);
  private ws!: WebSocket;
  data: Response | null = null;

  ngOnInit() {
    this.wsInit();
  }

  private wsInit() {
    this.ws = new WebSocket(environment.wsUrl);
    this.ws.onopen = () => {
      this.networkingService.updateWsState = true;
    };
    this.ws.onmessage = (event) => {
      const data: Data = JSON.parse(event.data);
      if (data.scannerId !== undefined) {
        const formData = new FormData();
        formData.append('bracelet_id', data.braceletId);
        formData.append('scanner_id', data.scannerId);
        this.http
          .post<Response>(environment.braceletApi, formData, {
            observe: 'response',
          })
          .subscribe((response) => {
            if (response.ok) {
              this.data = response.body;
              setTimeout(() => {
                this.data = null;
              }, environment.defaultTimeout);
            } else {
              this.networkingService.addError('Error getting data');
            }
          });
      }
    };
    this.ws.onerror = (event) => {
      this.networkingService.addError('Error connecting to the WebSocket');
      console.error(event);
    };
  }

  ngOnDestroy() {
    this.ws.close();
    this.networkingService.updateWsState = false;
  }
}
