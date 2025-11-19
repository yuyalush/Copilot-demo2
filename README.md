# 東京の天気と時刻 CLI

東京の現地時刻（JST）と公開天気APIから取得した最新の気象条件を表示する軽量なPythonコマンドラインインターフェース（CLI）ツールです。

---
## 機能
- 東京の現在時刻（JST）を表示
- 天気API（例：OpenWeatherMap）経由で現在の天気（気温、状態、湿度など）を取得
- クリーンで人間が読みやすいデフォルト出力
- JSON出力モード（予定）
- 適切なエラーハンドリング（ネットワーク/API/環境変数の問題）
- `pytest`によるテスト
- 拡張可能なモジュール設計（`weather.py`、`time_utils.py`、`cli.py`など）

---
## 必要要件
- Python: >= 3.10（推奨）
- 依存関係:
  - `requests`
  - `python-dotenv`（オプション、ローカル開発の利便性のため）
  - `pytest`（開発/テスト用）

依存関係のインストール（仮想環境作成後）:
```bash
pip install -r requirements.txt
```
（`requirements.txt`がまだ存在しない場合は、将来のコミットで追加されます。）

---
## インストールとセットアップ

### ステップ1: リポジトリのクローン
```bash
git clone https://github.com/yuyalush/Copilot-demo2.git
cd Copilot-demo2
```

