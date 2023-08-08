import { TestBed } from '@angular/core/testing';

import { GiosApiService } from './gios-api.service';

describe('GiosApiService', () => {
  let service: GiosApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GiosApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
