import os
import subprocess
import time
import signal
from playwright.sync_api import sync_playwright, expect

CHAT_URL = "http://localhost:5500"

def test_chat_response():
    # 1️⃣ Start the web app
    server = subprocess.Popen(
        ["./start.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=None  # remove on Windows
    )

    try:
        # 2️⃣ Give the server time to boot
        time.sleep(5)  # adjust if needed

        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=False, slow_mo=1500)
            page = browser.new_page()

            page.goto(CHAT_URL)
        
            chat_input = page.locator("#input")
            #chat_input.wait_for(state="visible", timeout=15000)

            chat_input.type("Hola puedes hacer la 1", delay=100)
            chat_input.press("Enter")

            system_messages = page.locator(".message.system")
            expect(system_messages).to_have_count(1, timeout=20000)

            response = system_messages.first.inner_text()
            assert response.strip() != ""

            chat_input.type("2026-02-15", delay=100)
            chat_input.press("Enter")
            system_messages = page.locator(".message.system")
            expect(system_messages).to_have_count(1, timeout=20000)
            response = system_messages.first.inner_text()
            assert response.strip() != ""

            browser.close()
            

            print("Test passed: Chat responded successfully.")
            browser.close()
        
    finally:
        # 3️⃣ Kill the server
        os.system("pkill -f 'uvicorn backend.main:app'")
        os.system("pkill -f 'python3 -m http.server'")
        server.terminate()
        server.wait()
