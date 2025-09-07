# ML Project Template

これは、機械学習モデルの学習からAPI化、デプロイまでの一連のフローを体験するためのプロジェクトテンプレートです。

## プロジェクト構成

```
project/
├── notebooks/train.ipynb   # データ前処理 & 学習 Notebook
├── app/main.py             # FastAPI アプリ
├── app/model.py            # モデル読み込み & 推論
├── app/model.pkl           # 学習済みモデル
├── requirements.txt
├── Dockerfile
├── .github/workflows/ci-cd.yml
└── README.md
```

## セットアップ & 実行

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. Kaggle APIの設定

`notebooks/train.ipynb` を実行するためには、KaggleのAPIキーが必要です。

1. Kaggleにログインし、"My Account" ページから `kaggle.json` をダウンロードします。
2. `~/.kaggle/kaggle.json` に配置します。

```bash
mkdir ~/.kaggle
mv path/to/your/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### 3. モデルの学習

MLflow UIを起動して実験をトラッキングします。

```bash
mlflow ui
```

Jupyter Notebookを起動し、`notebooks/train.ipynb` を開いて実行します。

```bash
jupyter notebook
```

### 4. APIサーバーの起動

```bash
uvicorn app.main:app --reload
```

### 5. APIのテスト

- **ヘルスチェック:** `http://127.0.0.1:8000/health`
- **推論:**
  ```bash
  curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
        "Pclass": 3,
        "Sex": "male",
        "Age": 22,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25,
        "Embarked": "S"
      }'
  ```

### 6. Dockerでの実行

```bash
# Dockerイメージのビルド
docker build -t ml-app .

# Dockerコンテナの実行
docker run -p 8000:8000 ml-app
```
