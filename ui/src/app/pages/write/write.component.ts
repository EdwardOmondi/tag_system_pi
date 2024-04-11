import { Component, inject } from '@angular/core';
import { environment } from '../../environment';
import { FormGroup, FormControl, Validators, FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Data } from '../../models/data';
import { DialogComponent } from './dialog/dialog.component';
import { NetworkingService } from '../../networking.service';

@Component({
  selector: 'app-write',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, DialogComponent],
  templateUrl: './write.component.html',
  styleUrl: './write.component.scss'
})
export class WriteComponent {
  private networkingService = inject(NetworkingService);
  private ws!: WebSocket;
  private fb = inject(FormBuilder);
  data: Data | null = null

  form = this.fb.group({
    userId: ['', Validators.required],
    braceletId: ['', Validators.required],
  });

  ngOnInit() {
    this.wsInit();
  }

  private wsInit() {
    this.ws = new WebSocket(environment.wsUrl);
    this.ws.onopen = () => {
      this.networkingService.updateWsState = true;
    };
    this.ws.onmessage = (event) => {
      console.log(event.data);
    };
    this.ws.onerror = (event) => {
      this.networkingService.addError('Error connecting to the WebSocket');
      console.error(event);
    }
  }

  ngOnDestroy() {
    this.ws.close();
    this.networkingService.updateWsState = false;
  }

  submitForm() {
    const data = { operation: 'write', ...this.form.value, timestamp: new Date().getTime() };
    const body = JSON.stringify(data);
    console.log(body, 'body');
    if (!this.ws || this.ws.readyState !== this.ws.OPEN) {
      this.networkingService.addError('WebSocket is not connected');
    } else {
      this.ws.send(body);
      this.data = data as Data;
      setTimeout(() => {
        this.data = null;
        this.form.reset();
      }, environment.defaultTimeout);
    }
  }
}
