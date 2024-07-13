import subprocess
# 使用ffmpeg合并ts片段
ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', 'lifan/产子岛 ～每周7天都可生产的雌性们/第1集/filelist.txt',
    '-c', 'copy',  # 如果编码一致，可以直接拷贝
    # 如果编码不一致，你可能需要取消注释下一行，并指定输出编码
    # '-codec: copy',  # 替代'-c copy'在某些ffmpeg版本中可能更有效
    'lifan/产子岛 ～每周7天都可生产的雌性们/第1集/合并剧集.mp4',
]

# 执行ffmpeg命令
subprocess.run(ffmpeg_cmd, check=True)