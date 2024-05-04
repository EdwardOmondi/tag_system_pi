import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { DialogComponent } from './success/dialog.component';
import { PiResponse, CloudResponse } from '../../models/data';
import { HttpClientModule } from '@angular/common/http';
import { PendingComponent } from './pending/pending.component';
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
          // console.log('initial scan', data);
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
          const innerData = JSON.parse(data.response); // Parse the response string once
          const parsedData = JSON.parse(innerData) as CloudResponse; // Parse the response string
          console.log(parsedData.Result, 'parsedData');
          if (parsedData.Result === 0) {
            this.networkingService.addError(`${parsedData.Message}`);
          }
          if (parsedData.Result === 1) {
            console.log(parsedData.data, 'parsedData');
            this.cloudResponse = parsedData;
            this.showSuccessMessage = true;
            this.showSuccessVideo = true;
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
}
