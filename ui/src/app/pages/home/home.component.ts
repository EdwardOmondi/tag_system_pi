import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Observable } from 'rxjs';
import { environment } from '../../environment';
import { NetworkingService } from '../../networking.service';
import { PiResponse, CloudResponse } from '../../models/data';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent implements OnInit, OnDestroy {
  private networkingService = inject(NetworkingService);
  data: PiResponse | null = null;
  pendingData: CloudResponse | null = null;
  websocket = new WebSocket('ws://localhost:8765/');
  cloudResponse!: CloudResponse;
  scannerId = '';

  ngOnInit() {
    this.reconnect();
    // this.networkingService.wsState.subscribe((state: boolean) => {
    //   if (!state) {
    //     this.reconnect();
    //   }
    // });
    this.networkingService.scannerId.subscribe((id: string) => {
      this.scannerId = id;
    });
  }

  reconnect() {
    console.log('reconnect');
    this.websocket = new WebSocket(environment.wsUrl);
    this.websocket.onopen = () => {
      this.networkingService.updateWsState = true;
    };
    this.websocket.onmessage = (value: MessageEvent<string>) => {
      this.networkingService.updateWsState = true;
      this.data = JSON.parse(value.data) as PiResponse;
      this.networkingService.updateScannerId = this.data.scanner_id;
      if (this.data.status === 'TOO_SOON') {
        this.networkingService.addError(
          `You  must wait at least 10 seconds before scanning again`
        );
      } else {
        this.cloudResponse = JSON.parse(this.data.response) as CloudResponse;
        console.log(this.cloudResponse);
      }
    };
    this.websocket.onerror = (event) => {
      this.networkingService.addError(`Websocket error: ${event}`);
    };
    this.websocket.onclose = () => {
      this.networkingService.updateWsState = false;
      console.log(`Websocket closed`);
    };
  }

  ngOnDestroy() {
    this.websocket.close();
  }
}
