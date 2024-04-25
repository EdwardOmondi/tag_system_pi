import { Component, inject } from '@angular/core';
import { environment } from '../../environment';
import { DialogComponent } from './dialog/dialog.component';
import { Response } from '../../models/data';
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
      if (data.Message === 'Success') {
        this.data = data;
        setTimeout(() => {
          this.data = null;
        }, environment.defaultTimeout);
      } else {
        this.networkingService.addError('Error scanning tag. ' + data.Message);
      }
    };
    this.ws.onerror = (event) => {
      this.networkingService.addError('Reader error');
      console.error(event);
    };
    this.ws.onclose = () => {
      this.networkingService.addError('Reader disconnected');
      this.networkingService.updateWsState = false;
      setTimeout(() => {
        console.log('Reconnecting...');
        this.wsInit();
      }, environment.errorTimeout);
    };
  }

  ngOnDestroy() {
    this.ws.close();
    this.networkingService.updateWsState = false;
  }
}
