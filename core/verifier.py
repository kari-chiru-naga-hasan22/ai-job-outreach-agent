import re
from typing import Dict, Any, Tuple

UNPAID_PATTERN = re.compile(
    r"\b(unpaid|volunteer|no\s+stipend|₹?\s*0\s*/\s*month|zero\s+stipend|certificate\s+only|un-paid)\b",
    re.IGNORECASE
)

def verify_lead_eligibility(
    raw_lead: Dict[str, Any],
    target_location: str,
    paid_only: bool = True,
    min_stipend_inr: int = 0
) -> Tuple[bool, str]:
    """
    Returns (is_eligible, reason_or_paid_status)
    """
    role = raw_lead.get("role", "").strip()
    location = raw_lead.get("location", "").strip()
    raw_pay = str(raw_lead.get("stipend", "") or raw_lead.get("paid_status", "")).strip()

    # 1. Location verification
    if target_location.lower() not in ["any", "all", "remote"]:
        if target_location.lower() not in location.lower() and location.lower() not in target_location.lower():
            return False, f"Location mismatch: {location} does not match {target_location}"

    # 2. Unpaid check via regex word boundaries
    if UNPAID_PATTERN.search(raw_pay) or UNPAID_PATTERN.search(role):
        if paid_only:
            return False, f"Unpaid position: {raw_pay}"

    # 3. Pay extraction & validation
    if paid_only:
        if not raw_pay or raw_pay.lower() in ["unknown", "none", "unclear"]:
            return False, "Pay status unconfirmed"

        # Check numeric minimum if present
        nums = re.findall(r"(\d[\d,]+)", raw_pay.replace(",", ""))
        if nums and min_stipend_inr > 0:
            found_stipend = int(nums[0])
            if 0 < found_stipend < min_stipend_inr:
                return False, f"Stipend ₹{found_stipend} below minimum ₹{min_stipend_inr}"

    paid_status = raw_pay if raw_pay.startswith("Confirmed") else f"Confirmed ({raw_pay})"
    return True, paid_status
