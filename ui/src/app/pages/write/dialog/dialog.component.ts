import { Component, Input } from '@angular/core';
import { Data } from '../../../models/data';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dialog',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dialog.component.html',
  styleUrl: './dialog.component.scss'
})
export class DialogComponent {
  @Input({ required: true }) data: Data | null = null;
}
