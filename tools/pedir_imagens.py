#!/usr/bin/env python3
"""Envia um pedido de imagens para o GitHub Actions e espera o resultado.

Uso:  python3 tools/pedir_imagens.py pedidos/<slug>.json

1. Faz commit + push do pedido (o push dispara a Action "Gerar imagens").
2. Faz git pull a cada 20 s, por até 8 min, até <destino>/creditos.json aparecer.
3. Mostra o que chegou e o conteúdo de ERRO.txt, se houver.
Código de saída: 0 = todas as imagens chegaram; 2 = chegaram com erro(s); 3 = tempo esgotado.
"""
import json, pathlib, subprocess, sys, time

AUTOR = ["-c", "user.name=Jayme Martins", "-c", "user.email=jaymemartins@users.noreply.github.com"]
MSG = ("Pedido de imagens: {}\n\nCo-Authored-By: Claude <noreply@anthropic.com>")

def git(*args, check=True):
    return subprocess.run(["git", *args], check=check, capture_output=True, text=True)

def main(pedido):
    p = pathlib.Path(pedido)
    ped = json.loads(p.read_text())
    dest = pathlib.Path(ped["destino"])
    nomes = [i["nome"] for i in ped["imagens"]]
    for velho in ("creditos.json", "ERRO.txt"):  # resposta de tentativa anterior
        if (dest / velho).exists():
            git("rm", "-q", str(dest / velho))
    git("add", str(p))
    git(*AUTOR, "commit", "-m", MSG.format(p.stem))
    git("pull", "--rebase", "origin", "main")
    git("push", "origin", "HEAD:main")
    print(f"pedido enviado: {p.name} → aguardando {dest}/")
    inicio = time.time()
    while time.time() - inicio < 480:
        time.sleep(20)
        git("pull", "--rebase", "--autostash", "origin", "main", check=False)
        if (dest / "creditos.json").exists():
            chegaram = [n for n in nomes if (dest / f"{n}.jpg").exists()]
            print(f"chegaram {len(chegaram)}/{len(nomes)}: {', '.join(chegaram) or '-'}")
            erro = dest / "ERRO.txt"
            if erro.exists():
                print("ERRO.txt:\n" + erro.read_text())
                sys.exit(2)
            sys.exit(0)
    print("tempo esgotado (8 min) sem resposta da Action")
    sys.exit(3)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
