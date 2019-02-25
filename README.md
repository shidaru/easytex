# easytex
## Description
Dockerを利用したLaTeXコンパイルのためのwebアプリ。
日本語での利用を想定しています。
英語で利用する場合はcompileスクリプトを変更してください。

Web Application to compile LaTeX code with Docker.
I suppose using Japanese.
Please change compile script when using it in English.

### Browser
動作確認.

Operation confirmed.

 - Firefox65.0
 - Chromium71.0.3578.98

### Docker
 - docker: version 18.09.1
 - docker-compse: version 1.23.2

## Usage
### Server
1. git clone https://github.com/shidaru/easytex.git
2. cd easytex
3. docker-compose up -d

### Application
1. サーバのIPアドレス:5000 へアクセス
2. テンプレートをダウンロード
3. 文章を書く
4. ディレクトリをアップロード
5. "Compile!!"ボタンを押す

途中でエラーが出た場合ログファイルが表示されます。

## Author
shidaru
