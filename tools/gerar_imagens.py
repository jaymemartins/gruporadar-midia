#!/usr/bin/env python3
"""Roda no GitHub Actions (tem internet). Lê pedidos/*.json, gera/baixa/decodifica imagens e salva no destino.

Pedido (pedidos/<slug>.json):
{
  "destino": "posts/2026-09-28-slug/fotos",
  "imagens": [
    {"nome": "cena", "fonte": "ia", "prompt": "...", "modelo": "@cf/black-forest-labs/flux-1-schnell"},
    {"nome": "portaria", "fonte": "foto", "busca": "security guard building lobby", "orientacao": "portrait"},
    {"nome": "arte-pronta", "fonte": "base64", "conteudo": "<BASE64 JPEG>"}
  ]
}
fonte "ia"     -> Cloudflare Workers AI (FLUX), segredos CF_ACCOUNT_ID e CF_API_TOKEN
fonte "foto"   -> Pexels (fotos reais, uso comercial livre), segredo PEXELS_API_KEY
fonte "base64" -> JPEG pronto enviado em base64; apenas decodifica e grava, sem recompressão
Resultado: <destino>/<nome>.jpg e <destino>/creditos.json. O pedido vai para pedidos/feitos/.
Erros ficam em <destino>/ERRO.txt (a rotina lê e decide).
"""
import base64, glob, json, os, pathlib, shutil, sys, urllib.error, urllib.parse, urllib.request

CF_ID, CF_TOKEN, PEXELS = [(os.getenv(k) or "").strip() or None for k in ("CF_ACCOUNT_ID", "CF_API_TOKEN", "PEXELS_API_KEY")]

UA = "Mozilla/5.0 (X11; Linux x86_64) gruporadar-midia/1.0"

def http(url, data=None, headers=None, timeout=120):
    h = {"User-Agent": UA, **(headers or {})}
    req = urllib.request.Request(url, data=data, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        corpo = e.read()[:400].decode("utf-8", "replace")
        host = urllib.parse.urlparse(url).netloc
        raise RuntimeError(f"HTTP {e.code} em {host}: {corpo}") from None

def gerar_ia(item):
    if not (CF_ID and CF_TOKEN):
        raise RuntimeError("segredos CF_ACCOUNT_ID/CF_API_TOKEN ausentes")
    modelo = item.get("modelo", "@cf/black-forest-labs/flux-1-schnell")
    body = {"prompt": item["prompt"], "steps": item.get("steps", 8)}
    if "seed" in item: body["seed"] = item["seed"]
    raw = http(f"https://api.cloudflare.com/client/v4/accounts/{CF_ID}/ai/run/{modelo}",
               json.dumps(body).encode(), {"Authorization": f"Bearer {CF_TOKEN}", "Content-Type": "application/json"})
    res = json.loads(raw)
    if not res.get("success", True) or "result" not in res:
        raise RuntimeError(f"Cloudflare: {res.get('errors')}")
    return base64.b64decode(res["result"]["image"]), {"fonte": "IA (Cloudflare Workers AI)", "modelo": modelo, "prompt": item["prompt"]}

def baixar_foto(item):
    if not PEXELS:
        raise RuntimeError("segredo PEXELS_API_KEY ausente")
    q = urllib.parse.urlencode({"query": item["busca"], "orientation": item.get("orientacao", "portrait"), "per_page": 15, "size": "large"})
    res = json.loads(http(f"https://api.pexels.com/v1/search?{q}", headers={"Authorization": PEXELS}))
    fotos = res.get("photos", [])
    if not fotos:
        raise RuntimeError(f"Pexels: nada para '{item['busca']}'")
    f = fotos[min(item.get("indice", 0), len(fotos) - 1)]
    img = http(f["src"]["large2x"])
    return img, {"fonte": "Pexels", "fotografo": f["photographer"], "url": f["url"], "busca": item["busca"],
                 "alternativas": [x["url"] for x in fotos[:6]]}

def decodificar_base64(item):
    conteudo = (item.get("conteudo") or "").strip()
    if not conteudo:
        raise RuntimeError("conteudo base64 ausente")
    if conteudo.startswith("data:"):
        conteudo = conteudo.split(",", 1)[-1]
    try:
        img = base64.b64decode(conteudo, validate=True)
    except Exception as e:
        raise RuntimeError(f"base64 inválido: {e}") from None
    if len(img) < 4:
        raise RuntimeError("imagem base64 vazia ou inválida")
    return img, {"fonte": "Upload base64", "bytes": len(img)}

def main():
    pedidos = sorted(glob.glob("pedidos/*.json"))
    if not pedidos:
        print("nenhum pedido"); return
    for p in pedidos:
        ped = json.load(open(p))
        dest = pathlib.Path(ped["destino"]); dest.mkdir(parents=True, exist_ok=True)
        for velho in ("creditos.json", "ERRO.txt"):
            (dest / velho).unlink(missing_ok=True)
        creditos, erros = {}, []
        for item in ped["imagens"]:
            try:
                fonte = item["fonte"]
                if fonte == "ia":
                    img, meta = gerar_ia(item)
                elif fonte == "foto":
                    img, meta = baixar_foto(item)
                elif fonte == "base64":
                    img, meta = decodificar_base64(item)
                else:
                    raise RuntimeError(f"fonte desconhecida: {fonte}")
                (dest / f"{item['nome']}.jpg").write_bytes(img)
                creditos[item["nome"]] = meta
                print(f"ok {dest}/{item['nome']}.jpg ({len(img)//1024} KB)")
            except Exception as e:
                erros.append(f"{item['nome']}: {e}")
                print(f"ERRO {item['nome']}: {e}", file=sys.stderr)
        (dest / "creditos.json").write_text(json.dumps(creditos, ensure_ascii=False, indent=2))
        if erros:
            (dest / "ERRO.txt").write_text("\n".join(erros))
        pathlib.Path("pedidos/feitos").mkdir(parents=True, exist_ok=True)
        shutil.move(p, f"pedidos/feitos/{pathlib.Path(p).name}")

if __name__ == "__main__":
    main()
