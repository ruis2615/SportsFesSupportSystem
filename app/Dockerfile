FROM python:3.11

# コンテナ内の作業ディレクトリを指定（以降のカレントディレクトリ）
WORKDIR /var/www/app

# ホストのカレントディレクトリをコンテナ内のカレントディレクトリにコピー
COPY . .

RUN apt install libpq-dev -y

# ライブラリインストール
RUN pip install --no-cache-dir -r /var/www/app/config/requirements.txt
