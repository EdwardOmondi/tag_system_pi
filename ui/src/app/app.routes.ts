import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { PageNotFoundComponent } from './pages/page-not-found/page-not-found.component';
import { DocsComponent } from './pages/docs/docs.component';
import { ReadComponent } from './pages/read/read.component';
import { WriteComponent } from './pages/write/write.component';

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
    path: 'docs',
    component: DocsComponent
  },
  {
    path: 'read',
    component: ReadComponent
  },
  {
    path: 'write',
    component: WriteComponent
  },
  {
    path: '**',
    component: PageNotFoundComponent
  }
];
