# vv_secretary

A program that uses VoiceVox to speak like a secretary.

# Motivation

Voicevox音声をMacローカルで喋らせてみたいだけ

# How to setup Mac arm64

```
❯ pip install https://github.com/VOICEVOX/voicevox_core/releases/download/0.15.0/voicevox_core-0.15.0+cpu-cp38-abi3-macosx_11_0_arm64.whl
❯ curl -sSfL https://github.com/VOICEVOX/voicevox_core/releases/latest/download/download-osx-arm64 -o download
❯ chmod +x download
❯ ./download
> sudo ln -s $(pwd)/voicevox_core/libonnxruntime.1.13.1.dylib /usr/local/lib/libonnxruntime.1.13.1.dylib
```

# Use Cases

Commandline

```shell
> python main.py
> python main.puy --mode say --text "夜更かしはやめて、そろそろ寝ましょう。"
```

CronTab

```crontab
0 12,17 * * 1-5 python /path/to/vv_secretary/main.py --option eyedrop >> /tmp/vv_secretary-`date +\%Y-\%m\%d`.log 2>&1
0 0,8,15,19 * * 1-5 python /path/to/vv_secretary/main.py >> /tmp/vv_secretary-`date +\%Y-\%m\%d`.log 2>&1
0 20 * * 1-5 python /path/to/vv_secretary/main.py --mode say --text "20時です、そろそろ仕事は終わりにしましょう。" >> /tmp/vv_secretary-`date +\%Y-\%m\%d`.log 2>&1
```

# Thanks

- 公式
  - [Python サンプルコード](https://github.com/VOICEVOX/voicevox_core/tree/main/example/python)
- voicevox_core.blockingが見つからない問題
  - [PythonでVOICEVOX COREを使ってみる](https://404background.com/program/voicevox-core/#voicevox_coreblocking%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)

