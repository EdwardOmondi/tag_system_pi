import {
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  ViewChild,
  inject,
} from '@angular/core';
import { environment } from '../../environment';
import { DialogComponent } from './dialog/dialog.component';
import { Response } from '../../models/data';
import { NetworkingService } from '../../networking.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { PendingComponent } from './pending/pending.component';
import { Observable, Subject, Subscription, map, takeUntil } from 'rxjs';

@Component({
  selector: 'app-read',
  standalone: true,
  imports: [DialogComponent, HttpClientModule, PendingComponent],
  templateUrl: './read.component.html',
  styleUrl: './read.component.scss',
})
export class ReadComponent implements OnInit, OnDestroy {
  private networkingService = inject(NetworkingService);
  data: Response | null = null;
  pendingData: Response | null = null;
  intervalId: any;
  destroy$: Observable<boolean> = new Observable<any>();

  vidEnded() {
    console.log('ended');
    const ws = this.networkingService.ws;
    const body: Response = {
      Result: 200,
      Message: 'Video Stopped',
      data: null,
    };
    ws.send(JSON.stringify(body));
    this.data = null;
  }

  ngOnInit() {
    this.networkingService.wsStream
      .pipe(takeUntil(this.destroy$))
      .subscribe((value: boolean) => {
        if (!value) {
          this.intervalId = setInterval(() => {
            this.wsInit();
          }, environment.errorTimeout);
        } else {
          if (this.intervalId) {
            clearInterval(this.intervalId);
          }
        }
      });
  }

  private wsInit() {
    console.log('Reader connecting home');
    const ws: WebSocket = this.networkingService.ws;
    const body: Response = {
      Result: 200,
      Message: 'Video Stopped',
      data: null,
    };
    ws.send(JSON.stringify(body));
    ws.onopen = () => {
      this.networkingService.updateWsState = true;
      console.log('Reader connected');
    };
    ws.onmessage = (event) => {
      const data: Response = JSON.parse(event.data);
      this.networkingService.updateWsState = true;
      if (data.Result === 1) {
        this.pendingData = null;
        this.data = data;
      } else if (data.Result === -1) {
        this.pendingData = data;
      } else if (data.Result === -2) {
        this.networkingService.addError(data.Message);
      } else {
        this.pendingData = null;
        this.networkingService.addError('Error scanning tag. ' + data.Message);
      }
    };
    ws.onerror = (event) => {
      this.pendingData = null;
      // this.networkingService.addError('Reader error');
      console.error(event);
    };
    ws.onclose = () => {
      this.pendingData = null;
      this.networkingService.addError('Reader disconnected');
      this.networkingService.updateWsState = false;
    };
  }

  ngOnDestroy() {
    console.log('Destroying read component');
    const ws = this.networkingService.ws;
    // ws.close();
    this.networkingService.updateWsState = false;
    this.destroy$.pipe(map((value) => value === true));
  }
}
