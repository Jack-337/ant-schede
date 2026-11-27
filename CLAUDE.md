# Istruzioni per Claude Code

Prima di fare qualsiasi cosa leggi **ANT.md**: contiene il contesto completo del progetto (storia, struttura, modello dei dati, build e rilascio, cose da verificare) e indica come lavorare con Jack.

Regole rapide:
- Si scrive in italiano, in modo semplice: Jack non programma.
- Il codice si modifica in `src/`; la radice del repo è il sito pubblicato e si rigenera con `node src/build-site.mjs <nuova versione>`.
- A ogni rilascio la versione va alzata. Prima del push vanno lanciati i test in `tests/`.
- Il repo è pubblico: niente dati personali.
