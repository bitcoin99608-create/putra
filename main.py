from flask import Flask, request, send_file, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/cut', methods=['GET'])
def cut_video():
    url = request.args.get('url')
    start = request.args.get('start')
    end = request.args.get('end')
    
    if not url or not start or not end:
        return jsonify({"error": "Data tidak lengkap"}), 400
        
    output_filename = "hasil_clip.mp4"
    if os.path.exists(output_filename):
        os.remove(output_filename)
        
    try:
        # Mengambil link video asli dari YouTube
        video_url = subprocess.check_output(f'yt-dlp -g "{url}" -f best', shell=True).decode().strip()
        # Memotong langsung pakai FFmpeg
        cmd = f'ffmpeg -ss {start} -to {end} -i "{video_url}" -c:v libx264 -c:a aac -strict experimental {output_filename}'
        subprocess.run(cmd, shell=True, check=True)
        
        return send_file(output_filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
