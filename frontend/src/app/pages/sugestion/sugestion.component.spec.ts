import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SugestionComponent } from './sugestion.component';

describe('SugestionComponent', () => {
  let component: SugestionComponent;
  let fixture: ComponentFixture<SugestionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SugestionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SugestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
