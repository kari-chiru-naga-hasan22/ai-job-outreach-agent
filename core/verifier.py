import os
import sys
import json
import re
from typing import List, Dict, Any, Tuple

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UNPAID_PATTERN = re.compile(r'\b(unpaid|volunteer|no\s+stipend|₹?\s*0\s*/\s*month|zero\s+stipend)\b', re.IGNORECASE)

def verify_stipend_status(stipend_str: str, min_stipend_inr: int = 10000) -> Tuple[bool, str]:
    if not stipend_str:
        return False, "Unspecified Compensation"
    s_lower = stipend_str.lower()
    if UNPAID_PATTERN.search(s_lower):
        return False, "Explicitly Unpaid / Volunteer Role"
    if "confirmed paid" in s_lower or "paid" in s_lower or "ppo" in s_lower:
        return True, stipend_str
    numbers = re.findall(r'(\d+[\d,.]*)', stipend_str)
    if numbers:
        try:
            val = int(numbers[0].replace(',', '').split('.')[0])
            if val < 100 and "k" in s_lower:
                val *= 1000
            if val >= min_stipend_inr or val >= 5000:
                return True, stipend_str
        except Exception:
            pass
    return True, stipend_str

def verify_location_match(company_loc: str, target_loc: str) -> bool:
    if not company_loc or not target_loc:
        return True
    c_lower = company_loc.lower()
    t_lower = target_loc.lower()
    if t_lower in ["any", "all", "remote", "india"]:
        return True
    return t_lower in c_lower or c_lower in t_lower

def verify_lead_eligibility(
    raw_lead: Dict[str, Any],
    target_location: str = "Hyderabad",
    paid_only: bool = True,
    min_stipend_inr: int = 10000
) -> Tuple[bool, str]:
    loc = raw_lead.get("location", "")
    if not verify_location_match(loc, target_location):
        return False, f"Location mismatch: '{loc}' is outside '{target_location}'"
    stipend = raw_lead.get("stipend", "")
    if paid_only:
        is_paid, reason = verify_stipend_status(stipend, min_stipend_inr=min_stipend_inr)
        if not is_paid:
            return False, f"Not confirmed paid: {reason}"
        return True, reason
    return True, stipend or "Unspecified"
