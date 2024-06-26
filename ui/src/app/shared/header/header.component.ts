import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NetworkingService } from '../../networking.service';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  private networkingService = inject(NetworkingService);
  showMobileMenu = false;
  serverActive = false;
  showHeaderLinks = false;
  $end = new Subject();
  scannerId = '';

  ngOnInit() {
    this.networkingService.wsState.pipe(takeUntil(this.$end)).subscribe((state) => {
      this.serverActive = state;
    });
    this.networkingService.scannerId.subscribe((id: string) => {
      this.scannerId = id;
    });
  }

  ngOnDestroy() {
    this.$end.next(true);
    this.$end.complete();
  }
}
