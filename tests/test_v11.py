# Test end-to-end con Playwright. Servire la radice del repo: python3 -m http.server 8000
import json
from playwright.sync_api import sync_playwright
U = __import__("os").environ.get("ANT_URL", "http://localhost:8000/")
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]
    pg=b.new_page(viewport={"width":420,"height":900}, accept_downloads=True); pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.clock.install()
    pg.goto(U); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
    pg.click("[data-a=wgo]")
    # collega rematore (3) e lento (4) in superserie
    pg.click("[data-a=link][data-i='2']"); pg.wait_for_timeout(100)
    print("sshead:", pg.inner_text(".sshead"))
    # pausa verso il prossimo nel circuito = 0, recupero tra i giri 75
    pg.click("[data-a=restAfter][data-v='0'][data-i='2']")
    pg.fill("input[data-f=rest][data-i='3']", "75")
    pg.locator("[data-a=sp][data-i='3']").click()
    print("sets synced:", pg.evaluate("JSON.parse(localStorage.getItem('ant-schede-v1')).w[0].ex.map(x=>x.sets.length)"))
    with pg.expect_download() as d: pg.click("[data-a=exp]")
    d.value.save_as(__import__("tempfile").gettempdir()+"/v11.fit")
    # cronologia per proposta: registra a mano squat completo
    pg.click("#lg"); pg.fill("#ld","2026-11-20"); pg.click("[data-a=drpe][data-v='7']"); pg.click("[data-a=lsave]"); pg.wait_for_timeout(200)
    pg.click("[data-v=schede]")
    pg.click("#lv"); pg.wait_for_timeout(200)
    print("proposal:", pg.inner_text(".prop b") if pg.is_visible(".prop") else None, "| kg:", pg.locator(".ad b").all_inner_texts())
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/v_prop.png", full_page=True)
    pg.click("[data-a=pyes]"); print("after accept:", pg.locator(".ad b").all_inner_texts(), pg.locator(".hint").all_inner_texts())
    pg.click("[data-a=lgo]"); pg.clock.run_for(20000); pg.click("[data-a=ldone]")
    print("rest label:", pg.inner_text("#lvl"), pg.inner_text("#lvt"))
    pg.click("[data-a=lfeel][data-v='3']"); pg.screenshot(path=__import__("tempfile").gettempdir()+"/v_rest.png", full_page=True)
    # salta squat restante, salta panca -> arriva alla superserie
    for _ in range(2): pg.click("[data-a=lask][data-k=ex]"); pg.click("[data-a=lskip][data-m=skip]")
    print("ss head:", pg.inner_text(".lvex span"))
    pg.click("[data-a=lgo]"); pg.clock.run_for(15000); pg.click("[data-a=ldone]")
    print("after A:", pg.evaluate("document.body.dataset.view"), pg.evaluate("JSON.parse(localStorage.getItem('ant-schede-v1')).live.phase"), pg.inner_text(".lvex h1"), "|", pg.inner_text(".lvex span"))
    pg.click("[data-a=lgo]"); pg.clock.run_for(15000); pg.click("[data-a=ldone]")
    print("after B:", pg.evaluate("JSON.parse(localStorage.getItem('ant-schede-v1')).live.phase"), pg.inner_text("#lvl") if pg.is_visible("#lvl") else "", pg.evaluate("JSON.parse(localStorage.getItem('ant-schede-v1')).live.restDur"), pg.inner_text(".lvex h1"))
    pg.click("[data-a=lend]"); pg.click("[data-a=lrpe][data-v='8']"); pg.screenshot(path=__import__("tempfile").gettempdir()+"/v_end.png", full_page=True)
    pg.click("[data-a=lsave]"); pg.wait_for_timeout(200)
    log=pg.evaluate("JSON.parse(localStorage.getItem('ant-schede-v1')).log")
    print("saved rpe:", [l.get('rpe') for l in log], "feel:", [s.get('f') for s in log[-1]['ex'][0]['sets']])
    pg.locator(".sess summary").first.click(); pg.screenshot(path=__import__("tempfile").gettempdir()+"/v_diary.png", full_page=True)
    # tema chiaro sul diario
    pg.click("[data-v=imp]"); pg.click("[data-a=cf][data-v=light]"); pg.click("[data-v=diario]"); pg.wait_for_timeout(300); pg.screenshot(path=__import__("tempfile").gettempdir()+"/v_diary_l.png", full_page=True)
    print("errors", errs); b.close()
