import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { DialogComponent } from './success/dialog.component';
import { PiResponse, CloudResponse } from '../../models/data';
import { HttpClientModule } from '@angular/common/http';
import { PendingComponent } from './pending/pending.component';
import { NetworkingService } from '../../networking.service';
import { environment } from '../../environment';
import { take } from 'rxjs';

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
  showSuccessVideo = false;

  vidEnded() {
    this.data = null;
    this.cloudResponse = null;
    this.showSuccessVideo = false;
    this.showTempMessage = false;
  }

  ngOnInit() {
    this.networkingService.connect();
    this.networkingService.data.subscribe((response) => {
      // this.showTempMessage = false;
      // this.showSuccessVideo = false;
      const data = response as PiResponse;
      if (data === null) {
        return;
      }
      this.networkingService.updateScannerId = data.scanner_id;
      switch (data.status) {
        case 'INITIAL_CONNECTION': {
          break;
        }
        case 'INITIAL_SCAN': {
          this.showTempMessage = true;
          this.showSuccessVideo = false;
          break;
        }
        case 'TOO_SOON': {
          this.showTempMessage = false;
          this.networkingService.addError(
            `You must wait at least 5 seconds before scanning again`
          );
          break;
        }
        case 'SCAN_COMPLETE': {
          this.showTempMessage = false;
          const innerData = JSON.parse(data.response); // Parse the response string once
          const parsedData = JSON.parse(innerData) as CloudResponse; // Parse the response string
          if (parsedData.Result === 0) {
            this.showSuccessVideo = true;
            this.networkingService.addError(`${parsedData.Message}`);
          }
          if (parsedData.Result === 1) {
            this.cloudResponse = parsedData;
            this.showSuccessVideo = true;
          }
          break;
        }
        case 'DISCONNECTED': {
          this.showTempMessage = false;
          this.networkingService.addError(
            `Scanner ${data.scanner_id} has disconnected`
          );
          break;
        }
      }
    });
  }
}
