"""
Apollo.io 1-Click Deep-Link & Email Enrichment Engine (Zero API Key Needed)
Generates direct Apollo.io people & verified email search URLs for any target company.
"""

import urllib.parse
from typing import Dict, Any

def generate_apollo_links(company: str, domain: str = None) -> Dict[str, str]:
    """
    Generates 1-click Apollo deep-links for:
    1. People & Verified Emails: Pre-filtered for HR, Talent Acquisition, Engineering Leads, Founders, and CEOs.
    2. Company Overview: Apollo organization intelligence page.
    3. Direct corporate email outreach query.
    """
    clean_company = company.strip()
    encoded_company = urllib.parse.quote(clean_company)
    
    # Apollo filtered people query URL targeting key decision makers
    apollo_people_url = (
        f"https://app.apollo.io/#/people?"
        f"organizationExactNames[]={encoded_company}&"
        f"personTitles[]=Recruiter&personTitles[]=Talent&personTitles[]=HR&"
        f"personTitles[]=Engineering&personTitles[]=Founder&personTitles[]=CEO&personTitles[]=CTO"
    )
    
    # Apollo company intelligence overview URL
    apollo_company_url = (
        f"https://app.apollo.io/#/companies?"
        f"organizationExactNames[]={encoded_company}"
    )

    return {
        "apollo_people_url": apollo_people_url,
        "apollo_company_url": apollo_company_url
    }
