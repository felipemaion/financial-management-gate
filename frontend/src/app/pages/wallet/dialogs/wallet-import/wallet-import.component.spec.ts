import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WalletImportComponent } from './wallet-import.component';

describe('WalletImportComponent', () => {
  let component: WalletImportComponent;
  let fixture: ComponentFixture<WalletImportComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WalletImportComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WalletImportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
