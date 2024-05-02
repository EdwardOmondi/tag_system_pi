import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { DialogComponent } from './success/dialog.component';
import { PiResponse, CloudResponse } from '../../models/data';
import { HttpClientModule } from '@angular/common/http';
import { PendingComponent } from './pending/pending.component';
import { Observable } from 'rxjs';
import { environment } from '../../environment';
import { NetworkingService } from '../../networking.service';

@Component({
  selector: 'app-read',
  standalone: true,
  imports: [DialogComponent, HttpClientModule, PendingComponent],
  templateUrl: './read.component.html',
  styleUrl: './read.component.scss',
})
export class ReadComponent implements OnInit, OnDestroy {
  private networkingService = inject(NetworkingService);
  data: PiResponse | null = null;
  websocket = new WebSocket('ws://localhost:8765/');
  cloudResponse: CloudResponse | null = null;

  vidEnded() {
    console.log('vid ended');
    this.data = null;
    this.cloudResponse = null;
  }

  ngOnInit() {
    this.reconnect();
    // this.networkingService.wsState.subscribe((state: boolean) => {
    //   if (!state) {
    //     this.reconnect();
    //   }
    // });
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
      }
      if (this.data.status === 'SCAN_COMPLETE') {
        const validResponse = JSON.parse(this.data.response) as CloudResponse;
        console.log(validResponse.data, 'validResponse');
        if (validResponse.data !== undefined) {
          this.cloudResponse = validResponse;
        }
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
