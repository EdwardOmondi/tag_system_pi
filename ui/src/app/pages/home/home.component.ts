import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NetworkingService } from '../../networking.service';
import { Response } from '../../models/data';
import { environment } from '../../environment';
import { Observable, Subject, Subscription, map, takeUntil } from 'rxjs';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent implements OnInit, OnDestroy {
  private networkingService = inject(NetworkingService);
  scannerId = '';
  intervalId: any;
  destroy$: Observable<boolean> = new Observable<any>();

  ngOnInit() {
    this.wsInit();
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
    // ws.send(JSON.stringify(body));
    ws.onopen = () => {
      this.networkingService.updateWsState = true;
      console.log('Reader connected');
    };
    ws.onmessage = (event) => {
      const data: Response = JSON.parse(event.data);
      this.networkingService.updateWsState = true;
      if (data.Result === -3) {
        this.scannerId = data.Message;
      }
    };
    ws.onerror = (event) => {
      console.error(event);
    };
    ws.onclose = () => {
      this.networkingService.addError('Reader disconnected');
      this.networkingService.updateWsState = false;
    };
  }

  ngOnDestroy() {
    console.log('Destroying home component');
    const ws: WebSocket = this.networkingService.ws;
    this.destroy$.pipe(map((value) => value === true));
    // this.destroy$.next(true);
    // this.destroy$.complete();
    this.networkingService.updateWsState = false;
  }
}
