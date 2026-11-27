# Genera guida-ANT.pdf nella radice del repo da guide/guida.html
import os
from playwright.sync_api import sync_playwright
H=os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto("file://"+os.path.join(H,"guida.html")); pg.wait_for_timeout(800)
    pg.pdf(path=os.path.join(H,"..","guida-ANT.pdf"), format="A4", print_background=True, prefer_css_page_size=True, display_header_footer=True, header_template="<span></span>",
           footer_template='<div style="font-size:8px;color:#888;width:100%;text-align:center">ANT Schede · pagina <span class="pageNumber"></span> di <span class="totalPages"></span></div>')
    b.close()
