import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  private apiUrl = 'http://localhost:5000/api/data';  // Flask APIのURL

  constructor(private http: HttpClient) { }

  // データ取得
  getData(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }

  // データ送信
  postData(message: string): Observable<any> {
    return this.http.post<any>(this.apiUrl, { message });
  }
}
