import os
import asyncio
import edge_tts
import subprocess
import dashscope
from dashscope import Generation

# 读取阿里云密钥
dashscope.api_key = os.getenv("ALI_ACCESS_KEY_SECRET")

# AI生成文案函数
def create_script(prompt):
    response = Generation.call(
        model="qwen-turbo",
        prompt=prompt,
        result_format="message"
    )
    if response.status_code == 200:
        return response.output.choices[0].message.content
    else:
        return f"生成失败：{response.message}"

# 1. AI生成电影解说文案
prompt = "为这部电影写一段150字左右的影视解说文案，节奏紧凑，适合短视频配音"
text = create_script(prompt)

# 2. 文字转语音
voice = "zh-CN-YunyangNeural"
communicate = edge_tts.Communicate(text, voice)

async def tts_task():
    await communicate.save_to_file("audio.mp3")

asyncio.run(tts_task())

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
