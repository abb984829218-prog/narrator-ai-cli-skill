from openai import OpenAI
import asyncio
import edge_tts
import subprocess

# 初始化客户端
client = OpenAI()

# 1. AI生成电影解说文案
prompt = "为这部电影写一段150字左右的影视解说文案，节奏紧凑，适合短视频配音"
resp = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
text = resp.choices[0].message.content

# 2. 文字转语音
voice = "zh-CN-YunyangNeural"
communicate = edge_tts.Communicate(text, voice)
asyncio.run(communicate.save_sync("audio.mp3"))

# 3. FFmpeg把视频和音频合并
cmd = [
    "ffmpeg",
    "-i", "source.mp4",
    "-i", "audio.mp3",
    "-c:v", "copy",
    "-c:a", "aac",
    "output_video.mp4"
]
subprocess.run(cmd)