# Rotinas automáticas — como executar

Leia antes: `ESTRATEGIA.md` (o quê e por quê), `PAUTA.md` (plano da semana), `LOG.md` (o que já foi publicado), `brand/brand.css` e `templates/` (como a arte é feita). A regra visual completa está no Design System "Grupo Radar Sistemas" (artifact do Claude); o resumo operacional é:

- Fundo `#06152A`, texto branco, destaque `#8DFF3F` em no máximo 2–3 palavras do título. Montserrat. Nada abaixo de 24px no canvas.
- Estrutura: hook → dor/evidência → prova/solução → fechamento + assinatura com a marca do produto.
- Assinatura: `radar-operacional.png`, `radar-ronda-simbolo.png` ou `radar-ponto.png` (em `brand/logos/`). Nunca o selo do grupo no rodapé.
- Sem vermelho como destaque, sem amarelo forte, sem fundo claro, sem emoji na arte.

Instagram: conector Windsor.ai, `connector: "instagram"`, `account: "17841441939601843"`.
Imagens públicas: `https://raw.githubusercontent.com/jaymemartins/gruporadar-midia/main/<caminho>`.

## Preparação (toda execução)

1. Clonar o repositório `jaymemartins/gruporadar-midia` com acesso de escrita (adicione o repo à sessão se preciso) e trabalhar dentro dele.
2. Conferir ferramentas: `python3 -c "import playwright, PIL"` e `which ffmpeg`. Não rodar `playwright install`.
3. Autor dos commits: `Jayme Martins <jaymemartins@users.noreply.github.com>` (nunca um e-mail pessoal: o repositório é público).

## Rotina diária (todo dia, ~11h BRT)

1. **Contexto**: ler `PAUTA.md` e as últimas entradas de `LOG.md`. Puxar no Windsor os posts dos últimos 7 dias (`media_id, timestamp, media_type, media_reach, media_saved, media_shares, media_comments_count`) para saber o que já saiu e como foi.
2. **Decidir o que publicar hoje**:
   - Story: sempre (1 imagem 9:16).
   - Feed: segunda, quarta e sexta, conforme `PAUTA.md`. Se a pauta estiver vazia ou desatualizada, escolher pela grade da `ESTRATEGIA.md`, sem repetir tema dos últimos 6 posts de feed.
   - Se já houver post de feed publicado hoje (checar no Windsor), não publicar outro.
3. **Produzir**: criar `posts/AAAA-MM-DD-slug/pecas.html` a partir de `templates/` (e do post `posts/2026-09-26-sinais-ronda/` como referência de carrossel). Cada peça é um `<section class="rg-canvas" data-out="01">` (feed/carrossel 1080×1350) ou `rg-canvas--story` (1080×1920). Renderizar com `python3 tools/render.py posts/<pasta>/pecas.html`. Para Reel: quadros `data-out="r1"`, `r2`… em 9:16, depois `python3 tools/reel.py posts/<pasta> 2.5`.
4. **Revisar de verdade**: abrir cada JPEG com a ferramenta de leitura de imagem e conferir contra o checklist abaixo. O render avisa "ATENÇÃO overflow": isso bloqueia até corrigir.
5. **Legenda** em `posts/<pasta>/legenda.txt` (hook na 1ª linha, CTA, até 5 hashtags).
6. **Publicar**: `git add`, commit, `git push`; confirmar que cada URL raw responde 200 `image/jpeg` (ou `video/mp4`). Depois `execute_action` no Windsor:
   - carrossel: `create_carousel_post` {image_urls, caption}
   - estático: `create_image_post` {image_url, caption}
   - Reel: `create_video_post` {video_url, caption, cover_url opcional}
   - Story: `create_story` {image_url}
7. **Verificar**: `get_data` do Instagram com `date_preset: "last_1dT"` e confirmar que o post aparece; pegar o `media_permalink`.
8. **Registrar** no topo de `LOG.md`: data, formato, produto, pilar, tema, hook, CTA, media_id, permalink. Commit e push.
9. **Avisar o Jayme** com uma mensagem curta: o que foi publicado, o racional em 1–2 frases e o link.

### Checklist (um "não" bloqueia a publicação)

- Tamanho exato; texto fora das áreas seguras do Story; nada cortado ou sobreposto.
- Fundo e cores da paleta; lime só nas palavras-chave; Montserrat carregada.
- Uma dor, uma mensagem; título entendido em 1–2 segundos; português correto.
- Nenhum dado apresentado como real sem fonte; nenhum cliente real.
- Tema diferente dos últimos 6 posts de feed.
- Assinatura com o produto certo.
- Legenda com hook, CTA e até 5 hashtags.

### Se algo falhar

Nunca publicar algo inferior. Se a arte não passar no checklist após 2 tentativas de correção, ou se push/URL/Windsor falharem: deixar a peça pronta em `posts/<pasta>/` com `RASCUNHO.md` explicando o que faltou, registrar no `LOG.md` como "não publicado" e avisar o Jayme. Não repetir uma publicação que possa ter saído (verificar no Windsor antes de tentar de novo). Não mexer em anúncios pagos.

## Rotina semanal (domingo, ~19h BRT)

1. **Métricas**: no Windsor, os posts dos últimos 7 e 30 dias com alcance, visualizações, salvamentos, compartilhamentos, comentários, `media_follows`, `media_profile_visits`; Reels com `media_reel_skip_rate` e `media_reel_avg_watch_time`; conta com `followers_count`. Comparar com a semana anterior (`relatorios/`).
2. **Leitura**: quais temas, formatos, hooks e produtos performaram melhor ou pior e por quê (hipótese curta).
3. **Benchmark**: pesquisa pública na web de perfis de referência e concorrentes em facilities, segurança condominial, controle de ponto, ronda, terceirização e condomínios: temas, formatos e hooks que engajam. Só como referência, nunca copiar.
4. **Relatório** em `relatorios/AAAA-Wsemana.md`: números, 3 aprendizados, o que muda na próxima semana.
5. **Pauta**: reescrever `PAUTA.md` para os próximos 7 dias (segunda a domingo) seguindo a grade e os pilares: para cada dia, formato, produto, pilar, tema, hook e CTA. Dobrar a aposta no que funcionou; manter 1 teste por semana (formato ou tipo de hook novo).
6. Commit, push e avisar o Jayme com um resumo de 5 linhas e o link do relatório no GitHub.
