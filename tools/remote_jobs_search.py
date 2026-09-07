#!/usr/bin/env python3
"""
Remote Jobs Search CLI Tool
Part of the remote-jobs-search and job-outreach-agent skills.
Searches all 10 remote job portals from 'Remote Jobs Websites.pdf' and company career pages in parallel.
"""

import sys
import os
import argparse
import json

# Add parent directory to path so core modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.remote_scout import scout_all_parallel, REMOTE_PORTALS, COMPANY_CAREER_TARGETS
from core.enricher import enrich_company_contacts, generate_cold_outreach_why_fits

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def format_table(leads):
    if not leads:
        print("No job opportunities found.")
        return

    print(f"\n{'='*110}")
    print(f"{'#':<3} | {'COMPANY':<22} | {'ROLE':<35} | {'SOURCE':<24} | {'LOCATION'}")
    print(f"{'='*110}")
    for idx, lead in enumerate(leads, 1):
        comp = lead.get("company", "N/A")[:22]
        role = lead.get("role", "N/A")[:35]
        src = lead.get("source", "N/A")[:24]
        loc = lead.get("location", "Remote")[:20]
        print(f"{idx:<3} | {comp:<22} | {role:<35} | {src:<24} | {loc}")
        print(f"    🔗 Apply: {lead.get('apply_url')}")
        if lead.get("contacts", {}).get("apollo_people_url"):
            print(f"    🚀 Apollo Emails: {lead['contacts']['apollo_people_url']}")
    print(f"{'='*110}\n")

def main():
    parser = argparse.ArgumentParser(description="Parallel search across 10 remote job portals and company career pages.")
    subparsers = parser.add_subparsers(dest="command")

    # Command: list-portals
    subparsers.add_parser("list-portals", help="List all 10 remote job portals from the PDF directory.")

    # Command: search
    search_parser = subparsers.add_parser("search", help="Search jobs across all portals and career pages in parallel.")
    search_parser.add_argument("-q", "--query", type=str, required=True, help="Job title, role or keyword (e.g. 'AI Engineer', 'Python')")
    search_parser.add_argument("-l", "--location", type=str, default="Remote", help="Location filter (default: Remote)")
    search_parser.add_argument("--career-pages", action="store_true", default=True, help="Include parallel scan of company career portals.")
    search_parser.add_argument("--limit", type=int, default=25, help="Max results to return (default: 25)")
    search_parser.add_argument("--format", choices=["table", "json", "plain"], default="table", help="Output format (table, json, plain)")

    args = parser.parse_args()

    if args.command == "list-portals":
        print("\n📂 Curated Remote Job Websites Directory (from Remote Jobs Websites.pdf):")
        print("="*75)
        for idx, (k, p) in enumerate(REMOTE_PORTALS.items(), 1):
            print(f"{idx:2d}. {p['name']:<18} — {p['url']}")
        print(f"\n🏢 Company Career Targets (Parallel Scan): {len(COMPANY_CAREER_TARGETS)} Companies")
        print("="*75)
        return

    if args.command == "search" or not args.command:
        query = getattr(args, "query", None)
        if not query:
            if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
                query = sys.argv[1]
            else:
                query = "AI Engineer Intern"

        location = getattr(args, "location", "Remote")
        limit = getattr(args, "limit", 25)
        out_format = getattr(args, "format", "table")

        print(f"🔎 Scouting in parallel: '{query}' across 10 Remote Portals & Company Career Pages...")
        leads = scout_all_parallel(query, location=location, max_results=limit)

        # Enrich each lead with verified LinkedIn points of contact
        for lead in leads:
            contacts = enrich_company_contacts(lead["company"], known_contacts=lead)
            lead["contacts"] = contacts
            lead["why_fits"] = generate_cold_outreach_why_fits(lead["company"], lead["role"], lead["location"])

        if out_format == "json":
            print(json.dumps(leads, indent=2))
        elif out_format == "plain":
            for idx, l in enumerate(leads, 1):
                print(f"[{idx}] {l['company']} - {l['role']} ({l['location']})")
                print(f"    Apply: {l['apply_url']}")
                print(f"    Source: {l.get('source')}\n")
        else:
            format_table(leads)
            print(f"Found {len(leads)} verified opportunities.\n")

if __name__ == "__main__":
    main()
