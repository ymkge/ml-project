# ML Project Template

これは、機械学習モデルの学習からAPI化、デプロイまで、モダンなMLOpsのワークフローを体験するためのプロジェクトテンプレートです。

## このプロジェクトで学べること

このリポジトリは、**「データ取得 → モデル学習 → API開発 → テスト → コンテナ化 → CI/CDによる自動化」** という、モダンな機械学習システムの開発・運用に必要不可欠な技術要素が詰まった、実践的なテンプレートとなっています。

具体的には、以下の技術要素を体系的に学ぶことができます。

- **機械学習モデルの開発と実験管理**
  - `Jupyter Notebook` と `pandas`, `scikit-learn` を用いたデータ分析とモデル学習
  - `MLflow` による実験トラッキングとモデル管理
  - `Kaggle API` を利用したデータセットの取得

- **学習済みモデルを使ったAPI開発**
  - `FastAPI` と `Pydantic` を用いた高速で堅牢なAPIの構築
  - 学習済みモデルをサービングする推論ロジックの実装

- **自動テスト**
  - `Pytest` を利用したAPIのエンドポイントテスト（正常系・異常系）

- **コンテナ化**
  - `Docker` を用いたアプリケーションのコンテナ化と環境の再現

- **CI/CDパイプライン**
  - `GitHub Actions` を用いたテストとビルドの自動化

これらの技術がどのように連携して一つのシステムとして機能するのかを具体的に理解するのに役立ちます。

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
