import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-pending',
  standalone: true,
  imports: [],
  templateUrl: './pending.component.html',
  styleUrl: './pending.component.scss'
})
export class PendingComponent {
  @Input({ required: true }) pendingMessage: string = '';
}
