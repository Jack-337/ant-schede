# Test end-to-end con Playwright. Servire la radice del repo: python3 -m http.server 8000
import sys
from playwright.sync_api import sync_playwright

path = __import__("os").environ.get("ANT_URL", "http://localhost:8000/")
with sync_playwright() as p:
    b = p.chromium.launch()
    errs = []
    pg = b.new_page(viewport={"width": 1280, "height": 900}, accept_downloads=True)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.goto(path)
    pg.wait_for_timeout(1200); pg.click("[data-v=schede]")
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/s1.png", full_page=True)
    # aggiungi esercizio personalizzato
    pg.click("[data-a=add]")
    pg.fill("#q", "Leg extension")
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/s2.png")
    pg.keyboard.press("Enter")
    # serie diverse sul primo esercizio
    pg.locator("[data-a=same]").first.check()
    pg.locator("input[data-f=kg][data-i='0'][data-j='3']").fill("90")
    pg.locator("input[data-f=v][data-i='0'][data-j='3']").fill("5")
    with pg.expect_download() as d:
        pg.click("[data-a=exp]")
    d.value.save_as(__import__("tempfile").gettempdir()+"/app_export.fit")
    print("download:", d.value.suggested_filename)
    pg.screenshot(path=__import__("tempfile").gettempdir()+"/s3.png", full_page=True)
    m = b.new_page(viewport={"width": 390, "height": 844})
    m.on("pageerror", lambda e: errs.append(str(e)))
    m.goto(path); m.wait_for_timeout(800)
    sw = m.evaluate("document.documentElement.scrollWidth")
    print("mobile scrollWidth", sw)
    m.screenshot(path=__import__("tempfile").gettempdir()+"/s4.png", full_page=True)
    print("errors:", errs)
    b.close()
