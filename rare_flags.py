# Reference list of U.S. coin key dates / varieties worth flagging for a closer
# look. This is not an appraisal - it's a cheap first-pass filter so a handful
# of candidates get pulled out of a big bag instead of everything being
# treated as "probably common."

KEY_DATE_CENTS = {
    "1909-S VDB", "1909-S", "1914-D", "1922 (no mintmark/plain)",
    "1931-S", "1943 (bronze - should be steel, extremely rare error)",
    "1943 (steel - normal for that year)", "1955 (doubled die obverse)",
    "1972 (doubled die obverse)", "1969-S (doubled die obverse)",
}

RULES = [
    {
        "test": lambda row: row["category"] == "Circulating Cent" and row.get("wheat_reverse"),
        "reason": "Wheat-reverse cent (1909-1958) - worth pulling aside and checking the exact date/mintmark against the key-date list (1909-S VDB, 1909-S, 1914-D, 1922 plain, 1931-S, 1955 DDO) before assuming it's common.",
    },
    {
        "test": lambda row: row["category"] == "Circulating Dime" and row.get("year") and _year_num(row["year"]) and _year_num(row["year"]) <= 1964,
        "reason": "Dated 1964 or earlier - Roosevelt dimes this age are 90% silver, worth several dollars in melt value alone regardless of grade.",
    },
    {
        "test": lambda row: row["category"] == "Circulating Quarter" and row.get("year") and _year_num(row["year"]) and _year_num(row["year"]) <= 1964,
        "reason": "Dated 1964 or earlier - Washington quarters this age are 90% silver.",
    },
    {
        "test": lambda row: row["category"] == "Circulating Nickel" and row.get("year") and _year_num(row["year"]) in (1942, 1943, 1944, 1945),
        "reason": "1942-1945 Jefferson nickels were struck in 35% silver (\"war nickels\") - check for a large mintmark over Monticello's dome.",
    },
]


def _year_num(year_field):
    try:
        return int(str(year_field).strip()[:4])
    except (ValueError, TypeError):
        return None


def flag(row):
    """Return (is_flagged, reason) for an inventory row dict."""
    for rule in RULES:
        try:
            if rule["test"](row):
                return True, rule["reason"]
        except Exception:
            continue
    return False, ""
