import sys
import requests
from pydub import AudioSegment
import os

OUTPUT_WAV_FILENAME = "output.wav"
OUTPUT_MP3_FILENAME = "output.mp3"
SPEAKER = "3" # 通常ずんだもん
API_HOST = "http://localhost:50021"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <text>")
        sys.exit(1)

    text = sys.argv[1]

    core_version = core_versions()[0]

    # とりあえずcore_versionsは一番目のやつ
    query_data = create_query(text, core_version)
    synthesis(query_data, OUTPUT_WAV_FILENAME, core_version)

    convert_wav_to_mp3(OUTPUT_WAV_FILENAME, OUTPUT_MP3_FILENAME)

# GET /core_versions
def core_versions() -> list[str]:
    url = f"{API_HOST}/core_versions"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()

# POST /audio_query
def create_query(text: str, core_version: str) -> str:
    """
    POST /audio_query に対して text, speaker, core_version などのパラメータを付与し、
    空ボディでJSONレスポンスを受け取る。
    """
    url = f"{API_HOST}/audio_query"
    params = {
        "text": text,
        "speaker": SPEAKER,
        "core_version": core_version,
    }
    headers = {
        "accept": "application/json"
    }
    
    # 空のJSONボディを送信 (Go版では bytes.NewBuffer([]byte{}) 相当)
    # → Voicevoxサーバが期待する形として、-d ''(空)を送っているのと同じにする
    response = requests.post(url, params=params, headers=headers, data="")
    response.raise_for_status()  # ステータスコードが200系以外なら例外

    print("Status (audio_query):", response.status_code)
    # レスポンス（JSON）をそのまま文字列で返す
    return response.text

# POST /synthesis
def synthesis(query_data: str, output_wav: str, core_version: str):
    """
    POST /synthesis に対して、先ほどの音声合成用パラメータ(JSON文字列)をボディとして送り、
    WAV音声を受け取って保存する。
    """
    url = f"{API_HOST}/synthesis"
    params = {
        "speaker": SPEAKER,
        "enable_interrogative_upspeak": "true",
        "core_version": core_version,
    }
    headers = {
        "Accept": "audio/wav",
        "Content-Type": "application/json"
    }

    response = requests.post(url, params=params, headers=headers, data=query_data)
    response.raise_for_status()

    # 音声データ (WAV) をファイルに保存
    with open(output_wav, "wb") as f:
        f.write(response.content)

def convert_wav_to_mp3(input_wav: str, output_mp3: str):
    sound = AudioSegment.from_wav(input_wav)
    sound.export(output_mp3, format="mp3")
    print(f"Audio saved as {output_mp3}")
    
    os.remove(input_wav)

if __name__ == "__main__":
    main()
