import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SuportComponent } from './suport.component';

describe('SuportComponent', () => {
  let component: SuportComponent;
  let fixture: ComponentFixture<SuportComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SuportComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SuportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
