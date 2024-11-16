import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';  // ngModelを使うためのモジュール
import { HttpClientModule } from '@angular/common/http';  // HttpClientModule をインポート

@Component({
  selector: 'app-root',
  template: `
    <h1>{{ message }}</h1>
    <input [(ngModel)]="newMessage" placeholder="Enter a new message" />
    <button (click)="sendMessage()">Send Messag</button>
    <button (click)="tallyData()">Tally Data</button>
    <h1>{{ data }}</h1>
  `,
  standalone: true,  // スタンドアロンコンポーネントとして定義
  imports: [HttpClientModule, FormsModule]  // HttpClientModule と FormsModule をインポート
})
export class AppComponent {
  message: string = '';   // Flaskからのメッセージを格納
  newMessage: string = ''; // 新しいメッセージ
  data: any;   // Flaskからのメッセージを格納

  constructor(private http: HttpClient) { }

  // Flask APIからデータを取得
  getData(): void {
    this.http.get<{ message: string }>('http://localhost:5001/api/data').subscribe(data => {
      this.message = data.message;
    });
  }

  // Flask APIにデータを送信
  sendMessage(): void {
    const body = { message: this.newMessage };

    this.http.post<{ status: string; data: { message: string } }>(
      'http://localhost:5001/api/data', body
    ).subscribe(response => {
      this.message = response.data.message;
      this.newMessage = ''; // 入力欄をクリア
    });
  }
  // Flask APIにデータを送信
  tallyData(): void {
    this.http.get<{ data: any }>('http://localhost:5001/api/tallyData').subscribe(response => {
      this.data = JSON.stringify(response);
    });
  }
  
  // 初期化時にデータを取得
  ngOnInit(): void {
    this.getData();
  }
}
