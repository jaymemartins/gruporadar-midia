#!/usr/bin/env python3
"""Monta um Reel (MP4 9:16) a partir de quadros JPEG 1080x1920 já renderizados.

Uso:  python3 tools/reel.py posts/<pasta> 2.5
      (usa todos os <pasta>/r*.jpg em ordem; 2.5 = segundos por quadro)

Gera <pasta>/reel.mp4: H.264, 30 fps, transição suave entre quadros, trilha de áudio muda.
Mantenha o total entre 7 e 15 s. O primeiro quadro precisa prender em 1–2 s.
"""
import sys, glob, subprocess, pathlib

def main(folder, per):
    frames = sorted(glob.glob(f"{folder}/r*.jpg"))
    if len(frames) < 2:
        sys.exit("ERRO: precisa de pelo menos 2 quadros r*.jpg")
    per = float(per); fade = 0.4
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for f in frames:
        cmd += ["-loop", "1", "-t", str(per + fade), "-i", f]
    total = per * len(frames) + fade
    cmd += ["-f", "lavfi", "-t", str(total), "-i", "anullsrc=r=44100:cl=stereo"]
    chains, prev = [], "[0:v]"
    for i in range(1, len(frames)):
        out = f"[v{i}]"
        chains.append(f"{prev}[{i}:v]xfade=transition=fade:duration={fade}:offset={per*i:.2f}{out}")
        prev = out
    fc = ";".join(chains) + f";{prev}format=yuv420p,scale=1080:1920,fps=30[vout]"
    out = pathlib.Path(folder) / "reel.mp4"
    cmd += ["-filter_complex", fc, "-map", "[vout]", "-map", f"{len(frames)}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-shortest",
            "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                         capture_output=True, text=True).stdout.strip()
    print(f"{out}: {float(dur):.1f}s · {out.stat().st_size//1024} KB")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
