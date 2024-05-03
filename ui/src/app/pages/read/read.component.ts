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
export class ReadComponent implements OnInit {
  private networkingService = inject(NetworkingService);
  data: PiResponse | null = null;
  cloudResponse: CloudResponse | null = null;
  showTempMessage = false;
  showSuccessMessage = false;
  showSuccessVideo = false;

  vidEnded() {
    console.log('vid ended');
    this.data = null;
    this.cloudResponse = null;
  }

  ngOnInit() {
    this.networkingService.data.subscribe((response) => {
      this.showTempMessage = false;
      this.showSuccessMessage = false;
      this.showSuccessVideo = false;
      const data = response as PiResponse;
      if (data === null) {
        return;
      }
      this.networkingService.updateScannerId = data.scanner_id;
      switch (data.status) {
        case 'INITIAL_CONNECTION': {
          console.log('initial connection', data);
          break;
        }
        case 'INITIAL_SCAN': {
          console.log('initial scan', data);
          this.showTempMessage = true;
          break;
        }
        case 'TOO_SOON': {
          console.log('too soon', data);
          this.networkingService.addError(
            `You must wait at least 10 seconds before scanning again`
          );
          break;
        }
        case 'SCAN_COMPLETE': {
          console.log('scan complete', data);
          const validResponse = JSON.parse(data.response) as CloudResponse;
          if (validResponse.data !== undefined) {
            this.cloudResponse = validResponse;
            this.showSuccessMessage = true;
          } else {
            this.networkingService.addError(
              `No data found for bracelet ${data.bracelet_id}`
            );
          }
          break;
        }
        case 'DISCONNECTED': {
          console.log('disconnected', data);
          this.networkingService.addError(
            `Scanner ${data.scanner_id} has disconnected`
          );
          break;
        }
      }
    });
  }

  // reconnect() {
  //   console.log('reconnect');
  //   this.websocket = new WebSocket(environment.wsUrl);
  //   this.websocket.onopen = () => {
  //     this.networkingService.updateWsState = true;
  //   };
  //   this.websocket.onmessage = (value: MessageEvent<string>) => {
  //     this.networkingService.updateWsState = true;
  //     this.data = JSON.parse(value.data) as PiResponse;
  //     this.networkingService.updateScannerId = this.data.scanner_id;
  //     if (this.data.status === 'TOO_SOON') {
  //       this.networkingService.addError(
  //         `You  must wait at least 10 seconds before scanning again`
  //       );
  //     }
  //     if (this.data.status === 'SCAN_COMPLETE') {
  //       const validResponse = JSON.parse(this.data.response) as CloudResponse;
  //       console.log(validResponse.data, 'validResponse');
  //       if (validResponse.data !== undefined) {
  //         this.cloudResponse = validResponse;
  //       }
  //     }
  //   };
  //   this.websocket.onerror = (event) => {
  //     this.networkingService.addError(`Websocket error: ${event}`);
  //   };
  //   this.websocket.onclose = () => {
  //     this.networkingService.updateWsState = false;
  //     console.log(`Websocket closed`);
  //   };
  // }
}
