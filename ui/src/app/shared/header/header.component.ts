import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  showMobileMenu = false;

  ngOnInit() {
    // // determine window size and if mobile set showMobileMenu to true
    // const windowWidth = window.innerWidth;
    // if (windowWidth <= 768) {
    //   this.showMobileMenu = true;
    // }
    // // listen for window resize event
    // window.addEventListener('resize', () => {
    //   const windowWidth = window.innerWidth;
    //   if (windowWidth <= 768) {
    //     this.showMobileMenu = true;
    //   } else {
    //     this.showMobileMenu = false;
    //   }
    // });
  }
}
