import { Component, inject } from '@angular/core';
import { environment } from '../../environment';
import { DialogComponent } from './dialog/dialog.component';
import { Data } from '../../models/data';
import { NetworkingService } from '../../networking.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-read',
  standalone: true,
  imports: [DialogComponent],
  templateUrl: './read.component.html',
  styleUrl: './read.component.scss',
})
export class ReadComponent {
  private networkingService = inject(NetworkingService);
  private http = inject(HttpClient);
  private ws!: WebSocket;
  data: Data | null = null;

  ngOnInit() {
    this.wsInit();
  }

  private wsInit() {
    this.ws = new WebSocket(environment.wsUrl);
    this.ws.onopen = () => {
      this.networkingService.updateWsState = true;
    };
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.userId !== undefined) {
        this.http
          .post<any>(environment.braceletApi, this.data)
          .subscribe((response) => {
            this.data = response;
            setTimeout(() => {
              this.data = null;
            }, environment.defaultTimeout);
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
