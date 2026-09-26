#!/usr/bin/env python3
"""Renderiza as peças de um post em JPEG prontos para o Instagram.

Uso:  python3 tools/render.py posts/<pasta>/pecas.html

Cada elemento com classe .rg-canvas e atributo data-out="01" vira <pasta>/01.jpg,
no tamanho exato do canvas (1080x1350 feed/carrossel, 1080x1920 story/reel).
O HTML deve carregar ../../brand/brand.css. Logos: ../../brand/logos/<arquivo>.png
"""
import sys, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

MAX_BYTES = 8 * 1024 * 1024

def main(html_path: str):
    html = pathlib.Path(html_path).resolve()
    out_dir = html.parent
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 2000}, device_scale_factor=1)
        page.goto(html.as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(400)
        fonts_ok = page.evaluate("document.fonts.check('800 40px Montserrat')")
        if not fonts_ok:
            sys.exit("ERRO: Montserrat não carregou — verifique o caminho de brand.css")
        canvases = page.query_selector_all(".rg-canvas[data-out]")
        if not canvases:
            sys.exit("ERRO: nenhum .rg-canvas[data-out] encontrado")
        for el in canvases:
            name = el.get_attribute("data-out")
            box = el.bounding_box()
            png = out_dir / f"{name}.png"
            el.screenshot(path=str(png))
            img = Image.open(png).convert("RGB")
            jpg = out_dir / f"{name}.jpg"
            q = 92
            img.save(jpg, "JPEG", quality=q, optimize=True, progressive=True)
            while jpg.stat().st_size > MAX_BYTES and q > 60:
                q -= 8
                img.save(jpg, "JPEG", quality=q, optimize=True, progressive=True)
            png.unlink()
            # checa overflow de texto: nenhum filho pode ultrapassar o canvas
            overflow = el.evaluate("""c => { const r=c.getBoundingClientRect(); let bad=[];
                c.querySelectorAll('*').forEach(n=>{if(n.closest('.rg-decor'))return;const b=n.getBoundingClientRect();
                  if(b.width&&(b.right>r.right+1||b.bottom>r.bottom+1||b.left<r.left-1)) bad.push(n.className||n.tagName)});
                return bad.slice(0,5) }""")
            print(f"{jpg.name}: {img.size[0]}x{img.size[1]} · {jpg.stat().st_size//1024} KB" + (f" · ATENÇÃO overflow em {overflow}" if overflow else ""))
        browser.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
