# Test end-to-end con Playwright: "Salta" chiede conferma, con "Recupera alla fine" e "Salta del tutto".
# Servire la radice del repo: python3 -m http.server 8000
from playwright.sync_api import sync_playwright
path = __import__("os").environ.get("ANT_URL", "http://localhost:8000/")
fails = []
def check(what, ok, got=""):
    print(("OK   " if ok else "FAIL ") + what + (f"  [{got}]" if got else ""))
    if not ok: fails.append(what)
with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    pg = b.new_page(viewport={"width": 390, "height": 844}); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.clock.install()
    pg.goto(path); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
    pg.click("[data-v=schede]"); pg.click("#lv"); pg.wait_for_timeout(200)
    if pg.is_visible("[data-a=sall]"): pg.click("[data-a=sall]")
    head = lambda: pg.inner_text(".lvex span")
    # il pulsante non salta subito: apre il riquadro
    pg.click("[data-a=lask][data-k=set]")
    check("riquadro aperto", pg.is_visible(".ask"), pg.inner_text(".ask b"))
    check("serie non ancora saltata", "serie 1 di 4" in head(), head())
    pg.click("[data-a=lask][data-k='']")
    check("Annulla chiude il riquadro", not pg.is_visible(".ask"))
    # rimanda la serie 1 di squat
    pg.click("[data-a=lask][data-k=set]"); pg.click("[data-a=lskip][data-m=later]")
    check("passa alla serie 2", "serie 2 di 4" in head(), head())
    # rimanda il resto dello squat
    pg.click("[data-a=lask][data-k=ex]")
    check("testo esercizio", "Restano 3 serie" in pg.inner_text(".ask span"), pg.inner_text(".ask span"))
    pg.click("[data-a=lskip][data-m=later]")
    check("passa alla panca", "Panca" in pg.inner_text(".lvex h1"), pg.inner_text(".lvex h1"))
    check("elenco: 4 alla fine", "4 alla fine" in pg.inner_text("[data-a=ljump][data-i='0'] em"))
    # salta del tutto una serie di panca
    pg.click("[data-a=lask][data-k=set]"); pg.click("[data-a=lskip][data-m=skip]")
    check("panca serie 2", "serie 2 di 4" in head(), head())
    # fa tutte le altre serie finché non tornano quelle rimandate
    n = 0
    while n < 30 and not head().startswith("Recupero"):
        pg.click("[data-a=lgo]"); pg.clock.run_for(5000); pg.click("[data-a=ldone]"); n += 1
    check("recupero dopo 12 serie", n == 12 and "Squat" in pg.inner_text(".lvex h1"), f"{n} serie, {head()}")
    check("messaggio di recupero", "rimandate" in pg.inner_text("#tmsg"), pg.inner_text("#tmsg"))
    for _ in range(4):
        pg.click("[data-a=lgo]"); pg.clock.run_for(5000); pg.click("[data-a=ldone]")
    if pg.is_visible("[data-a=sall]"): pg.click("[data-a=sall]")
    check("allenamento concluso", pg.is_visible("[data-a=lsave]"))
    pg.click("[data-a=lsave]"); pg.wait_for_timeout(200)
    log = pg.evaluate("JSON.parse(localStorage.getItem('ant-schede-v1')).log")
    sets = {x["n"]: len(x["sets"]) for x in log[0]["ex"]}
    check("diario: squat 4, panca 3", sets.get("Squat con bilanciere") == 4 and sets.get("Panca piana con bilanciere") == 3, str(sets))
    # Termina con serie rimandate: si può riprendere
    pg.click("[data-v=schede]"); pg.click("#lv"); pg.wait_for_timeout(200)
    if pg.is_visible("[data-a=sall]"): pg.click("[data-a=sall]")
    pg.click("[data-a=lask][data-k=ex]"); pg.click("[data-a=lskip][data-m=later]")
    pg.click("[data-a=lend]")
    check("fine: da recuperare", "4 da recuperare" in pg.inner_text(".stats"), pg.inner_text(".stats").replace("\n", " "))
    check("fine: Riprendi presente", pg.is_visible("[data-a=lresume]"))
    # toccare l'esercizio rimandato nell'elenco lo riprende subito
    pg.click("[data-a=lresume]"); pg.click("[data-a=ljump][data-i='0']")
    check("ripresa dall'elenco", "Squat" in pg.inner_text(".lvex h1") and head().startswith("Recupero"), head())
    check("nessun errore", not errs, str(errs))
    b.close()
print("TUTTO OK" if not fails else f"FALLITI: {fails}")
