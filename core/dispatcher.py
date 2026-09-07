import json
import os
import sys
import time
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any, List

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dispatched_leads.json")

def is_telegram_configured(bot_token: str, chat_id: str) -> bool:
    if not bot_token or not chat_id:
        return False
    if "YOUR_BOT_TOKEN" in bot_token or "YOUR_CHAT_ID" in chat_id:
        return False
    return True

def print_telegram_setup_guide():
    print("\n" + "-"*65)
    print("ℹ️  TELEGRAM NOT CONFIGURED (Running in Console Mode)")
    print("-"*65)
    print("All verified job leads will be printed directly to this terminal.")
    print("\nTo enable instant push notifications to your Telegram phone app:")
    print("  1. Open Telegram and message @BotFather -> send '/newbot' to get your BOT_TOKEN.")
    print("  2. Message @userinfobot -> copy your Id number as your CHAT_ID.")
    print("  3. Paste them into 'config.json' under the 'telegram' section.")
    print("-"*65 + "\n")

def load_dispatched_leads() -> List[Dict[str, Any]]:
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def clear_dispatched_cache():
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
            print("[INFO] Cleared dispatched leads cache.")
        except Exception as e:
            print(f"[WARNING] Could not clear cache: {e}")

def save_dispatched_lead(lead: Dict[str, Any]):
    leads = load_dispatched_leads()
    leads.append(lead)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

def is_duplicate(company: str, role: str) -> bool:
    leads = load_dispatched_leads()
    c_norm = company.strip().lower()
    r_norm = role.strip().lower()
    for l in leads:
        if l.get("company", "").strip().lower() == c_norm and l.get("role", "").strip().lower() == r_norm:
            return True
    return False

def send_telegram_message(bot_token: str, chat_id: str, text: str, parse_mode: Optional[str] = None) -> bool:
    if not is_telegram_configured(bot_token, chat_id):
        return False
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
        
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[ERROR] Error sending to Telegram: {e}")
        if parse_mode:
            try:
                payload.pop("parse_mode")
                data = urllib.parse.urlencode(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data)
                with urllib.request.urlopen(req) as resp:
                    return resp.status == 200
            except Exception as e2:
                print(f"[ERROR] Fallback error: {e2}")
        return False

def format_lead_message(
    company: str,
    role: str,
    location: str,
    paid_status: str,
    apply_url: str,
    hr_contact: str,
    tech_contact: str,
    ceo_contact: str,
    why_fits: str,
    apollo_people_url: Optional[str] = None,
    apollo_company_url: Optional[str] = None
) -> str:
    apollo_block = ""
    if apollo_people_url:
        apollo_block = (
            f"\n🚀 Apollo.io 1-Click Emails:\n"
            f"• Verified Decision-Makers & Emails: {apollo_people_url}\n"
        )
        if apollo_company_url:
            apollo_block += f"• Company Overview: {apollo_company_url}\n"

    msg = (
        f"🎯 {company}\n"
        f"Role: {role} ({location})\n"
        f"Paid: {paid_status}\n"
        f"Apply: {apply_url}\n\n"
        f"Contacts & Verified LinkedIn:\n"
        f"• 👤 HR / Talent: {hr_contact}\n"
        f"• 💻 Engineering / AI Lead: {tech_contact}\n"
        f"• 👔 Founder / CEO: {ceo_contact}\n"
        f"{apollo_block}\n"
        f"Why it fits: {why_fits}"
    )
    return msg

def dispatch_lead(
    bot_token: str,
    chat_id: str,
    company: str,
    role: str,
    location: str,
    paid_status: str,
    apply_url: str,
    hr_contact: str,
    tech_contact: str,
    ceo_contact: str,
    why_fits: str,
    dry_run: bool = False,
    allow_duplicate: bool = False,
    apollo_people_url: Optional[str] = None,
    apollo_company_url: Optional[str] = None
) -> bool:
    if not allow_duplicate and is_duplicate(company, role):
        print(f"[SKIP DUPLICATE] Already logged/sent: {company} - {role}")
        return False

    message = format_lead_message(
        company, role, location, paid_status, apply_url,
        hr_contact, tech_contact, ceo_contact, why_fits,
        apollo_people_url=apollo_people_url,
        apollo_company_url=apollo_company_url
    )

    telegram_ready = is_telegram_configured(bot_token, chat_id) and not dry_run

    if telegram_ready:
        success = send_telegram_message(bot_token, chat_id, message)
        if success:
            print(f"[DISPATCHED TO TELEGRAM] {company} - {role}")
        else:
            print(f"[FALLBACK TO CONSOLE] {company} - {role}")
            print("\n" + message + "\n")
    else:
        # Console display mode
        print("\n" + "="*60)
        print(message)
        print("="*60 + "\n")

    # Record to local database
    lead_data = {
        "company": company,
        "role": role,
        "location": location,
        "paid_status": paid_status,
        "apply_url": apply_url,
        "hr_contact": hr_contact,
        "tech_contact": tech_contact,
        "ceo_contact": ceo_contact,
        "why_fits": why_fits,
        "timestamp": time.time()
    }
    save_dispatched_lead(lead_data)
    return True
