import { Component, OnDestroy, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent implements OnInit, OnDestroy {
  scannerId = '';
  intervalId: any;
  destroy$: Observable<boolean> = new Observable<any>();
  websocket: any;

  ngOnInit() {
    console.log('init');
    this.websocket = new WebSocket('ws://192.168.1.7:8765/');
    this.websocket.onmessage = (data: string) => {
      console.log(data);
    };
  }

  ngOnDestroy() {
    this.websocket.close();
  }
}
