import { Component, Input } from '@angular/core';
import { Data } from '../../../models/data';

@Component({
  selector: 'app-dialog',
  standalone: true,
  imports: [],
  templateUrl: './dialog.component.html',
  styleUrl: './dialog.component.scss'
})
export class DialogComponent {
  @Input({ required: true }) data: Data | null = null;
}
