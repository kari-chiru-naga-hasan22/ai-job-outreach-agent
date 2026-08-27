#!/usr/bin/env python3
"""
Job Outreach Agent - Automated Multi-Source Job Search & 3-Contact Telegram Dispatcher
Author: Antigravity
Usage:
    python run.py
    python run.py --role "AI Engineer Intern" --location "All"
    python run.py --dry-run
"""

import os
import sys
import time
from core.config_loader import load_config
from core.scout import scout_leads
from core.verifier import verify_lead_eligibility
from core.enricher import enrich_company_contacts, generate_cold_outreach_why_fits
from core.dispatcher import (
    dispatch_lead,
    send_telegram_message,
    clear_dispatched_cache,
    is_telegram_configured,
    print_telegram_setup_guide
)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def run_pipeline():
    config = load_config()
    telegram_active = is_telegram_configured(config.telegram.bot_token, config.telegram.chat_id) and config.telegram.enabled and not config.dry_run

    print("="*65)
    print("🚀 JOB OUTREACH AGENT & 3-CONTACT TELEGRAM DISPATCHER")
    print("="*65)
    print(f"🎯 Target Role       : {config.job_title}")
    print(f"📍 Target Location   : {config.location}")
    print(f"💼 Job Type          : {config.job_type.title()}")
    print(f"💰 Paid Only         : {'Yes (Min: ₹' + str(config.minimum_stipend_inr) + '/mo)' if config.paid_only else 'No'}")
    print(f"📱 Delivery Mode     : {'Telegram Live Dispatch' if telegram_active else 'Terminal Console Output'}")
    print("="*65)

    if not telegram_active and not config.dry_run:
        print_telegram_setup_guide()

    if config.clear_cache:
        clear_dispatched_cache()

    # Step 1: Scouting
    print(f"🔎 Scouting active listings for '{config.job_title}' in {config.location}...")
    raw_leads = scout_leads(
        job_title=config.job_title,
        location=config.location,
        job_variants=config.job_variants,
        max_results=config.max_leads_per_run
    )
    print(f"Found {len(raw_leads)} potential candidate listings.\n")

    if not raw_leads:
        print(f"[INFO] No candidate listings found for '{config.job_title}' in '{config.location}'.")
        return

    # Notify start on Telegram if active
    if telegram_active:
        send_telegram_message(
            config.telegram.bot_token,
            config.telegram.chat_id,
            f"🚀 *AI Job Hunt Started*\nSearching: `{config.job_title}` across *{config.location}*",
            parse_mode="Markdown"
        )
        time.sleep(1)

    dispatched_count = 0

    # Step 2: Verification, Enrichment & Dispatch
    for idx, raw in enumerate(raw_leads, 1):
        comp = raw["company"]
        role = raw["role"]
        loc = raw["location"]

        # Pay & location verification
        is_eligible, paid_reason = verify_lead_eligibility(
            raw,
            target_location=config.location,
            paid_only=config.paid_only,
            min_stipend_inr=config.minimum_stipend_inr
        )

        if not is_eligible:
            print(f"[{idx}/{len(raw_leads)}] ❌ Skipped {comp} - {role}: {paid_reason}")
            continue

        # 3-Contact LinkedIn Enrichment
        contacts = enrich_company_contacts(comp, known_contacts=raw)
        why_fits = generate_cold_outreach_why_fits(comp, role, loc)

        # Dispatch lead (Sends directly to Telegram if configured, or prints to Console)
        success = dispatch_lead(
            bot_token=config.telegram.bot_token,
            chat_id=config.telegram.chat_id,
            company=comp,
            role=role,
            location=loc,
            paid_status=paid_reason,
            apply_url=raw["apply_url"],
            hr_contact=contacts["hr_contact"],
            tech_contact=contacts["tech_contact"],
            ceo_contact=contacts["ceo_contact"],
            why_fits=why_fits,
            dry_run=config.dry_run
        )

        if success:
            dispatched_count += 1
            if telegram_active:
                time.sleep(1.2)  # Rate limit protection

    # Step 3: Run Summary (Direct to console and Telegram, NO HTML generated)
    summary_msg = f"🏁 Run Complete — {dispatched_count} verified opportunities dispatched for {config.job_title}."
    print("\n" + summary_msg)
    
    if telegram_active and dispatched_count > 0:
        send_telegram_message(
            config.telegram.bot_token,
            config.telegram.chat_id,
            f"🏁 *{summary_msg}*",
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    run_pipeline()
