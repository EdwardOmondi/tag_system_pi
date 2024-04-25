import { Component, inject } from '@angular/core';
import { environment } from '../../environment';
import { DialogComponent } from './dialog/dialog.component';
import { Response } from '../../models/data';
import { NetworkingService } from '../../networking.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { PendingComponent } from './pending/pending.component';

@Component({
  selector: 'app-read',
  standalone: true,
  imports: [DialogComponent, HttpClientModule, PendingComponent],
  templateUrl: './read.component.html',
  styleUrl: './read.component.scss',
})
export class ReadComponent {
  private networkingService = inject(NetworkingService);
  private http = inject(HttpClient);
  private ws!: WebSocket;
  data: Response | null = null;
  pendingData: Response | null = null;

  ngOnInit() {
    this.wsInit();
  }

  private wsInit() {
    // this.ws = new WebSocket(environment.wsUrl);
    this.ws = new WebSocket('ws://192.168.1.15:8765');
    console.log(this.ws.url, 'ws url');
    this.ws.onopen = () => {
      this.networkingService.updateWsState = true;
      console.log('Reader connected');
    };
    this.ws.onmessage = async (event) => {
      const data: Response = JSON.parse(event.data);
      console.log(data, 'data');
      if (data.Result === 1) {
        this.pendingData = null;
        this.data = data;
        setTimeout(() => {
          this.data = null;
        }, environment.defaultTimeout);
      } else if (data.Result === -1) {
        this.pendingData = data;
      } else if (data.Result === -2) {
        this.networkingService.addError(data.Message);
      } else {
        this.pendingData = null;
        this.networkingService.addError('Error scanning tag. ' + data.Message);
      }
    };
    this.ws.onerror = (event) => {
      this.pendingData = null;
      this.networkingService.addError('Reader error');
      console.error(event);
    };
    this.ws.onclose = () => {
      this.pendingData = null;
      this.networkingService.addError('Reader disconnected');
      this.networkingService.updateWsState = false;
      setTimeout(() => {
        console.log('Reconnecting...');
        this.wsInit();
      }, environment.errorTimeout * 2);
    };
  }

  ngOnDestroy() {
    this.ws.close();
    this.networkingService.updateWsState = false;
  }
}
