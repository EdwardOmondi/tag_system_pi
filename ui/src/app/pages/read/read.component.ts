import { Component, OnDestroy, OnInit } from '@angular/core';
import { DialogComponent } from './dialog/dialog.component';
import { Response } from '../../models/data';
import { HttpClientModule } from '@angular/common/http';
import { PendingComponent } from './pending/pending.component';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-read',
  standalone: true,
  imports: [DialogComponent, HttpClientModule, PendingComponent],
  templateUrl: './read.component.html',
  styleUrl: './read.component.scss',
})
export class ReadComponent implements OnInit, OnDestroy {
  data: Response | null = null;
  pendingData: Response | null = null;
  websocket = new WebSocket('ws://localhost:8765/');

  vidEnded() {
    console.log('ended');
  }

  ngOnInit() {
    console.log('init');
    this.reconnect();
  }

  reconnect() {
    console.log('reconnect');
    this.websocket = new WebSocket('ws://192.168.1.7:8765/');
    this.websocket.onmessage = (data: MessageEvent<any>) => {
      console.log(data.data);
    };
    this.websocket.onopen = () => {
      console.log('connected');
    };
  }

  ngOnDestroy() {
    this.websocket.close();
  }
}
