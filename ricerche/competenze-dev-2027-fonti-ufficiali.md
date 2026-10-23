# Cosa deve saper fare un dev nel 2027 (ricerca del 24/10/2026)

Fonti ufficiali/primarie, salvo dove indicato. Dove non ho trovato l'edizione 2026 lo dico.

## Evidenze
- WEF Future of Jobs 2025 (gen 2025, attese dei datori di lavoro 2025-2030): competenze in più rapida crescita = IA e big data, reti e cybersecurity, alfabetizzazione tecnologica; poi pensiero creativo, resilienza, curiosità e apprendimento continuo. Sviluppatore software = 4º lavoro per crescita. https://www.weforum.org/publications/the-future-of-jobs-report-2025/in-full/3-skills-outlook/
- Stack Overflow Developer Survey 2026 (6/10/2026, 30.000+ risposte): assistenti/agenti di codice usati dal 66%; delegano codice in area familiare 69%, debug/refactoring 64%, test 58%, codice in area non familiare 56%; comunicazione e design molto meno (35% e 49%). Fiducia solo se verificabile (48%); solo 6,6% si fida per decisioni importanti; 76% valida eseguendo in locale; 10% usa le risposte così come sono. Per lavori IA: Python 39%, JavaScript 38%. https://survey.stackoverflow.co/2026/ai
- Anthropic Economic Index (2026) e analisi sviluppo software: su Claude Code il 79% è automazione (49% su Claude.ai); il codice richiede comunque molta revisione e iterazione umana (feedback loop +18,3%); lavori centrati su app e interfacce semplici esposti prima. Dati dell'analisi software: aprile 2025, solo Claude.ai Free/Pro e Claude Code. https://www.anthropic.com/research/impact-software-development
- BLS (2024-34): sviluppatori software +15,8% (≈267.700 posti), previsione precedente +17,9%; effetto netto dell'IA "altamente incerto"; l'IA può creare domanda (sviluppare e mantenere soluzioni IA). https://www.bls.gov/opub/ted/2026/artificial-intelligence-information-technology-and-employment-2024-34.htm
- GitHub Octoverse 2025 (nessun 2026 trovato): TypeScript #1; Python primo nei repository IA; i linguaggi tipizzati crescono perché rendono verificabile il codice generato; il controllo accessi mancante è la vulnerabilità più comune nel codice scaffold dell'IA. https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- DORA 2025 (nessun 2026 trovato): 90% usa IA; l'IA aumenta la velocità ma peggiora la stabilità delle consegne se i controlli a valle sono deboli; costo nascosto = verifica e revisione. https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- ACM/IEEE CS2023 e analisi dei programmi 2026: competenze emergenti = alfabetizzazione IA, orchestrazione di agenti, pratiche di interazione con l'IA, progetti reali con IA; più peso a esami in presenza e spiegazione del codice. https://arxiv.org/html/2608.05898v1
- Eurostat 2025: 10,45 milioni di specialisti ICT nell'UE (5,0% degli occupati), crescita in rallentamento (2,6% nel 2024-25); obiettivo 2030 di 20 milioni. Commissione (nov 2025): gap di 6,2-7 milioni di lavoratori IA entro il 2027. https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260527-2

## Italia (fonti NON ufficiali: blog, da trattare come indicative)
- Base 2026 secondo guide di settore: un linguaggio a fondo, controllo versione, test automatici, nozioni di cloud/deploy, sicurezza, uso critico degli assistenti IA. https://www.wwg.it/eccezionale-carriera-in-sviluppatore-software
- Lavoro quotidiano spostato dalla scrittura alla revisione critica; responsabilità di sicurezza e architettura resta all'umano; RAG e database vettoriali richiesti. https://www.kinetikon.com/developer-2026-guida-upskilling-ai
- Stipendi junior 24-35 mila €, ma più pagate le specializzazioni (cloud, IA). https://www.concorsando.it/blog/come-diventare-software-engineer
- Nessun dato ufficiale italiano (Istat/ministero) sulle competenze dev richieste trovato.

## Sintesi per decidere cosa studiare
1. Il codice si scrive sempre più con l'IA; il valore umano è verificare, correggere, decidere (SO 2026, DORA, Anthropic, blog italiani).
2. Per verificare servono fondamenti: leggere codice, SQL, HTTP, test, debug, sicurezza, tipi.
3. Cresce la domanda di chi sa costruire e mantenere sistemi IA (BLS, WEF, Commissione): RAG, valutazione, costi, guardrail.
4. Boilerplate, interfacce semplici, configurazioni e pezzi con risposta facilmente verificabile sono i più delegati.
5. Limiti: sondaggi autodichiarati, previsioni incerte, niente Octoverse/DORA 2026, Italia solo da blog.
