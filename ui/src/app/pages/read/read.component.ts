import { Component, inject } from '@angular/core';
import { environment } from '../../environment';
import { DialogComponent } from './dialog/dialog.component';
import { Data } from '../../models/data';
import { NetworkingService } from '../../networking.service';

@Component({
  selector: 'app-read',
  standalone: true,
  imports: [DialogComponent],
  templateUrl: './read.component.html',
  styleUrl: './read.component.scss'
})
export class ReadComponent {
  private networkingService = inject(NetworkingService);
  private ws!: WebSocket;
  data: Data | null = null
  ngOnInit() {
    this.wsInit();
  }

  private wsInit() {
    this.ws = new WebSocket(environment.wsUrl);
    this.ws.onopen = () => {
      this.networkingService.updateWsState = true;
    };
    this.ws.onmessage = (event) => {
      this.data = JSON.parse(event.data);
      setTimeout(() => {
        this.data = null;
      }, environment.defaultTimeout);
    };
    this.ws.onerror = (event) => {
      this.networkingService.addError('Error connecting to the WebSocket');
      console.error(event);
    }
  }

  ngOnDestroy() {
    this.ws.close();
    this.networkingService.updateWsState = false;
  }
}
