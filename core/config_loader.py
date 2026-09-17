import argparse
import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

@dataclass
class TelegramConfig:
    bot_token: str = ""
    chat_id: str = ""
    enabled: bool = True

@dataclass
class JobSearchConfig:
    job_title: str = "AI Engineer Intern"
    job_variants: List[str] = field(default_factory=lambda: [
        "Agentic AI Engineer Intern",
        "GenAI Intern",
        "Machine Learning Intern",
        "LLM Engineer Intern"
    ])
    location: str = "Hyderabad"
    job_type: str = "internship"  # internship | fulltime | any
    paid_only: bool = True
    minimum_stipend_inr: int = 10000
    max_leads_per_run: int = 15
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    dry_run: bool = False
    clear_cache: bool = False

def load_config(config_path: str = DEFAULT_CONFIG_PATH, cli_args: Optional[List[str]] = None) -> JobSearchConfig:
    config_dict: Dict[str, Any] = {}
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_dict = json.load(f)
        except Exception as e:
            print(f"[WARNING] Could not parse config file '{config_path}': {e}. Using defaults.")

    parser = argparse.ArgumentParser(description="Job Outreach Agent - Multi-Source Search & 3-Contact Telegram Dispatcher")
    parser.add_argument("--role", "--job-title", dest="job_title", type=str, help="Target job title to search")
    parser.add_argument("--location", dest="location", type=str, help="Target city or location")
    parser.add_argument("--type", dest="job_type", choices=["internship", "fulltime", "any"], help="Job type")
    parser.add_argument("--paid-only", dest="paid_only", action="store_true", default=None, help="Enforce paid positions only")
    parser.add_argument("--min-stipend", dest="min_stipend", type=int, help="Minimum monthly stipend in INR")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Print leads to console without sending Telegram messages")
    parser.add_argument("--clear-cache", dest="clear_cache", action="store_true", help="Clear dispatched leads deduplication cache")
    parser.add_argument("--config", dest="config_file", type=str, default=config_path, help="Path to config.json")

    args = parser.parse_args(cli_args)

    tg_raw = config_dict.get("telegram", {})
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN") or tg_raw.get("bot_token", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID") or tg_raw.get("chat_id", "")
    tg_config = TelegramConfig(
        bot_token=bot_token,
        chat_id=chat_id,
        enabled=tg_raw.get("enabled", True) and bool(bot_token and chat_id)
    )

    job_title = args.job_title or config_dict.get("job_title", "AI Engineer Intern")
    job_variants = config_dict.get("job_variants", [])
    if job_title not in job_variants:
        job_variants = [job_title] + job_variants

    location = args.location or config_dict.get("location", "Hyderabad")
    job_type = args.job_type or config_dict.get("job_type", "internship")
    paid_only = args.paid_only if args.paid_only is not None else config_dict.get("paid_only", True)
    minimum_stipend_inr = args.min_stipend if args.min_stipend is not None else config_dict.get("minimum_stipend_inr", 10000)
    max_leads = config_dict.get("max_leads_per_run", 15)

    return JobSearchConfig(
        job_title=job_title,
        job_variants=job_variants,
        location=location,
        job_type=job_type,
        paid_only=paid_only,
        minimum_stipend_inr=minimum_stipend_inr,
        max_leads_per_run=max_leads,
        telegram=tg_config,
        dry_run=args.dry_run,
        clear_cache=args.clear_cache
    )
