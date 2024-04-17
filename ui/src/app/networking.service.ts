import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { environment } from './environment';

@Injectable({
  providedIn: 'root'
})
export class NetworkingService {
  private _wsActive = new BehaviorSubject<boolean>(false);
  private _errors = new BehaviorSubject<string[]>([]);

  constructor() { }

  get wsState() {
    return this._wsActive.asObservable();
  }
  set updateWsState(value: boolean) {
    this._wsActive.next(value);
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
}