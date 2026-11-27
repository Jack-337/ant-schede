# ANT Schede: contesto di progetto per Claude Code

Questo file riassume come è nata l'app e come è fatta, per continuare lo sviluppo da Claude Code. Leggilo tutto prima di modificare qualcosa.

## 1. In breve

- **Cos'è**: web app installabile (PWA), in italiano, per la home gym "ANT Private Training Facility" di Jack (Giacomo Silingardi) e dei suoi amici. Serve a creare schede di allenamento, allenarsi con timer di serie e recupero, tenere un diario dei progressi ed esportare le schede sull'orologio Garmin (Venu 4) come file workout `.fit`.
- **Online**: https://jack-337.github.io/ant-schede/ (GitHub Pages dal branch `main`, cartella radice).
- **Repository**: `Jack-337/ant-schede`, pubblico (obbligatorio per Pages con l'account gratuito).
- **Versione attuale**: 1.2.0.
- **Utente**: Jack non sa programmare. Claude scrive tutto il codice, lo prova e lo pubblica; Jack prova l'app in palestra e propone miglioramenti. Si scrive in italiano, in modo semplice e conciso, senza gergo tecnico non spiegato.

## 2. Come lavorare con Jack

- Quando propone più idee, prima si analizzano insieme: fattibilità, limiti, alternative. Poi si implementano quelle che sceglie. Se una cosa non si può fare, glielo si dice chiaramente e si propone un'alternativa.
- Prima di dire "fatto", provare davvero: test automatici con Playwright, screenshot su telefono (390 px) e desktop, temi chiaro e scuro, nessun errore in console.
- A ogni rilascio: alzare la versione, aggiornare la guida PDF se cambia qualcosa di visibile, fare commit e push, poi spiegare a Jack in poche righe cosa cambia e come aggiornare (aprire l'app con la connessione e premere **Aggiorna**).
- Non inserire mai dati personali nel repo, che è pubblico. Per i commit usare `Jack-337 <Jack-337@users.noreply.github.com>`.

## 3. Storia della costruzione (passo per passo)

1. **Prova di fattibilità Garmin.** Un file `.fit` di tipo *workout* (non *activity*), generato con `@garmin/fitsdk` (classe `Encoder`), con tre esercizi, serie in blocchi ripetuti e recuperi. Si carica collegando l'orologio via USB e copiando il file in `GARMIN/NewFiles`. Il PC di Jack non ha la porta USB-C: serve un adattatore USB-C femmina → USB-A che supporti i dati. **Il test sull'orologio non è ancora stato fatto** (vedi §11).
2. **Prima app** in un unico file HTML locale: editor delle schede, catalogo di 50 esercizi italiani mappati sui codici Garmin, export `.fit`, backup e importazione JSON. Grafica nero/grigio/rosso/bianco con il logo ANT (versione per sfondo scuro: scritte bianche, riquadro rosso con la formica).
3. **Diario**: registrazione manuale degli allenamenti, record personali, grafico dei progressi per esercizio, volume, calendario della costanza, storico.
4. **Sezione Guida** dentro l'app (poi sostituita dalle Impostazioni e dal PDF).
5. **Catalogo completo**: 1.569 esercizi Garmin (profilo FIT SDK), con nomi inglesi, muscoli e attrezzi presi dai dati Garmin Connect. Circa 309 nomi italiani scritti a mano; ricerca in italiano anche sui nomi inglesi tramite glossario; filtri per muscolo e attrezzo; esercizi personalizzati con i muscoli scelti dall'utente.
6. **"Allenati ora"**: allenamento guidato offline con timer della serie e del recupero. A fine recupero suona l'allarme ma la serie successiva **non** parte da sola: il timer conta la pausa extra. Carichi suggeriti dall'ultima volta, serie ed esercizi saltabili, passaggio a un altro esercizio.
7. **Mappa muscolare**: figura fronte/retro disegnata in SVG, colorata per intensità, nel riepilogo e nel Diario.
8. **Pubblicazione online come PWA** (v1.0.0): manifest, icone, service worker con copia offline e banner "Nuova versione disponibile → Aggiorna". La palestra non ha connessione: tutto deve funzionare offline.
9. **v1.0.1**: "Allenati ora" (rosso pieno) e "Registra a mano" (solo contorno) fissi in basso; "Esporta per Garmin" nella scheda.
10. **v1.1.0**: Impostazioni al posto della Guida, con guida PDF scaricabile, tema scuro/chiaro/automatico, volume degli allarmi, vibrazione, bip 3-2-1, schermo acceso, pause predefinite, incrementi di carico e gestione dati. Inoltre: schermata di benvenuto; due pause per esercizio (tra le serie / prima del prossimo); superserie e circuiti; aumento di carico **proposto e da accettare**; fatica per serie (facile/giusta/dura); sforzo percepito 1-10 come sul Garmin.
11. **v1.1.1**: elenco schede con pressione lunga (o tasto destro) per spostare, duplicare ed eliminare; pulsante "+" in fondo all'elenco; nella scheda resta solo "Esporta per Garmin".
12. **v1.2.0**: sezioni **Riscaldamento** e **Defaticamento** in ogni scheda, con proposta automatica in base ai muscoli della scheda, 6 routine pronte e foto animate (34 esercizi con due foto alternate, da free-exercise-db, pubblico dominio). In "Allenati ora" queste sezioni avanzano da sole (5 s di preparazione, poi il conto alla rovescia, doppio bip a metà per gli esercizi "per lato"). Nel `.fit` diventano passi con intensità `warmup` e `cooldown`.

## 4. Struttura del repository

```
/                      sito pubblicato (GitHub Pages): NON modificare a mano, si genera
  index.html           app intera in un solo file (HTML+CSS+JS, FIT SDK, catalogo e logo inclusi)
  sw.js                service worker (cache offline, versione nel nome della cache)
  manifest.webmanifest
  icons/               icone dell'app (formica ANT su rosso)
  img/s/               foto stretching (<id>-0.jpg / <id>-1.jpg), in cache offline
  guida-ANT.pdf        guida utente (12 pagine)
src/                   SORGENTI
  app.template.html    tutto il codice dell'app (segnaposto __LOGO__, __CATALOG__, /*FITSDK*/, __VERSION__)
  build-site.mjs       genera index.html, sw.js, manifest, README nella radice
  build-catalog.mjs    genera catalog-full.json (serve la cartella dati Garmin, vedi §8)
  catalog-full.json    catalogo già generato (esercizi, categorie, muscoli, attrezzi, glossario, stretching, routine)
  it-names.mjs         nomi italiani, categorie IT, muscoli, attrezzi, glossario di ricerca
  stretch-lib.mjs      libreria stretching (nome Garmin ↔ foto ↔ italiano ↔ dinamico ↔ per lato ↔ muscoli) e routine pronte
  entry.js             ingresso per creare fitsdk.min.js con esbuild
  fitsdk.min.js        Garmin FIT SDK per il browser (solo Encoder e Profile)
  check.mjs            legge un .fit con il decoder ufficiale (verifica)
  logo_dark.png        logo per sfondo scuro
guide/                 guida PDF: guida.html, shots/ (schermate), shots.py, make_pdf.py
tests/                 test end-to-end Playwright (Python)
ANT.md                 questo file
```

## 5. Build, prova e rilascio

```bash
cd src && npm ci                      # una volta sola
npm run build:sdk                     # solo se si aggiorna @garmin/fitsdk
node build-site.mjs 1.2.1             # NUOVA versione: rigenera index.html, sw.js, manifest
cd .. && python3 -m http.server 8000  # servire la radice per le prove
python3 tests/test_live.py            # ecc. (variabile ANT_URL, default http://localhost:8000/)
python3 guide/shots.py && python3 guide/make_pdf.py   # se cambia la guida
git add -A && git commit && git push  # Pages si aggiorna in circa 1 minuto
```

- **La versione va sempre alzata**: finisce in `sw.js` (nome della cache `ant-<versione>`), ed è il cambio di `sw.js` che fa comparire agli utenti il banner "Aggiorna". Compare anche in Impostazioni.
- I test usano `page.clock` per far scorrere i timer e verificano anche i file `.fit` esportati (con `check.mjs`).
- `index.html` aperto come file locale funziona, ma senza service worker e senza le foto dello stretching.

## 6. Architettura dell'app

- **Nessun server**: tutto gira nel browser. I dati di ognuno restano sul proprio dispositivo (`localStorage`, chiave `ant-schede-v1`). Il tema scelto si salva anche in `ant-theme`, letto prima del rendering per evitare lampi di colore.
- **Offline**: il service worker mette in cache l'app, le icone, il PDF e le foto (cache-first). I font Google hanno una cache a parte (`ant-fonts`); se mancano, si usa il font di sistema.
- **Aggiornamento**: un nuovo `sw.js` va in attesa e compare il banner; "Aggiorna" invia `skip` e la pagina si ricarica. Al primo avvio non c'è ricarica.
- **Codice**: un solo blocco `{ ... }` in `app.template.html`, senza framework. Lo stato globale è `S`; `render()` smista sulle viste; `commit()` salva e ridisegna. Sezioni del codice (commenti `// ----`): calcoli, render, date, metriche diario, registra allenamento, salvataggio sessione, mappa muscolare, allenamento live, impostazioni, diario, annulla, eventi editor, scelta esercizio, file (export FIT/backup), app installabile.
- **Viste** (`S.view`): `welcome`, `schede`, `log` (registra a mano), `live`, `diario`, `imp` (impostazioni).
- **Annulla**: `snap()` salva una copia dello stato e il toast "Annulla" la ripristina.

## 7. Modello dei dati

```js
S = {
  w: [Scheda], cur: idScheda, log: [Sessione], view, draft, live, cfg, pex, mrange, mute
}
Scheda = { id, name, desc, ex: [Esercizio], warm: [Stretch], cool: [Stretch] }
Esercizio = {
  id, n (nome mostrato), c (categoria FIT) , e (codice esercizio FIT)  // c = null → personalizzato
  pm (maschera muscoli, solo personalizzati), mode: "reps"|"time", same (serie uguali),
  sets: [{ v (rip o secondi), kg }], rest (sec tra serie), restAfter (sec prima del prossimo),
  link (true = in superserie con il successivo)
}
Stretch = { id, n, c, e, sec, side (per lato: tempo × 2) }
Sessione = { id, date "YYYY-MM-DD", wId, wName, note, ex: [{ n, c, e, pm, mode, sets: [{ v, kg, f? (1 facile, 2 giusta, 3 dura) }] }],
  dur?, live?, rpe? (1-10), warm? (n. fatti), cool? }
cfg = { theme: "dark"|"light"|"auto", vol 0-1, vib, cd (bip 3-2-1), wake, rest, restAfter, incUp, incLow }
```

- **Muscoli** (indici, maschera a bit): 0 petto, 1 spalle, 2 bicipiti, 3 tricipiti, 4 avambracci, 5 addominali, 6 obliqui, 7 dorsali, 8 trapezi, 9 lombari, 10 glutei, 11 quadricipiti, 12 femorali, 13 adduttori, 14 abduttori, 15 polpacci, 16 flessori dell'anca.
- **Compatibilità**: ogni versione deve leggere i dati delle precedenti. All'avvio ci sono già migrazioni: `restAfter` mancante = `rest`; `S.view "guida"` → `imp`; sessioni live senza coda vengono ricostruite. Il backup JSON (`v: 3`) contiene `w`, `log`, `cfg`; l'importazione unisce senza cancellare.
- **Superserie**: gruppi di esercizi consecutivi con `link` (`groupsOf`). Le serie del gruppo sono sincronizzate (`syncGroup`). `planSteps(ex)` produce la coda `[esercizio, serie, pausa dopo]` usata sia da "Allenati ora" sia dalla durata stimata.
- **Proposta di carico**: `history(x)` guarda l'ultima sessione dell'esercizio. Se tutte le ripetizioni erano completate e nessuna serie era "dura", propone `+incUp` (parte alta) o `+incLow` (gambe e glutei); si parte comunque dal carico dell'ultima volta finché l'utente non preme **Accetta**.

## 8. Catalogo esercizi e foto

- **Codici**: profilo ufficiale `@garmin/fitsdk` (`Profile.types.<categoria>ExerciseName`). Sono escluse le categorie yoga, pilates, corsa, bici, macchine cardio e gli esercizi in carrozzina.
- **Nomi inglesi, muscoli, attrezzi**: dati Garmin Connect raccolti dal progetto pubblico https://github.com/maximecharriere/GarminExercisesCollector (`examples_garmin_data`). Per rigenerare: clonarlo e lanciare `GARMIN_DATA=<percorso>/examples_garmin_data node build-catalog.mjs` da `src/`.
- **Nomi italiani**: `it-names.mjs` (chiave `categoria.nomeFIT`). `build-catalog` si ferma se una chiave non esiste. Garmin ha un elenco ufficiale di nomi italiani (`connect.garmin.com/web-translations/exercise_types/exercise_types_it.properties`), ma non si scarica in automatico: se Jack lo salva dal suo browser, si possono integrare tutti i nomi ufficiali.
- **Foto stretching**: https://github.com/yuhonas/free-exercise-db (Unlicense, pubblico dominio), ridimensionate a 420 px in `img/s/`. In `stretch-lib.mjs` le foto sono abbinate ai nomi Garmin della categoria `warmUp`; quelle con un compagno sono state scartate. Le altre categorie non hanno animazioni.
- **Non usare** animazioni o contenuti Garmin, Freeletics o di altre app: sono protetti.

## 9. Export Garmin (.fit workout)

- Messaggi: `FILE_ID` (type workout), `WORKOUT` (sport training, subSport strengthTraining), `WORKOUT_STEP`, `EXERCISE_TITLE`.
- Passi: lavoro (`reps` o `time`, peso in kg) e recupero (`time`, intensity `rest`; nessun passo se la pausa è 0). Serie uguali → blocco `repeatUntilStepsCmplt` (`durationValue` = indice del primo passo, `targetValue` = numero di ripetizioni del blocco), seguito dall'ultima serie con la pausa "dopo l'esercizio". Superserie → un giro con tutti gli esercizi, ripetuto. Riscaldamento e defaticamento → passi `time` con intensity `warmup`/`cooldown`.
- Esercizi personalizzati: categoria `65534` (unknown) e numeri progressivi. Per ogni esercizio c'è un `EXERCISE_TITLE` con il nome italiano, perché l'orologio prende il nome da lì (senza, mostra "Go").
- Caricamento: USB → `GARMIN/NewFiles` (su Mac con OpenMTP). L'import di Garmin Connect accetta solo attività, non workout. L'API ufficiale Garmin è riservata alle aziende.

## 10. Interfaccia e design

- Colori: nero, grigi, rosso ANT `#e30d0f`, bianco. Font Saira / Saira Condensed. La barra in alto resta nera in entrambi i temi, per il logo. Tutti i colori sono variabili CSS (`:root` scuro, `:root[data-theme=light]` chiaro); gli SVG usano `style="fill:var(--…)"`.
- In basso, fissi nella vista Schede: **Registra a mano** (contorno rosso) e **Allenati ora** (rosso pieno; diventa "Riprendi allenamento" se ce n'è uno in corso).
- In alto: Schede · Diario · Impostazioni (più "Installa app" su Android).
- Dimensioni: target ≥ 44 px, input a 16 px, deve funzionare da 360 px di larghezza; niente `alert`/`confirm` (le azioni pericolose usano il doppio tocco).
- Suoni con Web Audio (volume da impostazioni). Su iPhone si prova `navigator.audioSession.type = "playback"` per suonare anche con il silenzioso. Wake Lock per tenere lo schermo acceso.

## 11. Da verificare e idee in sospeso

**Da verificare sul campo** (Jack non ha ancora l'adattatore USB-C):
- caricamento del `.fit` sul Venu 4 e comparsa in Forza › Allenamenti;
- nomi in italiano tramite `EXERCISE_TITLE` e animazioni Garmin;
- semantica di `targetValue` nei blocchi ripetuti (numero totale o ripetizioni aggiuntive);
- superserie, riscaldamento e defaticamento sull'orologio;
- allarme su iPhone con il silenzioso attivo.

**Idee discusse e rimandate:**
- **Animazioni per tutti gli esercizi**: rimandate. Jack non era convinto della soluzione mista (foto online + figure stilizzate offline) e vuole prima vedere una prova con le foto free-exercise-db (873 esercizi, copre circa metà del catalogo).
- **Battito cardiaco** (Polar H10 o trasmissione del Venu 4): rimandato. Web Bluetooth funziona su Chrome Android ma non su Safari iOS; nel gruppo ci sono sia iPhone sia Android.
- Import dell'attività registrata dall'orologio (file FIT activity) per riempire il diario in automatico.
- Nomi italiani ufficiali Garmin (serve il file salvato da Jack, vedi §8).
- Proposte fatte ma non ancora scelte: calcolatore dei dischi per lato, serie di riscaldamento escluse da volume e record, rotazione automatica delle schede A/B, riordino delle schede trascinando.
