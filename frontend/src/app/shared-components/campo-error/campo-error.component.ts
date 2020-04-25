import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-campo-error',
  templateUrl: './campo-error.component.html',
  styleUrls: ['./campo-error.component.scss']
})
export class CampoErrorComponent implements OnInit {

  @Input() mostraError: boolean;
  @Input() msgError: string;
  constructor() { }

  ngOnInit(): void {
  }

}
