#!/bin/bash

function usage() {
    cat<<EOF
Usage:
    ./run.sh {text}
EOF
}

if [ $# -ne 1 ]; then
    usage
    exit 1
fi

docker run --rm -d --name voicevox -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest

# リクエストが早すぎると起動が間に合わないからちょっと待つ
sleep 1

python3 main.py $@

docker stop voicevox