### ステップ2: 仮想環境のセットアップ
**推奨: venv（組み込み）を使用**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# Windowsの場合:
# .venv\Scripts\activate
```

**代替方法: Poetryを使用**
```bash
poetry shell
```

### ステップ3: 依存関係のインストール
**pipを使用（推奨）:**
```bash
pip install -r requirements.txt
```

**Poetryを使用:**
```bash
poetry install
```

> **注意:** `requirements.txt`がまだ存在しない場合は、将来のコミットで追加されます。

---
## 環境変数
このツールは天気プロバイダーのAPIキーが必要です。CLIを実行する前に設定してください。

| 変数 | 説明 | 例 |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap（または選択したプロバイダー）のAPIキー | `export OPENWEATHER_API_KEY=your_key_here` |

### 環境変数の設定

**方法1: 直接エクスポート（一時的）**
```bash
export OPENWEATHER_API_KEY=your_actual_api_key_here
```

**方法2: .envファイルを使用（開発時推奨）**

1. サンプルファイルをコピーして`.env`ファイルを作成:
```bash
cp .env.example .env
```

2. `.env`ファイルを編集して実際のAPIキーを追加:
```bash
# エディタで.envを開き、'your_api_key_here'を実際のキーに置き換える
# または次のコマンドを使用:
echo "OPENWEATHER_API_KEY=your_actual_api_key_here" > .env
```

3. `.env`ファイルが存在する場合、CLIは`python-dotenv`経由で自動的に読み込みます。

**重要な注意事項:**
- `.env`ファイルをバージョン管理にコミットしないでください（既に`.gitignore`に含まれています）
- APIキーは[OpenWeatherMap](https://openweathermap.org/api)から取得してください
- キーが設定されていない場合、CLIは明確なエラーメッセージを表示し、ゼロ以外のステータスで終了します

---
## 使用方法
インストールと環境変数の設定後:
```bash
python -m tokyoweather
```
またはエントリーポイントスクリプト`tokyoweather`が提供されている場合（予定）:
```bash
tokyoweather
```
### 出力例
```
Tokyo Time: 2025-11-19 15:42:07 JST
Weather: Clear sky
Temperature: 18.2 °C
Humidity: 55 %
Wind: 3.4 m/s
```

### （予定）オプション
| フラグ | 説明 |
|------|-------------|
| `--json` | APIからの生のJSONと派生した時刻情報を出力 |
| `--units metric|imperial` | 単位を上書き（デフォルト: metric） |
| `--raw` | フォーマットされていないAPIペイロードを表示 |

（これらのフラグは段階的に追加されます。初期MVPはこれらなしで開始する可能性があります。）

### エラーハンドリングの例
- APIキーが設定されていない → 表示: `ERROR: OPENWEATHER_API_KEY not set.`
- ネットワークの問題 → 表示: `ERROR: Failed to reach weather service (details...)`
- 無効なレスポンス → 表示: `ERROR: Unexpected API response format.`

終了コード:
- `0` 成功
- `1` 設定エラー（例: APIキーの欠落）
- `2` ネットワーク/APIの失敗

---
## プロジェクト構造（予定）
```
Copilot-demo2/
├── tokyoweather/
│   ├── __init__.py
│   ├── cli.py              # 引数解析 / メインエントリー
│   ├── weather.py          # 天気APIクライアントロジック
│   ├── time_utils.py       # JSTタイムヘルパー
│   └── models.py           # （オプション）レスポンス用データクラス
├── tests/
│   ├── test_weather.py
│   ├── test_time_utils.py
│   └── test_cli.py
├── README.md
├── requirements.txt（またはpyproject.toml）
└── .env（バージョン管理から除外 / .env.exampleによるサンプル）
```

---
## テスト
このプロジェクトはpytestを使用した包括的なテストカバレッジ（99%以上）を持っています。詳細なテスト情報については、**[TESTING.md](TESTING.md)**を参照してください。

### クイックスタート
すべてのテストを実行:
```bash
pytest -v
```

カバレッジレポート付きでテストを実行:
```bash
pytest --cov=tokyoweather --cov-report=term-missing
```

特定のテストカテゴリーを実行:
```bash
pytest -m unit           # ユニットテストのみ
pytest -m integration    # 統合テストのみ
pytest -m "not slow"     # 遅いテストを除外
```

### テスト統計
- **総テスト数**: 42（41成功、1スキップ）
- **テストカバレッジ**: 99%（83/83ステートメント）
- **テストカテゴリー**:
  - ユニットテスト: 22（天気API、時刻ユーティリティ）
  - 統合テスト: 20（CLIメイン関数、サブプロセス実行）

テスト構造、マーカー、モック戦略、トラブルシューティングを含む完全なテストドキュメントについては、**[TESTING.md](TESTING.md)**を参照してください。

---
## 開発ワークフロー
1. フィーチャーブランチを作成: `git checkout -b feature/cli-basic`
2. コードを実装/更新
3. テストを追加または更新
4. `pytest`を実行
5. コミット&プッシュ
6. 関連するIssueを参照してプルリクエストを開く（エピックと子タスクは既に作成済み）

---
## コントリビューションガイドライン
コントリビューションを歓迎します！
- 大きな変更の前にIssueを開く
- PRは焦点を絞って小さく保つ
- 既存のコードスタイル（PEP 8）に従う
- 新しいロジックにテストを追加
- CI（後で追加される場合）が通ることを確認
- シークレットをコミットしない—環境変数を使用

### バグの報告
以下を含めてください:
- 使用したCLIコマンド
- 完全なエラー出力
- 環境（OS、Pythonバージョン）

### 機能の提案
以下を説明するラベル`enhancement`付きのIssueを開く:
- ユースケース
- 提案されるインターフェース/フラグ
- 出力例

---
## セキュリティ
- `.env`や実際のAPIキーをコミットしないでください。
- 本番レベルの使用では、レート制限/リトライの追加を検討してください。

---
## ロードマップ（高レベル）
- [x] Issueのドラフト作成（エピック+タスク）
- [ ] 基本的な天気/時刻モジュールの実装
- [ ] CLIブートストラップの実装
- [ ] argparseと基本的なフラグの追加
- [ ] JSON出力モード
- [ ] テストカバレッジ>80%
- [ ] PyPIへのパッケージ公開（オプション）

---
## ライセンス
MITライセンス（リポジトリが別のライセンスを選択しない限り）。`LICENSE`ファイルがまだ存在しない場合は、将来のコミットで追加されます。

---
## 謝辞
- OpenWeatherMap（または選択された天気APIプロバイダー）
- Pythonコミュニティとオープンソースライブラリ

---
## トラブルシューティング

### よくある問題

**問題: CLIを実行する際の`ModuleNotFoundError`**
- **解決方法:** 仮想環境がアクティブ化され、依存関係がインストールされていることを確認してください:
  ```bash
  source .venv/bin/activate  # またはWindowsの場合 .venv\Scripts\activate
  pip install -r requirements.txt
  ```

**問題: 環境変数を設定したにもかかわらずAPIキーエラー**
- **解決方法:** 
  1. 変数が設定されているか確認: `echo $OPENWEATHER_API_KEY`（Linux/Mac）または`echo %OPENWEATHER_API_KEY%`（Windows）
  2. `.env`を使用している場合、ファイルがプロジェクトのルートディレクトリにあることを確認
  3. ターミナルを再起動するか、仮想環境を再アクティブ化

**問題: ネットワーク/接続エラー**
- **解決方法:**
  1. インターネット接続を確認
  2. OpenWeatherMapでテストしてAPIキーが有効であることを確認
  3. ファイアウォールが`api.openweathermap.org`へのリクエストをブロックしていないか確認

**問題: テストの実行に失敗**
- **解決方法:**
  1. `pytest`がインストールされていることを確認: `pip install pytest`
  2. プロジェクトのルートディレクトリから実行
  3. テストファイルが`tests/`ディレクトリにあることを確認

**問題: 仮想環境の作成時にパーミッションが拒否される**
- **解決方法:** 
  - Linux/Macの場合: `python`の代わりに`python3`を使用する必要がある場合があります
  - Windowsの場合: 必要に応じて管理者としてターミナルを実行

---
## FAQ
**Q: なぜ東京だけなのですか？**  
A: MVPの範囲です。後で任意の都市入力に一般化できます。

**Q: 別の天気プロバイダーを使用できますか？**  
A: はい。`weather.py`で取得ロジックを抽象化し、アダプターを追加してください。

**Q: 単位を変更するにはどうすればよいですか？**  
A: `--units`フラグを予定しています。現在はメトリックがデフォルトです。

**Q: 必要なPythonバージョンは？**  
A: Python 3.10以上を推奨します。`python --version`でバージョンを確認してください。

**Q: CLIが「API key not set」と表示されます。どうすればよいですか？**  
A: `OPENWEATHER_API_KEY`環境変数を設定するか、APIキーを含む`.env`ファイルを作成してください。[環境変数](#環境変数)セクションを参照してください。

**Q: OpenWeatherMap APIキーを取得するにはどうすればよいですか？**  
A: [OpenWeatherMap](https://openweathermap.org/api)でサインアップし、無料のAPIキーを作成してください。無料ティアはこのツールに十分です。

**Q: テストがネットワークエラーで失敗します。これは正常ですか？**  
A: テストはモックされたAPI呼び出しを使用し、ネットワークアクセスを必要としないはずです。ネットワークエラーが表示される場合は、テストが外部呼び出しを適切にモックしていることを確認してください。

**Q: インストールせずにこのツールを実行できますか？**  
A: はい、仮想環境をアクティブ化して依存関係をインストールした後、次を実行してください: `python -m tokyoweather`

**Q: バグを報告したり機能を提案したりする場所はどこですか？**  
A: 問題や機能強化に関する詳細情報を含めてGitHubリポジトリにIssueを開いてください。

---
## メンテナー
プロジェクト貢献者による初期セットアップ。参加したい場合はお気軽にIssueを開いてください。

---
## 免責事項
このプロジェクトはMVPであり、急速に進化する可能性があります。責任を持って使用してください。
