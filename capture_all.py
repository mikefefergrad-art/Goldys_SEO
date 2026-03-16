from playwright.sync_api import sync_playwright
import json
import time

URL = "https://goldys.ca"
OUTPUT_DIR = "/home/user/Goldys_SEO/screenshots"

viewports = [
    {"name": "desktop",  "width": 1920, "height": 1080},
    {"name": "laptop",   "width": 1366, "height": 768},
    {"name": "tablet",   "width": 768,  "height": 1024},
    {"name": "mobile",   "width": 375,  "height": 812},
]

def capture(page, url, path, width, height, full_page=False):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(url, wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.screenshot(path=path, full_page=full_page)
    print(f"Saved: {path}")

def collect_data(page):
    data = page.evaluate("""() => {
        const h1s = Array.from(document.querySelectorAll('h1')).map(el => ({
            text: el.innerText.trim(),
            visible: el.getBoundingClientRect().top < window.innerHeight
        }));
        const ctaButtons = Array.from(document.querySelectorAll('a, button')).filter(el => {
            const txt = el.innerText.toLowerCase();
            return txt.includes('shop') || txt.includes('buy') || txt.includes('order') ||
                   txt.includes('cart') || txt.includes('add') || txt.includes('get') ||
                   txt.includes('try') || txt.includes('learn');
        }).map(el => {
            const rect = el.getBoundingClientRect();
            return {
                text: el.innerText.trim().substring(0, 60),
                tag: el.tagName,
                aboveFold: rect.top < window.innerHeight && rect.top >= 0,
                top: Math.round(rect.top),
                width: Math.round(rect.width),
                height: Math.round(rect.height),
                tooSmall: rect.width < 48 || rect.height < 48
            };
        }).slice(0, 20);
        const images = Array.from(document.querySelectorAll('img')).map(el => ({
            src: el.src.substring(0, 80),
            alt: el.alt,
            hasAlt: el.alt && el.alt.trim().length > 0,
            loading: el.loading,
            width: el.naturalWidth,
            height: el.naturalHeight,
            renderedWidth: el.getBoundingClientRect().width,
            aboveFold: el.getBoundingClientRect().top < window.innerHeight
        })).slice(0, 30);
        const fonts = Array.from(document.querySelectorAll('p, span, li, a')).slice(0, 5).map(el => {
            const style = window.getComputedStyle(el);
            return {
                tag: el.tagName,
                fontSize: style.fontSize,
                lineHeight: style.lineHeight,
                color: style.color,
                bgColor: style.backgroundColor
            };
        });
        const metaViewport = document.querySelector('meta[name="viewport"]');
        const hasHorizontalScroll = document.body.scrollWidth > window.innerWidth;
        return {
            h1s,
            ctaButtons,
            images,
            fonts,
            metaViewport: metaViewport ? metaViewport.getAttribute('content') : null,
            hasHorizontalScroll,
            pageTitle: document.title,
            bodyScrollWidth: document.body.scrollWidth,
            windowInnerWidth: window.innerWidth
        };
    }""")
    return data

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Capture above-the-fold for all viewports
    for vp in viewports:
        page = browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
        path_atf = f"{OUTPUT_DIR}/{vp['name']}_atf.png"
        capture(page, URL, path_atf, vp["width"], vp["height"], full_page=False)

        if vp["name"] == "mobile":
            path_full = f"{OUTPUT_DIR}/{vp['name']}_full.png"
            capture(page, URL, path_full, vp["width"], vp["height"], full_page=True)
            mobile_data = collect_data(page)
            with open(f"{OUTPUT_DIR}/mobile_data.json", "w") as f:
                json.dump(mobile_data, f, indent=2)

        if vp["name"] == "desktop":
            path_full = f"{OUTPUT_DIR}/{vp['name']}_full.png"
            capture(page, URL, path_full, vp["width"], vp["height"], full_page=True)
            desktop_data = collect_data(page)
            with open(f"{OUTPUT_DIR}/desktop_data.json", "w") as f:
                json.dump(desktop_data, f, indent=2)

        page.close()

    browser.close()
    print("All captures complete.")
