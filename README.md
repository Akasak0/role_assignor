# Roll Assignor

Discord サーバーのメンバーに対して、AtCoder のレーティングに応じたロールを自動で割り当てる Discord Bot です。

## Features

- Discord ユーザーと AtCoder アカウントの紐付け
- AtCoder のレーティングに応じたロールの割り当て
- レーティング帯が変わった場合のロール更新
- レーティング帯が変わった際のメッセージ送信

## Requirements

- Python 3
- Discord Bot のトークン
- Discord サーバーと、そのサーバー内のロールを管理できる権限

## Setup

### 1. Install dependencies

仮想環境を作成し、有効化します。

```bash
python3 -m venv .venv
source .venv/bin/activate
```

依存ライブラリをインストールします。

```bash
pip install discord.py requests python-dotenv
```

### 2. Configure environment variables

プロジェクトのルートディレクトリに `.env` を作成し、Discord Bot のトークンを設定します。

```dotenv
TOKEN=YOUR_DISCORD_BOT_TOKEN
```

トークンは外部に公開しないでください。

### 3. Configure role IDs

`role.json.example` をコピーして、`role.json` を作成します。

```bash
cp role.json.example role.json
```

各値を、使用する Discord サーバーのロール ID に置き換えてください。

```json
{
    "gray": 123456789012345678,
    "brown": 123456789012345679,
    "green": 123456789012345680,
    "water": 123456789012345681,
    "blue": 123456789012345682,
    "yellow": 123456789012345683,
    "orange": 123456789012345684,
    "red": 123456789012345685
}
```

上記の ID は記入例です。実際のサーバーのロール ID に置き換えてください。

ロール ID は Discord の開発者モードを有効にし、対象ロールのメニューから「ロール ID をコピー」を選択して取得できます。

### 4. Configure user data

`atcoder_username.json.example` をコピーして、`atcoder_username.json` を作成します。

```bash
cp atcoder_username.json.example atcoder_username.json
```

初期状態では、次のように空の JSON オブジェクトを使用します。

```json
{}
```

ユーザーと AtCoder アカウントの対応情報は、Bot のコマンドを通じて登録されます。このファイルには Discord ユーザー ID と AtCoder アカウント名が保存されます。

### 5. Configure the Bot

Discord Developer Portal で Bot を作成し、対象サーバーに招待してください。

Bot には、少なくとも次の設定・権限が必要です。

- **Server Members Intent** など、メンバー情報の取得に必要な設定
- ロールの管理
- メッセージの送信
- 対象チャンネルへのアクセス

実際に必要な権限は、Bot のコードやサーバー設定に応じて調整してください。

また、Bot が操作するロールよりも、Bot 自身のロールを Discord のロール一覧で上位に配置してください。Bot のロールより上位にあるロールは操作できません。

## Usage

Bot を起動します。

```bash
python role_assignor.py
```

Discord 上で `/assignment_account` コマンドを実行し、AtCoder アカウント名を登録します。

登録後、Bot は登録されたアカウントのレーティングを取得し、対応するロールを割り当てます。レーティング帯が変わった場合は、古いロールを外して新しいロールを割り当てます。

## Rating and roles

| AtCoder rating | Role |
|---:|---|
| 0–399 | gray |
| 400–799 | brown |
| 800–1199 | green |
| 1200–1599 | water |
| 1600–1999 | blue |
| 2000–2399 | yellow |
| 2400–2799 | orange |
| 2800 以上 | red |

## Files

| File | Description |
|---|---|
| `role_assignor.py` | Bot 本体 |
| `.env` | Discord Bot のトークン |
| `role.json` | ロール名とロール ID の対応 |
| `role.json.example` | `role.json` のサンプル |
| `atcoder_username.json` | Discord ユーザーと AtCoder アカウントの対応情報 |
| `atcoder_username.json.example` | ユーザー情報ファイルのサンプル |
| `requirements.txt` | Python の依存ライブラリ |

`.env`、`role.json`、`atcoder_username.json` は環境固有の情報を含むため、Git リポジトリには登録しないでください。サンプルファイルを利用して、それぞれの環境で作成してください。

## Notes

- AtCoder のレーティング情報を取得するため、インターネット接続が必要です。
- Bot が停止している間は、レーティングの確認やロール更新は実行されません。
- Discord の権限設定やロールの上下関係によっては、ロールの割り当てに失敗する場合があります。

## License

ライセンスを設定する場合は、使用するライセンスに応じて `LICENSE` ファイルを追加してください。
