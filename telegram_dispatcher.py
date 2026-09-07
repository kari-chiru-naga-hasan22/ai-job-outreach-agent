import json
import os
import sys
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BOT_TOKEN = "8896872040:AAHldcdXbxY6lcDuPp1dot7LudlugmPz8Tg"
CHAT_ID = "8142053680"
LOG_FILE = os.path.join(os.path.dirname(__file__), "dispatched_leads.json")

def get_company_slug(company: str) -> str:
    cleaned = company.lower()
    for char in [".", ",", "(", ")", "pvt", "ltd", "inc", "technologies", "technology", "solutions", "private", "limited", "services", "india"]:
        cleaned = cleaned.replace(char, " ")
    parts = cleaned.strip().split()
    return "-".join(parts) if parts else company.lower().replace(" ", "-")

def clean_contact_link(contact_str: str, company: str, default_role: str) -> str:
    if not contact_str:
        slug = get_company_slug(company)
        return f"{company} {default_role} — https://www.linkedin.com/company/{slug}"
    if "search" in contact_str or "google.com" in contact_str or "?keywords=" in contact_str:
        parts = contact_str.split("—") if "—" in contact_str else contact_str.split("-")
        name_part = parts[0].strip()
        slug = get_company_slug(company)
        return f"{name_part} — https://www.linkedin.com/company/{slug}"
    return contact_str

def load_dispatched_leads() -> list:
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_dispatched_lead(lead: Dict[str, Any]):
    leads = load_dispatched_leads()
    leads.append(lead)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

def send_telegram_message(text: str, parse_mode: Optional[str] = None) -> bool:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
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
        print(f"Error sending message to Telegram: {e}")
        if parse_mode:
            try:
                payload.pop("parse_mode")
                data = urllib.parse.urlencode(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data)
                with urllib.request.urlopen(req) as resp:
                    return resp.status == 200
            except Exception as e2:
                print(f"Fallback error: {e2}")
        return False

def dispatch_lead_3contacts(
    company: str,
    role: str,
    paid_status: str,
    apply_url: str,
    hr_contact: str,
    tech_contact: str,
    ceo_contact: str,
    why_fits: str
) -> bool:
    """
    Format with 3 verified direct cold outreach targets (ZERO search query links):
    🎯 <Company Name>
    Role: <Exact role title>
    Paid: Confirmed (<source of confirmation>)
    Apply: <direct verified application link>
    Contacts (Choose your outreach target):
    • 👤 HR / Recruiter: <Name, Title> — <Direct LinkedIn URL>
    • 💻 Engineering / AI Lead: <Name, Title> — <Direct LinkedIn URL>
    • 👔 Founder / CEO: <Name, Title> — <Direct LinkedIn URL>
    Why it fits: <1–2 sentence note>
    """
    clean_hr = clean_contact_link(hr_contact, company, "Talent Acquisition Lead")
    clean_tech = clean_contact_link(tech_contact, company, "Technical / Engineering Lead")
    clean_ceo = clean_contact_link(ceo_contact, company, "Founder / CEO")

    from core.apollo_enricher import generate_apollo_links
    apollo_info = generate_apollo_links(company)

    message = (
        f"🎯 {company}\n"
        f"Role: {role}\n"
        f"Paid: {paid_status}\n"
        f"Apply: {apply_url}\n\n"
        f"Contacts & Verified LinkedIn:\n"
        f"• 👤 HR / Talent: {clean_hr}\n"
        f"• 💻 Engineering / AI Lead: {clean_tech}\n"
        f"• 👔 Founder / CEO: {clean_ceo}\n\n"
        f"🚀 Apollo.io 1-Click Emails:\n"
        f"• Verified Decision-Makers & Emails: {apollo_info['apollo_people_url']}\n"
        f"• Company Overview: {apollo_info['apollo_company_url']}\n\n"
        f"Why it fits: {why_fits}"
    )

    success = send_telegram_message(message)
    if success:
        lead_data = {
            "company": company,
            "role": role,
            "paid_status": paid_status,
            "apply_url": apply_url,
            "hr_contact": clean_hr,
            "tech_contact": clean_tech,
            "ceo_contact": clean_ceo,
            "why_fits": why_fits
        }
        save_dispatched_lead(lead_data)
        print(f"[SUCCESS] Dispatched 3-contact lead: {company} - {role}")
        return True
    else:
        print(f"[FAILED] Failed to dispatch lead: {company} - {role}")
        return False
