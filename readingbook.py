from gtts import gTTS
import os

def convert_text_to_audio(file_name, file_content):
    """将文本转换为音频文件"""
    text_file_name = file_name
    text_content = file_content
    # 2. 分割句子
    sentences = [s.strip() for s in text_content.split('\n') if s.strip()]

    # 3. 创建音频目录
    audio_dir = r"app001/toHtml/audio_files"
    os.makedirs(audio_dir, exist_ok=True)

    # 4. 生成单个句子MP3
    sentence_files = []
    for i, sentence in enumerate(sentences):
        filename = os.path.join(audio_dir, f"{text_file_name}_sentence_{i}.mp3")
        tts = gTTS(sentence, lang='zh-cn')
        tts.save(filename)
        sentence_files.append(filename.replace('app001/toHtml/', ''))

    # 5. 生成完整音频MP3
    full_audio = os.path.join(audio_dir, f"{text_file_name}_full_audio.mp3")
    tts = gTTS(text_content, lang='zh-cn')
    tts.save(full_audio)
    full_audio=full_audio.replace('app001/toHtml/', '')

    # 6. 生成HTML点读页面
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{text_file_name}</title>
        <style>
            body {{ font-family: 'Microsoft YaHei', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            .sentence {{ margin: 15px 0; padding: 10px; border-left: 3px solid #4CAF50; cursor: pointer; }}
            .sentence:hover {{ background-color: #f0f9ff; }}
            .controls {{ margin: 20px 0; padding: 15px; background-color: #f5f5f5; border-radius: 5px; }}
            button {{ padding: 10px 15px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px; }}
            button:hover {{ background-color: #45a049; }}
        </style>
    </head>
    <body>
        <nav style="position:sticky;top:0;background:#f5f5f5;padding:8px 12px;border-bottom:1px solid #ddd;display:flex;gap:12px;font-family:sans-serif;z-index:999;">
        <button onclick="history.back()" style="cursor:pointer;">← 返回上一页</button>
        <button onclick="location.href=\'index.html\'" style="cursor:pointer;">🏠 首页</button>
        </nav>
        <h1>{text_file_name}</h1>
        
        <div class="controls">
            <button onclick="playFullAudio()">播放完整内容</button>
            <button onclick="pauseAll()">暂停所有</button>
            <audio id="fullAudio" src="{full_audio}"></audio>
        </div>
        
        <div id="content">
            {"".join(f'<div class="sentence" onclick="playSentence({i})">{sentence}</div>' 
                    for i, sentence in enumerate(sentences))}
        </div>

        <script>
            // 存储所有音频对象
            const audioElements = [];
            
            // 初始化单个句子音频
            {''.join(f"const audio{i} = new Audio('{file.replace('\\', '/')}'); audioElements.push(audio{i});" 
                    for i, file in enumerate(sentence_files))}
            
            // 播放指定句子
            function playSentence(index) {{
                pauseAll();
                audioElements[index].currentTime = 0;
                audioElements[index].play();
            }}
            
            // 播放完整内容
            function playFullAudio() {{
                pauseAll();
                document.getElementById('fullAudio').play();
            }}
            
            // 暂停所有音频
            function pauseAll() {{
                audioElements.forEach(audio => audio.pause());
                document.getElementById('fullAudio').pause();
            }}
        </script>
    </body>
    </html>
    """

    # 7. 保存HTML文件
    with open( r"app001/toHtml/"+text_file_name+".html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("生成完成！请打开"+text_file_name+".html 使用点读功能")

if __name__ == "__main__":    
    # 1. 读取文本内容
    text_content = """New York is 3 hours ahead of California

    But it does not make California slow

    Someone graduated at the age of 22

    But waited 5 years before securing a good job

    Someone became a CEO at 25 and died at 50

    While another became a CEO at 50 and lived to 90 years

    Someone is still single while someone else got married

    Obama retires at 55, but Trump starts at 70

    Absolutely everyone in this world works based on their Time Zone

    People around you might seem to go ahead of you

    Some might seem to be behind you

    But everyone is running their own RACE, in their own TIME

    Don't envy them or mock them

    They are in their TIME ZONE, and you are in yours

    Life is about waiting for the right moment to act

    So, RELAX. You're not LATE. You're not EARLY

    You are very much ON TIME, and in your TIME ZONE
    """
    convert_text_to_audio("《time zome》",text_content)