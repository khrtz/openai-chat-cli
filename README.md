# openai-chat-cli

OpenAIのGPT-3.5-turboを使用して会話を行うPythonスクリプトです。

### 主な機能
- 会話毎にログをローカルに保存して、会話を引き継げる
- 会話終了後にトークンやコストを表示する
- gpt-3.5-turboを使用。Engineは選択できるようにするかも

## セットアップ

1. このリポジトリをクローンします。

2. openaiライブラリをインストールします。

    `pip install openai`


3. リポジトリのルートディレクトリに`secrets.json`ファイルを作成し、以下のような形式でOpenAI APIキーを記述します。OpenAIのマイページ (https://platform.openai.com/account/api-keys) からAPIを取得して記述します。

```json
{
    "openai_api_key": "YOUR API KEY"
}
```

4. main.pyを実行します。
```shell
python main.py
```
