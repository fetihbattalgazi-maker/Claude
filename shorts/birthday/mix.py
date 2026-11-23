"""Mix narration + self-made music (ducked under the voice) + sound effects, then mux with the 4K video."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import video as V
O = os.path.join(HERE, 'out'); A = os.path.join(HERE, 'audio')
ids = sorted(V.T)
inp, fc = [], []
for i in ids: inp += ['-i', os.path.join(A, f'e{i:02d}.mp3')]
inp += ['-i', os.path.join(O, 'music.wav'), '-i', os.path.join(O, 'fx.wav')]
n = len(ids); TOT = V.TOTAL
for k, i in enumerate(ids):
    ms = int(V.T[i] * 1000); fc.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[n{k}]")
fc.append(''.join(f'[n{k}]' for k in range(n)) + f"amix=inputs={n}:normalize=0,apad,atrim=0:{TOT:.2f},asplit=2[vo][sc]")
fc.append(f"[{n}:a]volume=0.5,apad,atrim=0:{TOT:.2f}[m]")
fc.append("[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md]")
fc.append(f"[{n + 1}:a]volume=0.55,apad,atrim=0:{TOT:.2f}[fx]")
fc.append(f"[vo][md][fx]amix=inputs=3:normalize=0,atrim=0:{TOT:.2f},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(['ffmpeg', '-y', '-v', 'error', *inp, '-filter_complex', ';'.join(fc), '-map', '[a]', '-c:a', 'aac', '-b:a', '192k',
                '-ar', '48000', os.path.join(O, 'audio.m4a')], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(O, 'video_4k.mp4'), '-i', os.path.join(O, 'audio.m4a'),
                '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', '-movflags', '+faststart',
                os.path.join(O, 'birthday_paradox_4k.mp4')], check=True)
print('FINAL OK')
