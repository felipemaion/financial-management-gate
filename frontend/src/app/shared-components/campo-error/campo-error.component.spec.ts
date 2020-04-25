import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CampoErrorComponent } from './campo-error.component';

describe('CampoErrorComponent', () => {
  let component: CampoErrorComponent;
  let fixture: ComponentFixture<CampoErrorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CampoErrorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CampoErrorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
