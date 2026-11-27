# Test end-to-end con Playwright. Servire la radice del repo: python3 -m http.server 8000
from playwright.sync_api import sync_playwright
path = __import__("os").environ.get("ANT_URL", "http://localhost:8000/")
with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    pg = b.new_page(viewport={"width": 420, "height": 900}); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.clock.install()
    pg.goto(path); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
    pg.click("[data-v=schede]"); pg.click("#lv"); pg.wait_for_timeout(200)
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/l1.png", full_page=True)
    pg.click("[data-a=lgo]"); pg.clock.run_for(23000); pg.wait_for_timeout(100)
    print("work clock:", pg.inner_text("#lvt"))
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/l2.png")
    pg.click("[data-a=ldone]"); pg.clock.run_for(60000); print("rest mid:", pg.inner_text("#lvt"), pg.inner_text("#lvl"))
    pg.clock.run_for(75000); pg.wait_for_timeout(100)
    print("rest over:", pg.inner_text("#lvt"), "|", pg.inner_text("#lvl"), "| over class:", pg.get_attribute("#lvc", "class"))
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/l3.png", full_page=True)
    pg.locator("[data-a=ladj][data-w=prev][data-f=v][data-d='-1']").click()  # corregge serie fatta: 7 rip
    pg.click("[data-a=lgo]"); pg.clock.run_for(20000); pg.click("[data-a=ldone]")
    pg.click("[data-a=lask][data-k=ex]"); pg.click("[data-a=lskip][data-m=skip]")  # salta del tutto il resto dello squat
    print("now:", pg.inner_text(".lvex h1"))
    pg.locator("[data-a=ljump][data-i='4']").click(); print("jumped:", pg.inner_text(".lvex h1"))
    pg.click("[data-a=lgo]"); pg.clock.run_for(50000); print("plank:", pg.inner_text("#lvt"), pg.inner_text("#lvl"))
    pg.click("[data-a=ldone]")
    pg.click("[data-a=lend]"); pg.wait_for_timeout(100)
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/l4.png", full_page=True)
    pg.fill("#lnote", "Test"); pg.click("[data-a=lsave]"); pg.wait_for_timeout(200)
    print("toast:", pg.inner_text("#tmsg"))
    log = pg.evaluate("JSON.parse(localStorage.getItem('ant-schede-v1')).log")
    print("saved:", [(x['n'], [(s['v'], s['kg']) for s in x['sets']]) for x in log[0]['ex']], "dur", log[0]['dur'])
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/l5.png", full_page=True)
    # seconda sessione: suggerimenti
    pg.click("[data-v=schede]"); pg.click("#lv")
    print("hint:", pg.locator(".hint").all_inner_texts(), "| last:", pg.inner_text(".lvex small"))
    print("kg shown:", pg.locator(".ad b").all_inner_texts())
    print("errors", errs); b.close()
