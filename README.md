## 概要
discordのサウンドボードに、手軽にサウンドを追加するために作った。

## Requirement
- uv (https://github.com/astral-sh/uv)
- ffmpeg
- docker

## 利用方法
最初に使う前に
- `uv sync` をしてください。

音声データ作成方法。

- `./run.sh {テキスト}`
  - 例：`./run.sh いいのだ`

output.mp3が出力される。

discordへの追加は手動。

