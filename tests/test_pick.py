# Test end-to-end con Playwright. Servire la radice del repo: python3 -m http.server 8000
from playwright.sync_api import sync_playwright
path = __import__("os").environ.get("ANT_URL", "http://localhost:8000/")
with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    pg = b.new_page(viewport={"width": 1280, "height": 900}); pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(path); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(500)
    pg.click("[data-v=schede]")
    print([t[:60] for t in pg.locator(".name small").all_inner_texts()][:3])
    pg.click("[data-a=add]"); print("all:", pg.inner_text("#cnt"))
    for q in ["panca inclinata manubri", "rematore", "leg extension", "alzate laterali", "hip thrust", "trazioni"]:
        pg.fill("#q", q); print(q, "->", pg.inner_text("#cnt"), "|", " / ".join(pg.locator("#lst button").all_inner_texts()[:4]).replace("\n"," "))
    pg.fill("#q", ""); pg.click("#chips [data-g='3']"); pg.click("#eqs [data-q='1']"); print("petto+manubri", pg.inner_text("#cnt"))
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/p1.png")
    pg.click("#chips [data-g='0']"); pg.click("#eqs [data-q='-1']"); pg.fill("#q", "plank laterale"); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    print("last:", pg.locator(".name").last.inner_text().replace("\n"," | "), pg.locator(".seg button.on").last.inner_text())
    pg.click("[data-a=add]"); pg.fill("#q", "Chest press macchina"); pg.keyboard.press("Enter")
    pg.locator("[data-a=pm][data-m='0']").last.click(); pg.wait_for_timeout(100)
    print("custom pm:", pg.evaluate("JSON.parse(localStorage.getItem('ant-schede-v1')).w[0].ex.slice(-1)[0].pm"))
    pg.click("[data-a=add]"); pg.click("#chips [data-g='1']"); print("le mie:", pg.inner_text("#cnt"), len(pg.locator("#lst button").all()))
    print("errors", errs); b.close()
