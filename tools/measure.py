"""Dev helper: open screens in headless Chromium at phone sizes, report overflow and save screenshots.

Usage: python tools/measure.py 6.1 3.1 ... [--out DIR] [--size 375x667]
"""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MEASURE_JS = """() => {
  const main = document.querySelector('[data-testid="stMain"]');
  const app = document.querySelector('[data-testid="stAppViewContainer"]');
  const doc = document.scrollingElement;
  const els = [main, app, doc].filter(Boolean);
  const over = Math.max(...els.map(e => e.scrollHeight - e.clientHeight));
  const wide = doc.scrollWidth - doc.clientWidth;
  const block = document.querySelector('[data-testid="stMainBlockContainer"]');
  return {over, wide, content: block ? Math.round(block.getBoundingClientRect().height) : null};
}"""


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@contextmanager
def streamlit_server(env_extra: dict | None = None):
    port = free_port()
    env = {**os.environ, **(env_extra or {})}
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless", "true",
         "--server.port", str(port), "--browser.gatherUsageStats", "false"],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(120):
            try:
                if urllib.request.urlopen(f"{url}/_stcore/health", timeout=1).read() == b"ok":
                    break
            except OSError:
                time.sleep(0.5)
        yield url
    finally:
        proc.terminate()
        proc.wait(timeout=10)


def wait_ready(page, timeout: int = 60000) -> None:
    """Wait until the Streamlit script has finished running and fonts are loaded."""
    page.wait_for_timeout(200)
    page.wait_for_selector('.stApp[data-test-script-state="notRunning"]', timeout=timeout)
    page.wait_for_function("() => document.fonts.status === 'loaded'", timeout=timeout)
    page.wait_for_timeout(700)


def measure(page) -> dict:
    return page.evaluate(MEASURE_JS)


def main() -> None:
    from playwright.sync_api import sync_playwright

    ap = argparse.ArgumentParser()
    ap.add_argument("screens", nargs="+")
    ap.add_argument("--out", default=None)
    ap.add_argument("--size", default="375x667")
    args = ap.parse_args()
    w, hgt = map(int, args.size.split("x"))
    out = Path(args.out) if args.out else None
    if out:
        out.mkdir(parents=True, exist_ok=True)
    with streamlit_server() as url, sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": w, "height": hgt}, device_scale_factor=1)
        for sid in args.screens:
            page.goto(f"{url}/?s={sid}")
            wait_ready(page)
            m = measure(page)
            print(sid, args.size, m)
            if out:
                page.screenshot(path=str(out / f"{sid}_{args.size}.png"))
        browser.close()


if __name__ == "__main__":
    main()
