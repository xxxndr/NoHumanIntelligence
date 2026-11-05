# NoHumanIntelligence

Assistente IA per PMI, in sviluppo: risponderà ai clienti usando i documenti dell'azienda, aprirà ticket e passerà il caso a una persona quando non è sicuro.

## Stato

Progetto di studio, in sviluppo. Fatti: scheletro dell'API, validazione degli input con errori RFC 9457, schema PostgreSQL e test. La risposta del modello è ancora un segnaposto: l'LLM arriva nel passo successivo.

## Stack

Python, FastAPI, Pydantic, PostgreSQL, pytest. Previsti: Pydantic AI e ricerca sui documenti con pgvector.

## Obiettivi

Risposte dai documenti con la fonte citata, passaggio a una persona, sicurezza (prompt injection, dati personali, conferma umana per le azioni importanti) e risparmio di tempo misurato su dati di prova inventati.
