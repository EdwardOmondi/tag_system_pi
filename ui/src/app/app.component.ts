import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './shared/header/header.component';
import { NetworkingService } from './networking.service';
import { AlertComponent } from './shared/alert/alert.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent, AlertComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'ui';
  private networkingService = inject(NetworkingService);
  errors: string[] = [];

  ngOnInit() {
    this.networkingService.errors.subscribe((error) => {
      this.errors = error;
    });
  }

}
