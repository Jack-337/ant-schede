# Rigenera le schermate della guida (tema chiaro, telefono 390x844).
# Prima servire la radice del repo: python3 -m http.server 8000
from playwright.sync_api import sync_playwright
import os
U=os.environ.get("ANT_URL","http://localhost:8000/"); D=os.path.join(os.path.dirname(os.path.abspath(__file__)),"shots")+"/"
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={"width":390,"height":844}, device_scale_factor=2, service_workers="block"); pg=ctx.new_page()
    pg.clock.install(time="2026-11-26T18:00:00")
    pg.goto(U); pg.evaluate("localStorage.clear(); localStorage.setItem('ant-theme','light')"); pg.reload(); pg.wait_for_timeout(400)
    # tema chiaro
    pg.click("[data-a=wgo]"); pg.click("[data-v=imp]"); pg.click("[data-a=cf][data-v=light]"); pg.click("[data-a=welcome]"); pg.wait_for_timeout(200)
    pg.screenshot(path=D+"01-benvenuto.png")
    pg.click("[data-a=wgo]")
    # scheda con superserie
    pg.click("[data-a=link][data-i='2']"); pg.click("[data-a=restAfter][data-v='0'][data-i='2']"); pg.fill("input[data-f=rest][data-i='3']","75")
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(100); pg.screenshot(path=D+"02-scheda.png")
    pg.locator(".sshead").scroll_into_view_if_needed(); pg.evaluate("window.scrollBy(0,-90)"); pg.wait_for_timeout(100); pg.screenshot(path=D+"03-superserie.png")
    # riscaldamento
    pg.click("[data-a=ssug][data-s=warm]"); pg.click("[data-a=ssug][data-s=cool]"); pg.wait_for_timeout(5600)
    pg.locator(".secb.warm").scroll_into_view_if_needed(); pg.evaluate("window.scrollBy(0,-130)"); pg.wait_for_timeout(1300); pg.screenshot(path=D+"14-riscaldamento.png")
    # scelta esercizio
    pg.click("[data-a=add]"); pg.click("#chips [data-g='3']"); pg.click("#eqs [data-q='1']"); pg.wait_for_timeout(100); pg.screenshot(path=D+"04-esercizi.png")
    pg.keyboard.press("Escape")
    # storico per proposta
    pg.click("#lg"); pg.fill("#ld","2026-11-20"); pg.click("[data-a=drpe][data-v='7']"); pg.click("[data-a=lsave]"); pg.wait_for_timeout(300)
    pg.click("[data-v=schede]"); pg.click("#lv"); pg.wait_for_timeout(5600); pg.clock.run_for(7000); pg.wait_for_timeout(1500); pg.screenshot(path=D+"15-stretch-live.png"); pg.click("[data-a=sall]"); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300); pg.screenshot(path=D+"05-proposta.png")
    pg.click("[data-a=pyes]"); pg.click("[data-a=lgo]"); pg.clock.run_for(25000); pg.wait_for_timeout(100); pg.screenshot(path=D+"06-serie.png")
    pg.click("[data-a=ldone]"); pg.clock.run_for(132000); pg.wait_for_timeout(300)
    pg.evaluate("document.body.classList.remove('flash')"); pg.click("[data-a=lfeel][data-v='2']"); pg.clock.run_for(1000); pg.wait_for_timeout(200); pg.evaluate("document.body.classList.remove('flash')")
    pg.screenshot(path=D+"07-recupero.png")
    for _ in range(3):
        pg.click("[data-a=lgo]"); pg.clock.run_for(20000); pg.click("[data-a=ldone]")
    pg.click("[data-a=ljump][data-i='2']")
    for _ in range(4):
        pg.click("[data-a=lgo]"); pg.clock.run_for(20000); pg.click("[data-a=ldone]"); pg.clock.run_for(5000)
    pg.click("[data-a=lend]"); pg.click("[data-a=lrpe][data-v='7']"); pg.wait_for_timeout(200)
    pg.evaluate("document.body.classList.remove('flash')"); pg.screenshot(path=D+"08-fine.png")
    pg.locator(".bm").first.scroll_into_view_if_needed(); pg.evaluate("window.scrollBy(0,-120)"); pg.wait_for_timeout(100); pg.screenshot(path=D+"09-muscoli.png")
    pg.click("[data-a=lsave]"); pg.wait_for_timeout(300); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(5200)
    pg.screenshot(path=D+"10-diario.png")
    pg.locator("#pf").scroll_into_view_if_needed(); pg.evaluate("window.scrollBy(0,-200)"); pg.wait_for_timeout(200); pg.screenshot(path=D+"11-progressi.png")
    pg.click("[data-v=imp]"); pg.wait_for_timeout(200); pg.screenshot(path=D+"12-impostazioni.png")
    pg.click("[data-v=schede]"); pg.wait_for_timeout(100)
    pg.evaluate("document.getElementById('nm').scrollIntoView(); window.scrollBy(0,-20)"); pg.wait_for_timeout(200)
    bb=pg.locator("#nm").bounding_box(); bb2=pg.locator("#st").bounding_box()
    pg.screenshot(path=D+"13-export.png", clip={"x":0,"y":bb["y"]-12,"width":390,"height":bb2["y"]+bb2["height"]-bb["y"]+24})
    b.close()
