# ── Slot-based managed customer ───────────────────────────────────────────────
# All managed-customer constants derive from SLOT so you only need to change
# one number when the current slot is taken by leftover data.
#
# How to use:
#   - If tests fail because the name/email already exists with wrong data,
#     increment SLOT (e.g. SLOT = 2) and re-run. The fixture will create a
#     fresh customer automatically.
#   - The fixture is self-healing: if a previous run left the name in a
#     changed state (e.g. "auto customer1 edited"), it will restore it.

SLOT = 10

CUSTOMER_FIRST = "vk test"
CUSTOMER_LAST = f"auto customer{SLOT}"
CUSTOMER_EMAIL = f"vktestcust{SLOT}@yopmail.com"
CUSTOMER_PHONE = "1111111111"
CUSTOMER_SITE = "Vk AL01"
CUSTOMER_DOB = "1990-01-15"
CUSTOMER_ADDRESS = "Vk test cust 1 test address"
CUSTOMER_ZIP = "10001"
CUSTOMER_STATE = "Arizona"
CUSTOMER_CITY = "Amado"
CUSTOMER_LICENSE_PLATE = "07"
CUSTOMER_CAR_RFID = "VK-CAR7"

# ── Edit-test scratch values ───────────────────────────────────────────────────
UPDATED_LAST = f"{CUSTOMER_LAST} edited"

# ── Negative / missing data ────────────────────────────────────────────────────
MISSING_PLATE = "NOMATCH-99999"
MISSING_PHONE = "0000000000"

# ── Broken-state markers ──────────────────────────────────────────────────────
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]
