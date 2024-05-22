import { Injectable, inject } from '@angular/core';
import { BehaviorSubject, Observable, map } from 'rxjs';
import { environment } from './environment';
import { PiResponse, CloudResponse } from './models/data';

@Injectable({
  providedIn: 'root',
})
export class NetworkingService {
  private _wsActive = new BehaviorSubject<boolean>(false);
  private _piId = new BehaviorSubject<string>('');
  private _errors = new BehaviorSubject<string[]>([]);
  private _data = new BehaviorSubject<PiResponse | null>(null);
  private _pendingData = new BehaviorSubject<CloudResponse | null>(null);
  private _wsUrl = new BehaviorSubject<string>(environment.wsUrl);
  private _wsRetryCounter = 0;

  public set wsUrl(v: string) {
    this._wsUrl.next(v);
  }

  get data() {
    return this._data.asObservable();
  }

  set updateData(value: PiResponse | null) {
    this._data.next(value);
  }

  get pendingData() {
    return this._pendingData.asObservable();
  }

  set updatePendingData(value: CloudResponse | null) {
    this._pendingData.next(value);
  }

  get wsState() {
    return this._wsActive.asObservable();
  }
  set updateWsState(value: boolean) {
    this._wsActive.next(value);
  }

  get scannerId() {
    return this._piId.asObservable();
  }

  set updateScannerId(value: string) {
    this._piId.next(value);
  }

  get errors() {
    return this._errors.asObservable();
  }

  addError(error: string) {
    this._errors.next([...this._errors.value, error]);
    // after 5 seconds remove the error
    setTimeout(() => {
      this.removeError(this._errors.value.indexOf(error));
    }, environment.errorTimeout);
  }

  removeError(index: number) {
    const errors = this._errors.value;
    errors.splice(index, 1);
    this._errors.next(errors);
  }

  connect() {
    this._wsUrl.subscribe((url) => {
      const websocket = new WebSocket(url);
      websocket.onopen = () => {
        this.updateWsState = true;
      };
      websocket.onmessage = (value: MessageEvent<string>) => {
        if (!this._wsActive.value) {
          this.updateWsState = true;
        }
        this.updateData = JSON.parse(value.data) as PiResponse;
        this.updateScannerId = (
          JSON.parse(value.data) as PiResponse
        ).scanner_id;
      };
      websocket.onerror = (event: Event) => {
        if ('error' in event) {
        } else {
          if (this._wsActive.value === false && this._wsRetryCounter < 50) {
            this.connect();
            this._wsRetryCounter++;
          }
        }
        // this.addError(`Connection error: ${event.currentTarget}`);
        return;
      };
      websocket.onclose = () => {
        if (this._wsActive.value) {
          this.updateWsState = false;
          this.connect();
        }
      };
    });
  }
}
