import { TestBed } from '@angular/core/testing';

import { SidenavglobalService } from './sidenavglobal.service';

describe('SidenavglobalService', () => {
  let service: SidenavglobalService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SidenavglobalService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
