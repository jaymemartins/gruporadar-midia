# Estratégia de Instagram — @gruporadarsistemas

Fonte da verdade para as rotinas automáticas. Identidade visual: `brand/` (espelho do Design System "Grupo Radar Sistemas" no Claude).

## Objetivo

Transformar o perfil em referência de **controle operacional com evidência** para quem responde pela operação, e gerar conversas comerciais pelo direct.

Metas para os primeiros 90 dias (a partir de 26/09/2026):
- Consistência: 3 posts de feed por semana + 1 Story por dia, sem falhas.
- Alcance médio por post de feed: de ~25 (ago/2026) para 150+.
- Salvamentos + compartilhamentos: pelo menos 5 por post de feed.
- Conversas com palavra-chave no direct: 2+ por semana a partir do 2º mês.

Linha de base (26/09/2026): 176 seguidores, 15 posts, último post em 30/08, alcance dos últimos posts 24–29, salvamentos ~0.

## Público

Quem responde pela operação e sente a dor quando algo falha:
- Empresas de facilities e terceirização (gestor de operações, supervisor, diretor)
- Empresas de segurança condominial e patrimonial
- Administradoras de condomínio e gestores de condomínio
- Síndicos (profissionais e moradores)

## Pilares de conteúdo

| Pilar | Peso | O que é | Exemplos |
| --- | --- | --- | --- |
| Dor e erro comum | 35% | O problema real, do jeito que acontece | Posto descoberto que ninguém viu; ronda assinada que não aconteceu; ponto batido fora do posto |
| Educação prática | 25% | Algo útil que a pessoa salva | Checklist de passagem de turno; como auditar ronda; o que registrar numa ocorrência |
| Produto resolvendo | 20% | A tela/fluxo resolvendo a dor em segundos | Alerta de posto descoberto; mapa da ronda; ponto com foto e geofence |
| Prova e confiança | 15% | Números, antes/depois, bastidor de implantação | "Antes: livro de papel. Depois: 8/8 pontos com foto" |
| Marca e bastidor | 5% | Quem está por trás, visão | Por que criamos o Radar |

Nunca começar pelo produto. A ordem é sempre dor → consequência → como resolver.

## Grade semanal

Publicação por volta das **11h30 (horário de Brasília)**.

| Dia | Feed | Story |
| --- | --- | --- |
| Segunda | **Carrossel** (dor ou educação) | Chamada para o carrossel |
| Terça | — | Pergunta para responder por direct |
| Quarta | **Post estático ou Reel curto** (dor + pergunta) | Dica rápida |
| Quinta | — | Tela/fluxo do produto (sem dado real) |
| Sexta | **Carrossel ou Reel** (produto resolvendo / prova) | Chamada para o post |
| Sábado | — | Frase de posicionamento |
| Domingo | — | Pergunta leve / bastidor |

Rodízio de produto: cada semana cobre os três (Radar Ronda, Radar Ponto, Radar Operacional), um por post de feed, alternando a ordem. Posts de dor/educação podem ser do grupo (sem produto).

Formatos:
- **Carrossel** 6–8 slides: capa forte, 1 ideia por slide, último slide com CTA.
- **Estático**: uma dor + consequência + prova.
- **Reel curto** 7–15 s: 3–5 quadros 9:16 com transição (`tools/reel.py`), primeiro quadro com o hook. Sem rosto, sem locução.
- **Story**: 1 imagem 9:16, 1 mensagem, chamada escrita na arte ("responda este story", "veja o post de hoje"). Figurinhas não funcionam por API.

## CTA

- Posts educativos e de dor: **pergunta para comentar** ("Comente o número", "Como vocês fazem hoje?").
- Posts de produto e prova: **palavra-chave no direct**: `RONDA`, `PONTO` ou `OPERACIONAL`. Ex.: "Quer ver como funciona? Mande PONTO no direct."
- Na bio: link do site. Nunca "compre agora", urgência falsa ou promessa absoluta.

## Legenda e hashtags

- 1ª linha = hook. 3–6 linhas curtas. CTA no fim. Máx. 1–2 emojis funcionais.
- Até 5 hashtags, específicas. Banco: #SegurancaCondominial #Condominios #Sindico #Facilities #GestaoDeFacilities #Terceirizacao #GestaoOperacional #SegurancaPatrimonial #ControleDePonto #Portaria + a do produto (#RadarRonda #RadarPonto #RadarOperacional).

## Regras de conteúdo

- Dados, horários, nomes de posto e telas são **exemplos fictícios**; nunca apresentar número inventado como estatística de mercado. Estatística real só com fonte.
- Nunca citar cliente real, condomínio real ou pessoa real sem autorização.
- Não repetir o tema de nenhum dos últimos 6 posts de feed (ver `LOG.md`).
- Benchmark de concorrentes serve para tema, formato e estrutura. Nunca copiar texto, arte ou roteiro.
- Esta rotina **não mexe em anúncios pagos**.

## Métricas (relatório semanal)

Por post: alcance, visualizações, salvamentos, compartilhamentos, comentários, seguidores gerados (`media_follows`), visitas ao perfil. Para Reels: pulo nos 3 primeiros segundos e tempo médio assistido. Conta: seguidores, alcance diário, interações.
O que mais importa: **salvamentos + compartilhamentos** (descoberta) e **direct com palavra-chave** (lead).
