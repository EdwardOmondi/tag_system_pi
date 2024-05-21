import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ReadComponent } from './pages/read/read.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/read',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: 'read',
    component: ReadComponent
  },
  {
    path: '**',
    component: ReadComponent
  }
];
