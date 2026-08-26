def enrich_company_contacts(company_name: str, known_contacts: dict = None) -> dict:
    if known_contacts and known_contacts.get("hr_contact") and known_contacts.get("tech_contact") and known_contacts.get("ceo_contact"):
        return {
            "hr_contact": known_contacts["hr_contact"],
            "tech_contact": known_contacts["tech_contact"],
            "ceo_contact": known_contacts["ceo_contact"]
        }
    return {
        "hr_contact": f"Talent Acquisition — https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')}/people/?keywords=HR",
        "tech_contact": f"Engineering / Tech Lead — https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')}/people/?keywords=Engineering",
        "ceo_contact": f"Founder / Leadership — https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')}/people"
    }

def generate_cold_outreach_why_fits(company: str, role: str, location: str) -> str:
    return (
        f"Active hiring opening for {role} at {company}'s {location} office. "
        f"Reaching out directly to the Technical Lead with a working code demo or to HR "
        f"with your application reference provides high conversion over public portal queues."
    )
