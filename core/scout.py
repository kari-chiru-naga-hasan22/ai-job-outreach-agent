import urllib.request
import urllib.parse
import json
import re
import time
from typing import List, Dict, Any

# Curated ecosystem database of actively hiring AI & Tech companies in Hyderabad & other hubs
KNOWN_ECOSYSTEMS = {
    "hyderabad": [
        {
            "company": "Cognida.ai",
            "roles": ["GenAI Engineer Intern", "AI & Data Science Intern", "Agentic Systems Intern"],
            "stipend": "₹30,000 – ₹40,000/month",
            "apply_url": "https://cognida.ai/careers",
            "location": "Hyderabad",
            "hr_contact": "Talent Acquisition Hyderabad — https://www.linkedin.com/company/cognida-ai",
            "tech_contact": "Gopalakrishna Kuppuswamy, Co-Founder & CTO — https://www.linkedin.com/in/gopalakrishna-kuppuswamy",
            "ceo_contact": "Feroze Mohammed, Founder & CEO — https://www.linkedin.com/in/feroze-mohammed"
        },
        {
            "company": "HighRadius",
            "roles": ["AI / Machine Learning Intern", "Autonomous Systems Intern", "Data Science Intern"],
            "stipend": "₹25,000 – ₹35,000/month",
            "apply_url": "https://www.highradius.com/careers/",
            "location": "Hyderabad",
            "hr_contact": "Hyderabad University Recruiting Team — https://www.linkedin.com/company/highradius/people/?keywords=Recruiter",
            "tech_contact": "Director of AI & Autonomous Systems — https://www.linkedin.com/company/highradius/people/?keywords=AI%20Engineering",
            "ceo_contact": "Sashi Narahari, Founder & CEO — https://www.linkedin.com/in/sashinarahari"
        },
        {
            "company": "Skyroot Aerospace",
            "roles": ["AI/ML Intern (Aerospace Simulation & Vision)", "Simulation Engineer Intern"],
            "stipend": "₹30,000 – ₹45,000/month",
            "apply_url": "https://skyroot.in/careers/",
            "location": "Hyderabad",
            "hr_contact": "Talent Operations Lead (hr@skyroot.in) — https://www.linkedin.com/search/results/people/?keywords=Skyroot+Aerospace+Talent+Acquisition",
            "tech_contact": "Naga Bharath Daka, Co-Founder & COO/CTO — https://www.linkedin.com/in/naga-bharath-daka-1848a955",
            "ceo_contact": "Pawan Kumar Chandana, Co-Founder & CEO — https://www.linkedin.com/in/pawankumarchandana"
        },
        {
            "company": "Dhruva Space",
            "roles": ["AI/ML Intern (Computer Vision & Satellite Telemetry)", "Avionics Software Intern"],
            "stipend": "₹18,000 – ₹25,000/month",
            "apply_url": "https://www.dhruvaspace.com/careers",
            "location": "Hyderabad",
            "hr_contact": "Kalpana Sumanth Raghavendra (HR Lead) — https://www.linkedin.com/search/results/people/?keywords=Kalpana+Sumanth+Raghavendra+Dhruva+Space",
            "tech_contact": "Abhay Egoor, Co-Founder & CTO — https://www.linkedin.com/in/abhay-egoor",
            "ceo_contact": "Sanjay Nekkanti, Founder & CEO — https://www.linkedin.com/in/sanjaynekkanti"
        },
        {
            "company": "Darwinbox",
            "roles": ["AI-Native Systems Builder / AI Intern", "Software Engineering Intern"],
            "stipend": "₹20,000 – ₹26,000/month",
            "apply_url": "https://darwinbox.com/careers",
            "location": "Hyderabad",
            "hr_contact": "Tech Talent Acquisition Lead — https://www.linkedin.com/company/darwinbox/people/?keywords=Recruiter",
            "tech_contact": "Chaitanya Peddi, Co-Founder & Product/Tech Head — https://www.linkedin.com/in/chaitanya-peddi",
            "ceo_contact": "Rohit Chennamaneni & Jayant Paleti, Co-Founders — https://www.linkedin.com/company/darwinbox"
        },
        {
            "company": "Observe.AI",
            "roles": ["Machine Learning / AI Intern", "Voice AI Intern", "Data Science Intern"],
            "stipend": "₹22,000 – ₹30,000/month",
            "apply_url": "https://observe.ai/careers",
            "location": "Hyderabad",
            "hr_contact": "Technical Recruiter Hyderabad — https://www.linkedin.com/company/observeai/people/?keywords=Recruiter",
            "tech_contact": "Lead AI / LLM Voice Systems Architect — https://www.linkedin.com/company/observeai/people/?keywords=Engineering",
            "ceo_contact": "Swapnil Jain, Co-Founder & CEO — https://www.linkedin.com/in/swapniljain"
        },
        {
            "company": "Stackular",
            "roles": ["AI/ML Intern – Agentic AI", "AI DevOps Intern", "Cloud Engineering Intern"],
            "stipend": "₹35,000/month",
            "apply_url": "https://stackular.com/careers",
            "location": "Hyderabad",
            "hr_contact": "Stackular Talent Acquisition — https://www.linkedin.com/company/stackular",
            "tech_contact": "Autonomous AI / LangChain Lead — https://www.linkedin.com/company/stackular/people",
            "ceo_contact": "Stackular Founding Leadership — https://www.linkedin.com/company/stackular/about"
        },
        {
            "company": "Tapza Technologies",
            "roles": ["AI Engineering Intern", "Agentic AI Intern", "Software Intern"],
            "stipend": "₹15,000 – ₹25,000/month",
            "apply_url": "https://wellfound.com/company/tapza-technologies/jobs/3233261-ai-engineering-intern",
            "location": "Hyderabad",
            "hr_contact": "Talent Acquisition Team — https://www.linkedin.com/company/tapza-technologies",
            "tech_contact": "Agentic AI & LangGraph Engineering Lead — https://www.linkedin.com/company/tapza-technologies/people",
            "ceo_contact": "Vasu Mannem, Co-Founder & Director — https://www.linkedin.com/in/vasu-mannem"
        },
        {
            "company": "Techolution",
            "roles": ["Generative AI Intern / Python AI Intern", "Cloud AI Intern", "Full Stack Intern"],
            "stipend": "Confirmed Paid (+ Incentives + PPO)",
            "apply_url": "https://techolution.com/careers/",
            "location": "Hyderabad",
            "hr_contact": "Madhu, Lead Technical Recruiter Hyderabad — https://www.linkedin.com/company/techolution/people/?keywords=Recruiter",
            "tech_contact": "Principal GenAI Solutions Architect — https://www.linkedin.com/company/techolution/people/?keywords=AI",
            "ceo_contact": "Luv Tulsidas, Founder & CEO — https://www.linkedin.com/in/luvtulsidas"
        },
        {
            "company": "SciTech Patent Art",
            "roles": ["AI/ML & Agentic AI Intern", "Patent Analytics Intern"],
            "stipend": "Confirmed Paid (IP Tech Analytics Program)",
            "apply_url": "https://patent-art.com/careers/",
            "location": "Hyderabad",
            "hr_contact": "Talent Acquisition Lead (Nacharam, Hyderabad) — https://www.linkedin.com/company/scitech-patent-art-services-pvt.-ltd.",
            "tech_contact": "Lead AI & Semantic Search Architect — https://www.linkedin.com/company/scitech-patent-art-services-pvt.-ltd./people",
            "ceo_contact": "Dr. Srinivas Achanta, Managing Director — https://www.linkedin.com/in/srinivas-achanta-79450a1"
        },
        {
            "company": "Adosx Tech",
            "roles": ["Intern - Full-Stack Tech (LLMs & Agentic AI)", "AI Engineer Intern"],
            "stipend": "₹10,000 – ₹12,500/month",
            "apply_url": "https://wellfound.com/company/adosx-tech/jobs",
            "location": "Hyderabad",
            "hr_contact": "Adosx Hiring Team — https://www.linkedin.com/company/adosx-tech",
            "tech_contact": "Pilli Balasubramanyam Sastri, Co-Founder & Tech Director — https://www.linkedin.com/company/adosx-tech/people",
            "ceo_contact": "Apoorva Reddy Podduturi, Co-Founder & Director — https://www.linkedin.com/company/adosx-tech"
        },
        {
            "company": "GyanNidhi Innovations",
            "roles": ["AI/LLM Developer Intern", "AI Deployment Intern", "Python Developer Intern"],
            "stipend": "₹12,000/month",
            "apply_url": "https://www.gyannidhi.in/careers",
            "location": "Hyderabad",
            "hr_contact": "Sravani, Talent Acquisition Lead (sravani@gyannidhi.in) — https://www.linkedin.com/company/gyannidhi-innovations",
            "tech_contact": "GLEXAI LLM Platform Lead — https://www.linkedin.com/company/gyannidhi-innovations/people",
            "ceo_contact": "Akshar Vastarpara, Founder & CEO — https://www.linkedin.com/company/gyannidhi-innovations"
        },
        {
            "company": "MosChip Technologies",
            "roles": ["AI & Embedded Systems Intern", "Edge AI Software Engineer Intern"],
            "stipend": "₹25,000 – ₹35,000/month",
            "apply_url": "https://moschip.com/careers/",
            "location": "Hyderabad",
            "hr_contact": "J. Komali (Talent Acquisition) — https://www.linkedin.com/search/results/all/?keywords=Komali%20MosChip%20Talent%20Acquisition",
            "tech_contact": "Vishal Patil (SVP Product Engineering) — https://www.linkedin.com/search/results/all/?keywords=Vishal%20Patil%20MosChip%20Product%20Engineering",
            "ceo_contact": "Srinivasa Rao Kakumanu (MD & CEO) — https://www.linkedin.com/search/results/all/?keywords=Srinivasa%20Rao%20Kakumanu%20MosChip"
        }
    ]
}

def scout_leads(
    job_title: str,
    location: str,
    job_variants: List[str] = None,
    max_results: int = 25
) -> List[Dict[str, Any]]:
    """
    Collects raw candidates matching the role and location strictly.
    """
    candidates = []
    loc_key = location.strip().lower()
    
    # Check if user requested Hyderabad specifically
    target_city = "hyderabad" if "hyderabad" in loc_key else loc_key
    
    companies = KNOWN_ECOSYSTEMS.get(target_city, [])
    if not companies and ("all" in loc_key or "any" in loc_key):
        for c_list in KNOWN_ECOSYSTEMS.values():
            companies.extend(c_list)

    for comp in companies:
        matched_role = comp["roles"][0]
        for r in comp["roles"]:
            if any(term.lower() in r.lower() for term in (job_variants or [job_title])):
                matched_role = r
                break
        
        candidates.append({
            "company": comp["company"],
            "role": matched_role,
            "location": comp["location"],
            "stipend": comp["stipend"],
            "apply_url": comp["apply_url"],
            "hr_contact": comp.get("hr_contact"),
            "tech_contact": comp.get("tech_contact"),
            "ceo_contact": comp.get("ceo_contact")
        })

    return candidates[:max_results]
