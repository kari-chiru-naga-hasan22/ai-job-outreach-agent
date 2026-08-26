import sys
import os
import webbrowser
import threading
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def open_browser(url: str):
    time.sleep(1.5)
    print(f"\n🌐 Opening web browser at {url} ...")
    webbrowser.open(url)

def main():
    backend_dir = os.path.join(os.path.dirname(__file__), "web", "backend")
    sys.path.insert(0, backend_dir)
    os.chdir(backend_dir)

    port = int(os.getenv("PORT", 8000))
    app_url = f"http://localhost:{port}"

    print("="*65)
    print("🚀 UNIVERSAL JOB & INTERNSHIP FINDER — WEB APPLICATION")
    print("="*65)
    print(f"📍 Location Enforced : Any / Hyderabad (Embedded, PCB, AI, VLSI, Software)")
    print(f"🧠 OpenRouter Model  : {os.getenv('OPENROUTER_MODEL_ID', 'meta-llama/llama-3.3-70b-instruct')}")
    print(f"🖥️  Web Server URL    : {app_url}")
    print("="*65 + "\n")

    threading.Thread(target=open_browser, args=(app_url,), daemon=True).start()

    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)

if __name__ == "__main__":
    main()
