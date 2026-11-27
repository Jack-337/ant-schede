# Test end-to-end con Playwright. Servire la radice del repo: python3 -m http.server 8000
from playwright.sync_api import sync_playwright
path = __import__("os").environ.get("ANT_URL", "http://localhost:8000/")
with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(path); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(500)
    pg.click("text=Diario"); pg.wait_for_timeout(300); pg.screenshot(path=__import__("tempfile").gettempdir()+"/d0.png")
    pg.click("[data-v=schede]")
    # 3 sessioni via UI con date diverse e carichi crescenti
    for date, kg in [("2026-10-20", "70"), ("2026-11-02", "75"), ("2026-11-12", "80")]:
        pg.click("#lg")
        pg.fill("#ld", date)
        for j in range(4):
            pg.fill(f"input[data-lf=kg][data-i='0'][data-j='{j}']", kg)
        pg.locator("[data-a=ldone]").nth(7).uncheck()
        pg.click("[data-a=lsave]"); pg.wait_for_timeout(300)
        print("toast:", pg.inner_text("#tmsg"))
        pg.click("[data-v=schede]")
    pg.click("[data-v=diario]"); pg.wait_for_timeout(500)
    pg.hover("#pf svg", position={"x": 300, "y": 100}); pg.wait_for_timeout(200)
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/d1.png", full_page=True)
    pg.click("#pex button:nth-child(2)"); pg.wait_for_timeout(300)
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/d2.png")
    m = b.new_page(viewport={"width": 390, "height": 844}); m.on("pageerror", lambda e: errs.append(str(e)))
    st = pg.evaluate("localStorage.getItem('ant-schede-v1')")
    m.goto(path); m.evaluate("s=>localStorage.setItem('ant-schede-v1',s)", st); m.reload(); m.wait_for_timeout(600)
    print("mobile sw", m.evaluate("document.documentElement.scrollWidth"))
    m.screenshot(path=__import__("tempfile").gettempdir()+"/d3.png", full_page=True)
    print("errors", errs); b.close()
