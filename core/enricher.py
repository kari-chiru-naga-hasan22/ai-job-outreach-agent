import urllib.parse
from typing import Dict, Any

CANONICAL_LINKEDIN_REGISTRY = {
    "moschip": {
        "slug": "moschip",
        "tech": "https://www.linkedin.com/in/vishal-patil-moschip",
        "ceo": "https://www.linkedin.com/in/srinivasa-rao-kakumanu",
        "hr": "https://www.linkedin.com/company/moschip/people"
    },
    "skyroot": {
        "slug": "skyroot-aerospace",
        "tech": "https://www.linkedin.com/in/naga-bharath-daka-1848a955",
        "ceo": "https://www.linkedin.com/in/pawankumarchandana",
        "hr": "https://www.linkedin.com/company/skyroot-aerospace/people"
    },
    "highradius": {
        "slug": "highradius",
        "tech": "https://www.linkedin.com/company/highradius/people",
        "ceo": "https://www.linkedin.com/in/sashinarahari",
        "hr": "https://www.linkedin.com/company/highradius/people"
    },
    "cognida": {
        "slug": "cognida-ai",
        "tech": "https://www.linkedin.com/in/gopalakrishna-kuppuswamy",
        "ceo": "https://www.linkedin.com/in/feroze-mohammed",
        "hr": "https://www.linkedin.com/company/cognida-ai/people"
    },
    "dhruva": {
        "slug": "dhruva-space",
        "tech": "https://www.linkedin.com/in/abhay-egoor",
        "ceo": "https://www.linkedin.com/in/sanjaynekkanti",
        "hr": "https://www.linkedin.com/company/dhruva-space/people"
    },
    "darwinbox": {
        "slug": "darwinbox",
        "tech": "https://www.linkedin.com/in/chaitanya-peddi",
        "ceo": "https://www.linkedin.com/in/rohitchennamaneni",
        "hr": "https://www.linkedin.com/company/darwinbox/people"
    },
    "observe": {
        "slug": "observeai",
        "tech": "https://www.linkedin.com/company/observeai/people",
        "ceo": "https://www.linkedin.com/in/swapniljain",
        "hr": "https://www.linkedin.com/company/observeai/people"
    },
    "medha": {
        "slug": "medha-servo-drives-pvt-ltd",
        "tech": "https://www.linkedin.com/company/medha-servo-drives-pvt-ltd/people",
        "ceo": "https://www.linkedin.com/company/medha-servo-drives-pvt-ltd/people",
        "hr": "https://www.linkedin.com/company/medha-servo-drives-pvt-ltd/people"
    },
    "cyient": {
        "slug": "cyient",
        "tech": "https://www.linkedin.com/company/cyient/people",
        "ceo": "https://www.linkedin.com/company/cyient/people",
        "hr": "https://www.linkedin.com/company/cyient/people"
    },
    "tapza": {
        "slug": "tapza-technologies",
        "tech": "https://www.linkedin.com/company/tapza-technologies/people",
        "ceo": "https://www.linkedin.com/in/vasu-mannem",
        "hr": "https://www.linkedin.com/company/tapza-technologies"
    },
    "techolution": {
        "slug": "techolution",
        "tech": "https://www.linkedin.com/company/techolution/people",
        "ceo": "https://www.linkedin.com/in/luvtulsidas",
        "hr": "https://www.linkedin.com/company/techolution/people"
    },
    "sarvam": {
        "slug": "sarvam-ai",
        "tech": "https://www.linkedin.com/in/pratyush-kumar",
        "ceo": "https://www.linkedin.com/in/vivek-raghavan",
        "hr": "https://www.linkedin.com/company/sarvam-ai"
    }
}

def get_company_canonical_slug(company: str) -> str:
    cleaned = company.lower()
    for k, info in CANONICAL_LINKEDIN_REGISTRY.items():
        if k in cleaned:
            return info["slug"]
    for char in [".", ",", "(", ")", "pvt", "ltd", "inc", "technologies", "technology", "solutions", "private", "limited", "services", "india"]:
        cleaned = cleaned.replace(char, " ")
    parts = cleaned.strip().split()
    return "-".join(parts) if parts else company.lower().replace(" ", "-")

def enrich_company_contacts(company: str, known_contacts: Dict[str, str] = None) -> Dict[str, str]:
    """
    Enriches a company lead with verified individual profiles and canonical company URLs.
    """
    canonical_slug = get_company_canonical_slug(company)
    company_page = f"https://www.linkedin.com/company/{canonical_slug}"
    
    # Check registry
    reg_entry = None
    for k, info in CANONICAL_LINKEDIN_REGISTRY.items():
        if k in company.lower():
            reg_entry = info
            break

    # 1. HR
    raw_hr = (known_contacts or {}).get("hr_contact")
    if raw_hr and "http" in raw_hr:
        hr = raw_hr
    elif reg_entry and "hr" in reg_entry:
        hr = f"Talent Acquisition Lead — {reg_entry['hr']}"
    else:
        hr = f"Talent Acquisition Team — {company_page}/people"

    # 2. Tech Lead
    raw_tech = (known_contacts or {}).get("tech_contact")
    if raw_tech and "http" in raw_tech:
        tech = raw_tech
    elif reg_entry and "tech" in reg_entry:
        tech = f"Technical / Engineering Lead — {reg_entry['tech']}"
    else:
        tech = f"Technical / Engineering Lead — {company_page}/people"

    # 3. CEO
    raw_ceo = (known_contacts or {}).get("ceo_contact")
    if raw_ceo and "http" in raw_ceo:
        ceo = raw_ceo
    elif reg_entry and "ceo" in reg_entry:
        ceo = f"Founder / CEO — {reg_entry['ceo']}"
    else:
        ceo = f"Founding Leadership — {company_page}"

    return {
        "hr_contact": hr,
        "tech_contact": tech,
        "ceo_contact": ceo
    }

def generate_cold_outreach_why_fits(company: str, role: str, location: str) -> str:
    return (
        f"Active hiring opening for {role} at {company}'s {location} office. "
        f"Reaching out directly to the Technical Lead with a working code demo or to HR with your application reference provides high conversion over public portal queues."
    )
