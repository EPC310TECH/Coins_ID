# Coin/set inventory data, compiled by visual identification of the photos in
# coin_images/. Each row is one PHYSICAL coin or one full set/token where the
# pieces aren't sold apart. Loose coins in multi-coin batch photos have been
# isolated into their own crop (see coin_crops/) with a matching annotated
# overlay (see annotated/) showing exactly where on the source photo that coin
# sits - see build_all() in annotate.py and the box coordinates in
# coin_boxes.py. Values are rough reference-guide ranges for common
# circulated/typical-grade examples in original packaging where noted - actual
# grade-sensitive value requires an in-hand look or a certified grade.
#
# confidence: "high" = design/date clearly legible; "medium" = design certain,
# date probable; "low" = read from a rotated/worn/glare-affected coin, verify
# in hand.
#
# crop_file: filename in coin_crops/ isolating this exact physical coin, or
# None if this row wasn't individually boxed (bulk/residual rows, or items
# that are already a single subject in their source photo).
# box_id: the id used in coin_boxes.py / annotate.py for this coin, or None.
# wheat_reverse: True if the reverse was actually seen and shows wheat ears
# (pre-1959 Lincoln cent) - feeds rare_flags.py.
# flagged / flag_reason: a visual anomaly worth a second look (e.g. unusual
# toning), independent of the key-date rare_flags.py check.

INVENTORY = [
    # ---------------- MINT / PROOF SETS ----------------
    {
        "photo_group": "Set 1", "source_images": "IMG_1198, IMG_1199",
        "category": "Proof Set", "denomination": "Cent/Nickel/Dime/Quarter/Half Dollar (5 coins)",
        "country": "USA", "year": 1960, "mint_mark": "(none - Philadelphia, pre-1968 proofs unmarked)",
        "design_variety": "1960 U.S. Proof Set in original hard-plastic holder",
        "coin_spec_key": None,
        "obverse_text": "Individual coins: LIBERTY / IN GOD WE TRUST + date on each",
        "reverse_text": "Holder engraved: \"U.S. PROOF COINS 1960\"",
        "condition_notes": "Sealed in period Capital-style plastic holder, light haze/toning visible on cent and nickel, dime/quarter/half show cameo-like mirror fields",
        "qty": 1,
        "est_value_low_usd": 32, "est_value_high_usd": 50,
        "value_basis": "Greysheet/USA Coin Book 2026 guide, large-date vs small-date cent variety affects low/high end",
        "confidence": "high",
        "notes": "Cent/nickel are base metal; dime, quarter, half are 90% silver. Large-date vs small-date cent variety changes value - check cent closely.",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Set 2", "source_images": "IMG_1214",
        "category": "Mint Set", "denomination": "Cent/Nickel/Dime/Quarter/Half Dollar",
        "country": "USA", "year": 1974, "mint_mark": "P (Philadelphia panel photographed)",
        "design_variety": "1974 U.S. Mint Uncirculated Set, sealed cellophane pack",
        "coin_spec_key": None,
        "obverse_text": "Kennedy half visible: LIBERTY / IN GOD WE TRUST 1974",
        "reverse_text": "n/a (sealed pack)",
        "condition_notes": "Still factory-sealed in original cellophane with red stripe",
        "qty": 1,
        "est_value_low_usd": 15, "est_value_high_usd": 19,
        "value_basis": "Greysheet ($15) / USA Coin Book (~$19) 2026 guide for complete P&D set",
        "confidence": "high",
        "notes": "Only the Philadelphia panel was photographed - full 1974 Mint Set includes a matching Denver (D) panel; check the envelope for a second sealed panel before assuming this is complete.",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Set 3", "source_images": "IMG_1215",
        "category": "Mint Set", "denomination": "Cent/Nickel/Dime/Quarter/Half Dollar/SBA Dollar",
        "country": "USA", "year": 1998, "mint_mark": "P&D",
        "design_variety": "1998 U.S. Mint Uncirculated Set, sealed cellophane pack",
        "coin_spec_key": None,
        "obverse_text": "Susan B. Anthony Dollar (LIBERTY, 1998), Washington quarter, Kennedy half, Roosevelt dime, Jefferson nickel, Lincoln cent all visible",
        "reverse_text": "n/a (sealed pack)",
        "condition_notes": "Factory-sealed cellophane",
        "qty": 1,
        "est_value_low_usd": 5, "est_value_high_usd": 7,
        "value_basis": "Greysheet (~$5.50) / USA Coin Book (~$7.20) 2026 guide",
        "confidence": "high",
        "notes": "1998 was the last year of the Susan B. Anthony dollar before the Sacagawea dollar replaced it in 2000 - a small draw for type collectors.",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Set 4", "source_images": "IMG_1216",
        "category": "Mint Set", "denomination": "Cent/Nickel/Dime/Quarter/Half Dollar",
        "country": "USA", "year": 1999, "mint_mark": "P&D",
        "design_variety": "1999 U.S. Mint Uncirculated Set (Delaware state quarter visible), sealed cellophane pack",
        "coin_spec_key": None,
        "obverse_text": "Delaware statehood quarter, Kennedy half, Jefferson nickel, Lincoln cent visible",
        "reverse_text": "n/a (sealed pack)",
        "condition_notes": "Factory-sealed cellophane",
        "qty": 1,
        "est_value_low_usd": 8, "est_value_high_usd": 12,
        "value_basis": "General guide range for early 50-States-era mint sets (first year of state quarter program)",
        "confidence": "medium",
        "notes": "First year of the 50 State Quarters program - modestly more collector interest than later years.",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Set 5", "source_images": "IMG_1217",
        "category": "Commemorative Display Card", "denomination": "Nickel (+ cent visible)",
        "country": "USA", "year": 2004, "mint_mark": "P (Philadelphia)",
        "design_variety": "\"Westward Journey\" Keelboat Jefferson Nickel on a themed collector card",
        "coin_spec_key": "Jefferson Nickel",
        "obverse_text": "UNITED STATES OF AMERICA, LEWIS & CLARK, KEELBOAT, FIVE CENTS",
        "reverse_text": "Card text: \"The Westward Journey / Keelboat\", \"Philadelphia Denver 2004\"",
        "condition_notes": "Uncirculated-looking nickel mounted in card, cent below only partly visible",
        "qty": 1,
        "est_value_low_usd": 1, "est_value_high_usd": 3,
        "value_basis": "Common date/mintmark Keelboat nickel is worth face to ~$1 even in high uncirculated grade; card adds small novelty premium",
        "confidence": "high",
        "notes": "Not a full mint set - just the nickel (and a cent) on a promotional display card. No real numismatic premium over face value.",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },

    # ---------------- TOKENS / EXONUMIA (not U.S. legal tender) ----------------
    {
        "photo_group": "Token 1", "source_images": "IMG_1200",
        "category": "Casino Token", "denomination": "$1.00 (redeemable cash value)",
        "country": "USA (Nevada)", "year": None, "mint_mark": None,
        "design_variety": "Aladdin Hotel & Casino (Las Vegas) \"World's 7 Wonders\" series - Eiffel Tower",
        "coin_spec_key": "Casino Token (base metal)",
        "obverse_text": "ONE DOLLAR REDEEMABLE CASH VALUE / EIFFEL TOWER / ALADDIN",
        "reverse_text": "Aladdin and magic carpet over the casino name (not photographed in this set of images)",
        "condition_notes": "Brass-toned token in a plastic capsule, light wear",
        "qty": 1,
        "est_value_low_usd": 2, "est_value_high_usd": 5,
        "value_basis": "eBay/Worthpoint comparables for individual Aladdin World's 7 Wonders tokens (complete 7-piece $2 sets sell around $18, i.e. ~$2.50/token)",
        "confidence": "high",
        "notes": "Aladdin closed/was demolished in 1998 (site is now Planet Hollywood) - defunct-casino tokens like this have modest but real collector demand.",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Token 2", "source_images": "IMG_1201",
        "category": "Casino Token", "denomination": "$2.00 (redeemable cash value)",
        "country": "USA (Nevada)", "year": 1996, "mint_mark": None,
        "design_variety": "Aladdin Hotel & Casino (Las Vegas) \"World's 7 Wonders\" series",
        "coin_spec_key": "Casino Token (base metal)",
        "obverse_text": "TWO DOLLAR REDEEMABLE CASH VALUE / WORLD'S 7 WONDERS / ALADDIN",
        "reverse_text": "Aladdin and magic carpet motif",
        "condition_notes": "Brass-toned token in a plastic capsule, light wear, small edge nick",
        "qty": 1,
        "est_value_low_usd": 2, "est_value_high_usd": 5,
        "value_basis": "Same comparables as Token 1",
        "confidence": "high",
        "notes": "Series issued 1996; there were 7 different wonder designs at $2 each - if there are more of these in the bag, a matched set is worth more together than piecemeal.",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Exonumia 1", "source_images": "IMG_1202",
        "category": "Elongated Cent (souvenir)", "denomination": "Rolled 1 cent",
        "country": "USA", "year": 1939, "mint_mark": None,
        "design_variety": "1939 New York World's Fair \"The World of Tomorrow\" - Trylon & Perisphere",
        "coin_spec_key": "Elongated Cent (souvenir)",
        "obverse_text": "NEW YORK WORLD'S FAIR 1939 / THE WORLD OF TOMORROW (rolled over Trylon & Perisphere image)",
        "reverse_text": "n/a (rolled onto a genuine Lincoln cent planchet, original details erased)",
        "condition_notes": "Good detail, brown copper patina, no major creases",
        "qty": 1,
        "est_value_low_usd": 5, "est_value_high_usd": 15,
        "value_basis": "Collector-forum comparables: common 1939 NYWF elongated designs sell for a few dollars, scarcer die varieties up to ~$50; PCGS CoinFacts catalogs this as die variety M&D-1",
        "confidence": "high",
        "notes": "This is a legitimate 87-year-old souvenir elongated coin, not a modern reproduction - collectible in the elongated-coin (\"pressed penny\") hobby, which is a real and organized sub-collecting niche.",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },

    # ---------------- LOOSE QUARTERS (IMG_1213, boxes q01-q06) ----------------
    {
        "photo_group": "Quarter - North Carolina", "source_images": "IMG_1213, IMG_1203, IMG_1205, IMG_1206, IMG_1207",
        "category": "Circulating Quarter", "denomination": "25 cents",
        "country": "USA", "year": 2001, "mint_mark": "not legible in photo",
        "design_variety": "50 State Quarters - North Carolina (\"NORTH CAROLINA 1789\", First Flight / Wright Flyer)",
        "coin_spec_key": "Washington/State/ATB Quarter (clad, 1965-present)",
        "obverse_text": "UNITED STATES OF AMERICA / LIBERTY / IN GOD WE TRUST",
        "reverse_text": "NORTH CAROLINA 1789 / FIRST FLIGHT / Wright Flyer biplane",
        "condition_notes": "Circulated, moderate wear",
        "qty": 1,
        "est_value_low_usd": 0.25, "est_value_high_usd": 1,
        "value_basis": "Face value; common-date circulated state quarters carry no premium",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1213_q01_nc.jpg", "box_id": "q01_nc", "wheat_reverse": False,
    },
    {
        "photo_group": "Quarter - Washington Crossing the Delaware", "source_images": "IMG_1213, IMG_1203, IMG_1205, IMG_1207",
        "category": "Circulating Quarter", "denomination": "25 cents",
        "country": "USA", "year": 2021, "mint_mark": "not legible in photo",
        "design_variety": "\"Washington Crossing the Delaware\" quarter (George Washington crossing the Delaware River, boat scene)",
        "coin_spec_key": "Washington/State/ATB Quarter (clad, 1965-present)",
        "obverse_text": "UNITED STATES OF AMERICA / E PLURIBUS UNUM / crossing scene / QUARTER DOLLAR",
        "reverse_text": "(design shown is on what's usually the reverse face; Washington portrait is on the other side, not photographed in this crop)",
        "condition_notes": "Circulated, light wear",
        "qty": 1,
        "est_value_low_usd": 0.25, "est_value_high_usd": 1,
        "value_basis": "Face value; common-date circulated commemorative-reverse quarters carry no premium",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1213_q02_wxc.jpg", "box_id": "q02_wxc", "wheat_reverse": False,
    },
    {
        "photo_group": "Quarter - unidentified rays design", "source_images": "IMG_1213",
        "category": "Circulating Quarter", "denomination": "25 cents",
        "country": "USA", "year": None, "mint_mark": "not legible in photo",
        "design_variety": "American Women Quarters (?) - robed/dancing figure with radiating ray lines and a diamond-shaped geometric element; closest match appears to be the 2023 \"Maria Tallchief\" (prima ballerina) design, but this is not fully certain from photo angle/wear alone",
        "coin_spec_key": "Washington/State/ATB Quarter (clad, 1965-present)",
        "obverse_text": "...QUARTER DOLLAR (partial arc text, rest obscured by wear/glare)",
        "reverse_text": "Standing/dancing robed figure, radiating rays, diamond design element",
        "condition_notes": "Moderate wear, some glare obscuring the lettering needed for a certain ID",
        "qty": 1,
        "est_value_low_usd": 0.25, "est_value_high_usd": 1,
        "value_basis": "Face value regardless of exact design - modern clad quarters carry no premium",
        "confidence": "low",
        "notes": "This is a 6th quarter that wasn't part of the original 5 identified in earlier passes. Recommend comparing side-by-side with a reference photo of the 2023 Maria Tallchief American Women Quarter to confirm.",
        "crop_file": "IMG_1213_q03_unk.jpg", "box_id": "q03_unk", "wheat_reverse": False,
    },
    {
        "photo_group": "Quarter - Maya Angelou", "source_images": "IMG_1213, IMG_1206",
        "category": "Circulating Quarter", "denomination": "25 cents",
        "country": "USA", "year": 2022, "mint_mark": "not legible in photo",
        "design_variety": "American Women Quarters - Maya Angelou (figure with wings/arms raised, rising sun rays)",
        "coin_spec_key": "Washington/State/ATB Quarter (clad, 1965-present)",
        "obverse_text": "UNITED STATES OF AMERICA / QUARTER DOLLAR / E PLURIBUS UNUM",
        "reverse_text": "MAYA ANGELOU / bird in flight / sunrise rays design",
        "condition_notes": "Lightly circulated, good detail",
        "qty": 1,
        "est_value_low_usd": 0.25, "est_value_high_usd": 1,
        "value_basis": "Face value; first-year 2022 American Women Quarter, common in circulation",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1213_q04_angelou.jpg", "box_id": "q04_angelou", "wheat_reverse": False,
    },
    {
        "photo_group": "Quarter - Colorado", "source_images": "IMG_1213, IMG_1203, IMG_1205, IMG_1206, IMG_1207",
        "category": "Circulating Quarter", "denomination": "25 cents",
        "country": "USA", "year": 2006, "mint_mark": "not legible in photo",
        "design_variety": "50 State Quarters - Colorado (\"COLORADO 1876\", Rocky Mountains design)",
        "coin_spec_key": "Washington/State/ATB Quarter (clad, 1965-present)",
        "obverse_text": "UNITED STATES OF AMERICA / LIBERTY / IN GOD WE TRUST",
        "reverse_text": "COLORADO 1876 / mountain landscape",
        "condition_notes": "Circulated, moderate wear",
        "qty": 1,
        "est_value_low_usd": 0.25, "est_value_high_usd": 1,
        "value_basis": "Face value; common-date circulated state quarters carry no premium",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1213_q05_co.jpg", "box_id": "q05_co", "wheat_reverse": False,
    },
    {
        "photo_group": "Quarter - West Virginia", "source_images": "IMG_1213, IMG_1203, IMG_1205, IMG_1207",
        "category": "Circulating Quarter", "denomination": "25 cents",
        "country": "USA", "year": 2005, "mint_mark": "not legible in photo",
        "design_variety": "50 State Quarters - West Virginia (\"WEST VIRGINIA 1863\", New River Gorge Bridge)",
        "coin_spec_key": "Washington/State/ATB Quarter (clad, 1965-present)",
        "obverse_text": "UNITED STATES OF AMERICA / LIBERTY / IN GOD WE TRUST",
        "reverse_text": "WEST VIRGINIA 1863 / New River Gorge Bridge",
        "condition_notes": "Circulated, light-moderate wear",
        "qty": 1,
        "est_value_low_usd": 0.25, "est_value_high_usd": 1,
        "value_basis": "Face value; common-date circulated state quarters carry no premium",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1213_q06_wv.jpg", "box_id": "q06_wv", "wheat_reverse": False,
    },
]


def _dime(box_id, year=None, confidence="low", notes=""):
    return {
        "photo_group": f"Dime {box_id}", "source_images": "IMG_1213, IMG_1206, IMG_1210",
        "category": "Circulating Dime", "denomination": "10 cents",
        "country": "USA", "year": year, "mint_mark": "not legible in photo",
        "design_variety": "Roosevelt Dime, clad", "coin_spec_key": "Roosevelt Dime (clad, 1965-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST" + (f" / {year}" if year else ""),
        "reverse_text": "not photographed close enough to read",
        "condition_notes": "Moderate to heavy circulation wear" + ("; date obscured/rotated in this crop" if not year else ""),
        "qty": 1,
        "est_value_low_usd": 0.10, "est_value_high_usd": 0.10,
        "value_basis": "Face value if clad (1965+); would be worth several dollars in silver melt alone if 1964-or-earlier (90% silver) - check edge for a copper-colored stripe (clad) vs uniform silver-gray (silver)",
        "confidence": confidence,
        "notes": notes or "Edge check: a visible copper-colored line means clad (common); a solid silver-gray edge with no copper line means 90% silver (1964 or earlier) - worth pulling aside.",
        "crop_file": f"IMG_1213_{box_id}.jpg", "box_id": box_id, "wheat_reverse": False,
    }


DIMES = [
    _dime("d01"), _dime("d02"), _dime("d03"), _dime("d04"), _dime("d05"), _dime("d06"),
    _dime("d07", year=1973, confidence="low",
          notes="Partial \"1973\" visible at the bottom edge of this crop - not fully confident, verify in hand."),
    _dime("d08"), _dime("d09"), _dime("d10"), _dime("d11"), _dime("d12"),
]

NICKEL_LOOSE = [
    {
        "photo_group": "Nickel 1", "source_images": "IMG_1203, IMG_1205, IMG_1206, IMG_1207",
        "category": "Circulating Nickel", "denomination": "5 cents",
        "country": "USA", "year": None, "mint_mark": "not legible in photo",
        "design_variety": "Jefferson Nickel, heavily worn (date not legible)",
        "coin_spec_key": "Jefferson Nickel",
        "obverse_text": "LIBERTY (partial, worn smooth)",
        "reverse_text": "not clearly photographed",
        "condition_notes": "Heavily worn/smoothed, date illegible in photo",
        "qty": 1,
        "est_value_low_usd": 0.05, "est_value_high_usd": 0.05,
        "value_basis": "Face value - worn common-date Jefferson nickels have no numismatic premium",
        "confidence": "medium", "notes": "",
        "crop_file": "IMG_1203_n01.jpg", "box_id": "n01", "wheat_reverse": False,
    },
]

# ---------------- CENT GRID (IMG_1209, also re-shot in IMG_1210/1211) ----------------
# year=None + wheat_reverse=True means: reverse actually shows wheat ears (pre-1959),
# but the obverse date wasn't legible in this rotation/lighting.
_GRID_READS = {
    "c1r1": dict(year=None, wheat=True, conf="medium",
                 notes="Wheat-ears reverse confirms this is a pre-1959 Lincoln cent. Obverse date not legible in this rotation - flip and check against key dates (1909-S VDB, 1909-S, 1914-D, 1922 plain, 1931-S, 1955 DDO) before assuming it's common."),
    "c1r2": dict(year=None, conf="low", notes="Worn/rotated, date not legible from photo."),
    "c1r3": dict(year=None, wheat=True, conf="medium",
                 notes="Wheat-ears reverse, dark/corroded - pre-1959 cent, date not legible. Check against key dates before assuming common."),
    "c1r4": dict(year=None, conf="low", notes="Worn/rotated, date not legible from photo."),
    "c1r5": dict(year=1968, conf="high", notes=""),
    "c2r1": dict(year=None, wheat=True, conf="medium",
                 notes="Wheat-ears reverse, dark/corroded - pre-1959 cent, date not legible. Check against key dates before assuming common."),
    "c2r2": dict(year="1975", conf="low", notes="Partially legible, verify in hand."),
    "c2r3": dict(year="1974", conf="low", notes="Partially legible, verify in hand."),
    "c2r4": dict(year=None, conf="low", notes="Worn, glare obscures the date."),
    "c2r5": dict(year=1988, conf="high", notes=""),
    "c3r1": dict(year=None, conf="low", notes="Dark and worn, date not legible."),
    "c3r2": dict(year="1971", conf="medium", notes=""),
    "c3r3": dict(year=1984, conf="high", notes=""),
    "c3r4": dict(year=1982, conf="high", notes=""),
    "c3r5": dict(year=1962, conf="medium", notes="Partially obscured by neighboring coin in this crop."),
    "c4r1": dict(year=1972, conf="high", notes=""),
    "c4r2": dict(year=1982, conf="high", notes=""),
    "c4r3": dict(year="1961", conf="medium", notes=""),
    "c4r4": dict(year=1976, mint="D", conf="high", notes=""),
    "c4r5": dict(year=1980, conf="high", notes=""),
    "c5r1": dict(year="1970", conf="medium", notes=""),
    "c5r2": dict(year=1969, conf="high", notes=""),
    "c5r3": dict(year="1972", conf="medium", notes=""),
    "c5r4": dict(year=1966, conf="high", notes=""),
    "c5r5": dict(year=None, conf="low", notes="Worn, date not legible."),
    "c6r1": dict(year=1982, conf="high", notes=""),
    "c6r2": dict(year=1982, conf="high", notes=""),
    "c6r3": dict(year=None, conf="low", notes="Worn, date not legible."),
    "c6r4": dict(year=1989, conf="high", notes=""),
    "c6r5": dict(year=None, conf="low", notes="Worn/obscured by neighboring coin."),
    "c7r1": dict(year="1973", conf="medium", notes=""),
    "c7r2": dict(year="1965", conf="medium", notes=""),
    "c7r3": dict(year=None, conf="low", notes="Dark and worn, date not legible."),
    "c7r4": dict(year="1969", conf="medium", notes=""),
    "c7r5": dict(year=1976, conf="high", notes=""),
    "c8r1": dict(year=None, conf="low", notes="Dark and worn, date not legible."),
    "c8r2": dict(year=None, conf="low", notes="Dark and worn, date not legible."),
    "c8r3": dict(year=None, conf="low", notes="Dark and worn, date not legible."),
    "c8r4": dict(year=None, conf="low", notes="Underexposed/dark, date not legible."),
    "c8r5": dict(year=None, conf="low", notes="Dark and worn, date not legible."),
    "extra1": dict(year=1980, conf="low",
                   notes="This crop's dominant coin looks like the SAME 1980 cent captured in grid_c4r5 (the two boxes are adjacent/overlapping) - likely not a distinct 42nd physical coin. Treat as a duplicate view unless a physical recount says otherwise."),
}


def _cent_grid_row(box_id, year, conf, notes, wheat=False, mint="not legible in photo"):
    if wheat:
        spec_key = "Lincoln Cent (Wheat, bronze 1909-1942, 1944-1958)"
    elif isinstance(year, int) and year >= 1982:
        spec_key = "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)"
    elif isinstance(year, int) or (isinstance(year, str) and year.isdigit()):
        spec_key = "Lincoln Cent (Memorial, bronze 1959-1982)"
    else:
        spec_key = "Lincoln Cent (Memorial, bronze 1959-1982) / (copper-plated zinc 1982-present)"
    return {
        "photo_group": f"Cent grid {box_id}", "source_images": "IMG_1209, IMG_1210, IMG_1211",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": year, "mint_mark": mint,
        "design_variety": "Lincoln wheat cent (pre-1959)" if wheat else "Lincoln Memorial cent",
        "coin_spec_key": spec_key,
        "obverse_text": "LIBERTY / IN GOD WE TRUST" + (f" / {year}" if year else " / date not legible"),
        "reverse_text": "wheat ears / ONE CENT" if wheat else "Lincoln Memorial building / ONE CENT / UNITED STATES OF AMERICA",
        "condition_notes": "From the ~40-coin hand-laid grid photographed in IMG_1209 (also re-photographed at the same angle in IMG_1210/1211 - not re-boxed there since it's the same physical layout)",
        "qty": 1,
        "est_value_low_usd": 0.01 if not wheat else 0.05,
        "est_value_high_usd": 0.25 if not wheat else 1.50,
        "value_basis": "Face value for common-date memorial cents; wheat cents (1909-1958) are worth a modest premium (~$0.05-$0.25 common dates) unless a key date, which can be worth $20 to thousands",
        "confidence": conf,
        "notes": notes,
        "crop_file": f"IMG_1209_grid_{box_id}.jpg", "box_id": f"grid_{box_id}", "wheat_reverse": wheat,
    }


CENT_GRID_ROWS = [
    _cent_grid_row(bid, r.get("year"), r["conf"], r["notes"], wheat=r.get("wheat", False), mint=r.get("mint", "not legible in photo"))
    for bid, r in _GRID_READS.items()
]

# ---------------- SCATTERED PILE (IMG_1208, also re-shot in IMG_1212) ----------------
_PILE_READS = {
    "p01": dict(year=1982, conf="medium", notes=""),
    "p02": dict(year=None, conf="low", notes="Digits ambiguous - looks like the 1970s (possibly 1971 or 1977), not confident enough to record a specific year."),
    "p03": dict(year="1971", conf="medium", notes=""),
    "p04": dict(year="1976", conf="medium", notes=""),
    "p05": dict(year=1974, mint="D", conf="high", notes=""),
    "p06": dict(year=None, conf="low", notes="Dark and worn, date not legible."),
    "p07": dict(year=None, conf="low", notes="Date not legible in this crop."),
    "p08": dict(year="1982", conf="medium", notes=""),
    "p09": dict(year="1974", conf="medium", notes=""),
    "p10": dict(year=None, conf="low",
                notes="Digits are ambiguous between a 1970s date and \"1944\" - if it's actually 1944 this would be a wheat cent (check the reverse for wheat ears). Worth a physical look rather than assuming either reading."),
    "p11": dict(year=None, conf="low", notes="Dark, date not legible."),
    "p12": dict(year=None, conf="low", notes="Only a sliver of this coin is visible in-frame; date not legible."),
    "p13": dict(year=1974, mint="D", conf="medium", notes=""),
    "p14": dict(year=None, conf="low", notes="Date digits not clearly legible."),
    "p15": dict(year="1974", conf="low", notes="Partially legible, verify in hand."),
    "p16": dict(year=None, conf="low", notes="Overlapping neighbor coin makes the date ambiguous."),
    "p17": dict(year="1974", conf="medium", notes=""),
    "p18": dict(year=None, conf="low", notes="Date obscured by an overlapping neighbor coin."),
    "p19": dict(year="1976", conf="medium", notes=""),
    "p20": dict(year=None, conf="low", notes="Dark, date not legible."),
}


def _pile_row(box_id, year, conf, notes, mint="not legible in photo"):
    if isinstance(year, int) and year >= 1982:
        spec_key = "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)"
    elif year:
        spec_key = "Lincoln Cent (Memorial, bronze 1959-1982)"
    else:
        spec_key = "Lincoln Cent (Memorial, bronze 1959-1982) / (copper-plated zinc 1982-present)"
    return {
        "photo_group": f"Pile {box_id}", "source_images": "IMG_1208, IMG_1212",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": year, "mint_mark": mint,
        "design_variety": "Lincoln Memorial cent",
        "coin_spec_key": spec_key,
        "obverse_text": "LIBERTY / IN GOD WE TRUST" + (f" / {year}" if year else " / date not legible"),
        "reverse_text": "not the focus of this crop (obverse-up)",
        "condition_notes": "From the ~20-coin scattered (non-grid) pile photographed in IMG_1208 (also re-photographed at the same angle in IMG_1212 - not re-boxed there since it's the same physical pile)",
        "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.25,
        "value_basis": "Face value for common-date memorial cents; no wheat cents confirmed in this particular pile",
        "confidence": conf,
        "notes": notes,
        "crop_file": f"IMG_1208_{box_id}.jpg", "box_id": box_id, "wheat_reverse": False,
    }


PILE_ROWS = [_pile_row(bid, r.get("year"), r["conf"], r["notes"], mint=r.get("mint", "not legible in photo")) for bid, r in _PILE_READS.items()]

# ---------------- BATCH 2 CENTS (IMG_1233) ----------------
_BATCH2_CENT_READS = {
    "b01": dict(year=2023, reverse="shield", conf="high", notes=""),
    "b02": dict(year=None, reverse="shield", conf="medium", notes="Union Shield reverse is clear (2010-present), but the obverse/date isn't shown in this crop."),
    "b03": dict(year=2021, reverse="shield", conf="high", notes=""),
    "b04": dict(year=2021, reverse="shield", conf="high", notes=""),
    "b05": dict(year=None, reverse="shield", conf="medium", notes="Union Shield reverse is clear (2010-present), but the obverse/date isn't shown in this crop."),
    "b06": dict(year=2021, reverse="shield", conf="high", notes=""),
    "b07": dict(year=2011, reverse="shield", conf="high", notes=""),
    "b08": dict(year=None, reverse="memorial", conf="medium", notes="Lincoln Memorial reverse is clear (1959-2008), but the obverse/date isn't shown in this crop."),
    "b09": dict(year=1976, reverse="memorial", conf="high", notes=""),
    "b10": dict(year=None, reverse="shield", conf="medium", notes="Union Shield reverse is clear (2010-present), but the obverse/date isn't shown in this crop."),
}


def _batch2_cent_row(box_id, year, reverse, conf, notes):
    if reverse == "shield":
        spec_key = "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)"
        rev_text = "ONE CENT / E PLURIBUS UNUM / UNITED STATES OF AMERICA - Union Shield design"
        design = "Lincoln cent, Union Shield reverse (2010-present)"
    else:
        spec_key = "Lincoln Cent (Memorial, bronze 1959-1982) / (copper-plated zinc 1982-present)"
        rev_text = "Lincoln Memorial building / ONE CENT / UNITED STATES OF AMERICA"
        design = "Lincoln cent, Memorial reverse (1959-2008)"
    return {
        "photo_group": f"Batch 2 cent {box_id}", "source_images": "IMG_1233",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": year, "mint_mark": "not legible in photo",
        "design_variety": design, "coin_spec_key": spec_key,
        "obverse_text": ("LIBERTY / IN GOD WE TRUST" + (f" / {year}" if year else "")) if year else "not shown in this crop",
        "reverse_text": rev_text,
        "condition_notes": "Laid out on green textured fabric, good detail, some glare",
        "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.04,
        "value_basis": "Face value - common modern dates, no premium",
        "confidence": conf, "notes": notes,
        "crop_file": f"IMG_1233_{box_id}.jpg", "box_id": box_id, "wheat_reverse": False,
    }


BATCH2_CENT_ROWS = [_batch2_cent_row(bid, r["year"], r["reverse"], r["conf"], r["notes"]) for bid, r in _BATCH2_CENT_READS.items()]
BATCH2_CENT_ROWS.append({
    "photo_group": "Batch 2 cent b11_gold", "source_images": "IMG_1233",
    "category": "Circulating Cent", "denomination": "1 cent",
    "country": "USA", "year": None, "mint_mark": None,
    "design_variety": "Union Shield cent (2010-present) with unusual overall brass/gold coloring instead of normal copper-red",
    "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
    "obverse_text": "not shown in this crop",
    "reverse_text": "ONE CENT / E PLURIBUS UNUM / UNITED STATES OF AMERICA - shield design, brassy-gold tone",
    "condition_notes": "Distinct yellow/gold tone across the whole coin, unlike the reddish-brown of the others next to it",
    "qty": 1,
    "est_value_low_usd": 0.01, "est_value_high_usd": 1,
    "value_basis": "Face value - the color shift is almost certainly heat/chemical discoloration or a novelty gold-dipped souvenir cent, not a mint error or plating variety with real premium",
    "confidence": "medium",
    "notes": "If you want to be sure, a genuine mint error (like a wrong-planchet or unplated cent) would be worth checking with a coin dealer, but the most common explanation for an evenly gold-toned modern cent is environmental exposure - which does not add value.",
    "crop_file": "IMG_1233_b11_gold.jpg", "box_id": "b11_gold", "wheat_reverse": False,
    "flagged": True, "flag_reason": "Unusual brass/gold toning - worth a second look even though most likely just discoloration",
})

# ---------------- BATCH 2 NICKELS (IMG_1234-1236, not individually boxed) ----------------
BATCH2_NICKEL_ROWS = [
    {
        "photo_group": "Batch 2 nickel - 2022", "source_images": "IMG_1234, IMG_1235, IMG_1236",
        "category": "Circulating Nickel", "denomination": "5 cents",
        "country": "USA", "year": "2022 (P)", "mint_mark": "P",
        "design_variety": "Jefferson Nickel, \"Return to Monticello\" design (2006-present)",
        "coin_spec_key": "Jefferson Nickel",
        "obverse_text": "IN GOD WE TRUST / Liberty (script signature) / 2022 P",
        "reverse_text": "MONTICELLO / E PLURIBUS UNUM / UNITED STATES OF AMERICA / FIVE CENTS",
        "condition_notes": "Lightly circulated, good detail, clearly dated",
        "qty": 1,
        "est_value_low_usd": 0.05, "est_value_high_usd": 0.05,
        "value_basis": "Face value - common date/mintmark",
        "confidence": "high", "notes": "",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Batch 2 nickel - worn 1", "source_images": "IMG_1234, IMG_1235, IMG_1236",
        "category": "Circulating Nickel", "denomination": "5 cents",
        "country": "USA", "year": None, "mint_mark": "not legible in photo",
        "design_variety": "Jefferson Nickel, older classic design, date worn/photo too blurry to read",
        "coin_spec_key": "Jefferson Nickel",
        "obverse_text": "LIBERTY / IN GOD WE TRUST (arched pre-2004 style lettering)",
        "reverse_text": "MONTICELLO / E PLURIBUS UNUM / UNITED STATES OF AMERICA / FIVE CENTS",
        "condition_notes": "Moderate wear; reverse photos (IMG_1235/1236) are motion-blurred, date not recoverable from these images",
        "qty": 1,
        "est_value_low_usd": 0.05, "est_value_high_usd": 0.05,
        "value_basis": "Face value expected for a common worn Jefferson nickel; re-photograph in focus if you want an exact date",
        "confidence": "low", "notes": "",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Batch 2 nickel - worn 2", "source_images": "IMG_1234, IMG_1235, IMG_1236",
        "category": "Circulating Nickel", "denomination": "5 cents",
        "country": "USA", "year": None, "mint_mark": "not legible in photo",
        "design_variety": "Jefferson Nickel, older classic design, date worn/photo too blurry to read",
        "coin_spec_key": "Jefferson Nickel",
        "obverse_text": "LIBERTY / IN GOD WE TRUST (arched pre-2004 style lettering)",
        "reverse_text": "MONTICELLO / E PLURIBUS UNUM / UNITED STATES OF AMERICA / FIVE CENTS",
        "condition_notes": "Moderate wear; reverse photos (IMG_1235/1236) are motion-blurred, date not recoverable from these images",
        "qty": 1,
        "est_value_low_usd": 0.05, "est_value_high_usd": 0.05,
        "value_basis": "Face value expected for a common worn Jefferson nickel; re-photograph in focus if you want an exact date",
        "confidence": "low", "notes": "",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
]

# ---------------- BIG SPREAD (IMG_1237-1240) - individually isolated coins ----------------
BIG_SPREAD_ROWS = [
    {
        "photo_group": "Big Spread cent - 2015 (frame 1)", "source_images": "IMG_1237",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": 2015, "mint_mark": "not legible in photo",
        "design_variety": "Lincoln Union Shield cent", "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST / 2015", "reverse_text": "not shown in this crop",
        "condition_notes": "Good detail, on green quilted fabric", "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.01, "value_basis": "Face value - common modern date",
        "confidence": "medium", "notes": "Bottom edge of the date is slightly cropped in this photo.",
        "crop_file": "IMG_1237_s1_c2015.jpg", "box_id": "s1_c2015", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread cent - 2004 (frame 1)", "source_images": "IMG_1237",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": 2004, "mint_mark": "not legible in photo",
        "design_variety": "Lincoln Memorial cent", "coin_spec_key": "Lincoln Cent (Memorial, bronze 1959-1982) / (copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST / 2004", "reverse_text": "not shown in this crop",
        "condition_notes": "Good detail, on green quilted fabric", "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.01, "value_basis": "Face value - common modern date",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1237_s1_c2004.jpg", "box_id": "s1_c2004", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread nickel (frame 1)", "source_images": "IMG_1237",
        "category": "Circulating Nickel", "denomination": "5 cents",
        "country": "USA", "year": None, "mint_mark": "not legible in photo",
        "design_variety": "Jefferson Nickel, \"Return to Monticello\" design (script Liberty)",
        "coin_spec_key": "Jefferson Nickel",
        "obverse_text": "IN GOD WE TRUST / Liberty (script) / date not clearly legible",
        "reverse_text": "not shown in this crop",
        "condition_notes": "Heavy dark toning obscures the exact date digits (looks like a 2020s date)",
        "qty": 1,
        "est_value_low_usd": 0.05, "est_value_high_usd": 0.05, "value_basis": "Face value - common date expected",
        "confidence": "low", "notes": "Toning makes the last 1-2 digits ambiguous; re-check in hand under better light.",
        "crop_file": "IMG_1237_s1_nickel.jpg", "box_id": "s1_nickel", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread cent - 2013 (frame 2)", "source_images": "IMG_1238",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": 2013, "mint_mark": "not legible in photo",
        "design_variety": "Lincoln Union Shield cent", "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST / 2013", "reverse_text": "not shown in this crop",
        "condition_notes": "Darker toning, moderate wear", "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.01, "value_basis": "Face value - common modern date",
        "confidence": "medium", "notes": "",
        "crop_file": "IMG_1238_s2_c2013.jpg", "box_id": "s2_c2013", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread cent - 2016 (frame 2)", "source_images": "IMG_1238",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": 2016, "mint_mark": "not legible in photo",
        "design_variety": "Lincoln Union Shield cent", "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST / 2016", "reverse_text": "not shown in this crop",
        "condition_notes": "Good detail, some glare", "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.01, "value_basis": "Face value - common modern date",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1238_s2_c2016.jpg", "box_id": "s2_c2016", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread cent - shield reverse (frame 2)", "source_images": "IMG_1238",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": None, "mint_mark": None,
        "design_variety": "Lincoln cent, Union Shield reverse (2010-present)",
        "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
        "obverse_text": "not shown in this crop",
        "reverse_text": "UNITED STATES OF AMERICA / ONE CENT - Union Shield design",
        "condition_notes": "Gold-ish patina, reverse-up", "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.01, "value_basis": "Face value - common, no premium",
        "confidence": "medium", "notes": "Reverse confirms 2010-present, but obverse/date not shown in this crop.",
        "crop_file": "IMG_1238_s2_shield.jpg", "box_id": "s2_shield", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread cent - 2015 (frame 3)", "source_images": "IMG_1239",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": 2015, "mint_mark": "not legible in photo",
        "design_variety": "Lincoln Union Shield cent", "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST / 2015", "reverse_text": "not shown in this crop",
        "condition_notes": "Good detail", "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.01, "value_basis": "Face value - common modern date",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1239_s3_c2015.jpg", "box_id": "s3_c2015", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread cent - 2020 (frame 3)", "source_images": "IMG_1239",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": 2020, "mint_mark": "not legible in photo",
        "design_variety": "Lincoln Union Shield cent", "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST / 2020", "reverse_text": "not shown in this crop",
        "condition_notes": "Good detail, coin is rotated in-frame", "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.01, "value_basis": "Face value - common modern date",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1239_s3_c2020.jpg", "box_id": "s3_c2020", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread cent - 2023 (frame 3)", "source_images": "IMG_1239",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": 2023, "mint_mark": "not legible in photo",
        "design_variety": "Lincoln Union Shield cent", "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST / 2023", "reverse_text": "not shown in this crop",
        "condition_notes": "Good detail, coin is rotated in-frame", "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.01, "value_basis": "Face value - common modern date",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1239_s3_c2023.jpg", "box_id": "s3_c2023", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread cent - 1986 (frame 3)", "source_images": "IMG_1239",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": 1986, "mint_mark": "not legible in photo",
        "design_variety": "Lincoln Memorial cent", "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST / 1986", "reverse_text": "not shown in this crop",
        "condition_notes": "Good detail", "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 0.01, "value_basis": "Face value - common date",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1239_s3_c1986.jpg", "box_id": "s3_c1986", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread dime (frame 3, was mislabeled as a nickel)", "source_images": "IMG_1239",
        "category": "Circulating Dime", "denomination": "10 cents",
        "country": "USA", "year": None, "mint_mark": "not legible in photo",
        "design_variety": "Roosevelt Dime", "coin_spec_key": "Roosevelt Dime (clad, 1965-present)",
        "obverse_text": "LIBERTY / date not shown in this crop", "reverse_text": "not shown in this crop",
        "condition_notes": "This box was originally labeled \"s3_nickel\" during layout but the coin is actually a Roosevelt Dime (profile bust + LIBERTY arc match the dime obverse, not the Jefferson Nickel design) - corrected here.",
        "qty": 1,
        "est_value_low_usd": 0.10, "est_value_high_usd": 0.10,
        "value_basis": "Face value if clad; check edge for a copper stripe (clad) vs solid silver-gray (90% silver, 1964-or-earlier)",
        "confidence": "low", "notes": "Date not visible in this crop - re-photograph to confirm year.",
        "crop_file": "IMG_1239_s3_nickel.jpg", "box_id": "s3_nickel", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread nickel - 2022 (frame 4)", "source_images": "IMG_1240",
        "category": "Circulating Nickel", "denomination": "5 cents",
        "country": "USA", "year": 2022, "mint_mark": "not legible in photo",
        "design_variety": "Jefferson Nickel, \"Return to Monticello\" design (script Liberty)",
        "coin_spec_key": "Jefferson Nickel",
        "obverse_text": "IN GOD WE TRUST / Liberty (script) / 2022", "reverse_text": "not shown in this crop",
        "condition_notes": "Clear, lightly circulated", "qty": 1,
        "est_value_low_usd": 0.05, "est_value_high_usd": 0.05, "value_basis": "Face value - common date",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1240_s4_nickel2022.jpg", "box_id": "s4_nickel2022", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread nickel - 2009 (frame 4)", "source_images": "IMG_1240",
        "category": "Circulating Nickel", "denomination": "5 cents",
        "country": "USA", "year": 2009, "mint_mark": "P",
        "design_variety": "Jefferson Nickel, \"Return to Monticello\" design (script Liberty)",
        "coin_spec_key": "Jefferson Nickel",
        "obverse_text": "IN GOD WE TRUST / Liberty (script) / 2009 P", "reverse_text": "not shown in this crop",
        "condition_notes": "Clear, lightly circulated", "qty": 1,
        "est_value_low_usd": 0.05, "est_value_high_usd": 0.05, "value_basis": "Face value - common date/mintmark",
        "confidence": "high", "notes": "",
        "crop_file": "IMG_1240_s4_nickel2009.jpg", "box_id": "s4_nickel2009", "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread cent - anomalous gold-toned (frame 4)", "source_images": "IMG_1240",
        "category": "Circulating Cent", "denomination": "1 cent",
        "country": "USA", "year": None, "mint_mark": None,
        "design_variety": "Lincoln cent with unusual overall brass/gold coloring instead of normal copper-red",
        "coin_spec_key": "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / partial date obscured by the gold toning (possibly 1960s, not confirmed)",
        "reverse_text": "not shown in this crop",
        "condition_notes": "Distinct yellow/gold tone across the whole coin - second gold-toned cent found in this collection (see also b11_gold from batch 2)",
        "qty": 1,
        "est_value_low_usd": 0.01, "est_value_high_usd": 1,
        "value_basis": "Face value - most likely environmental discoloration, not a mint error",
        "confidence": "low",
        "notes": "Second unusual brass/gold-toned cent in this batch - same likely explanation as the other one (environmental discoloration), but worth comparing the two side by side.",
        "crop_file": "IMG_1240_s4_gold.jpg", "box_id": "s4_gold", "wheat_reverse": False,
        "flagged": True, "flag_reason": "Second unusual brass/gold-toned cent in this batch - worth comparing side by side with b11_gold",
    },
]

# ---------------- BIG SPREAD residual (not individually isolated) ----------------
# 4 overlapping photos (IMG_1237-1240) of what looks like ONE large scattered
# spread - the coins above were isolated with confidence; these residual rows
# cover what's left, with the qty reduced by however many were pulled out
# above. Still very likely some double-counting between the 4 frames - see notes.
BIG_SPREAD_RESIDUAL_ROWS = [
    {
        "photo_group": "Big Spread - remaining cents", "source_images": "IMG_1237, IMG_1238, IMG_1239, IMG_1240",
        "category": "Circulating Cent (bulk, possible duplicate photos)", "denomination": "1 cent",
        "country": "USA", "year": None, "mint_mark": None,
        "design_variety": "Additional Lincoln cents visible across these 4 photos, not individually isolated",
        "coin_spec_key": "Lincoln Cent (Memorial, bronze 1959-1982) / (copper-plated zinc 1982-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST + date", "reverse_text": "mix of Lincoln Memorial and Union Shield reverses",
        "condition_notes": "These 4 photos appear to be overlapping shots of ONE large scattered coin spread (same green quilted fabric, matching coins visible near the edges of adjacent frames), not 4 separate piles",
        "qty": 23,
        "est_value_low_usd": 0.23, "est_value_high_usd": 0.23,
        "value_basis": "Face value expected - no wheat cents or unusual dates spotted among these",
        "confidence": "low",
        "notes": "Treat this as one estimate for the whole spread, not 4x the visible coins - recommend a physical recount since the same coins likely appear in more than one of these 4 overlapping photos. 10 of the coins in this spread were individually isolated above (see \"Big Spread cent/dime\" rows).",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread - remaining nickels", "source_images": "IMG_1237, IMG_1238, IMG_1239, IMG_1240",
        "category": "Circulating Nickel", "denomination": "5 cents",
        "country": "USA", "year": None, "mint_mark": "not legible in photo",
        "design_variety": "Additional Jefferson Nickels, mix of older arched-\"LIBERTY\" pre-2004 design and newer script design, dates not legible",
        "coin_spec_key": "Jefferson Nickel",
        "obverse_text": "LIBERTY / IN GOD WE TRUST + date (not legible)",
        "reverse_text": "not photographed",
        "condition_notes": "Several look moderately worn with a duller/darker tone - worth a quick check for 1942-1945 \"war nickels\" (35% silver, large mint mark over Monticello dome)",
        "qty": 6,
        "est_value_low_usd": 0.30, "est_value_high_usd": 5,
        "value_basis": "Face value if standard copper-nickel; ~$1.50+ each in silver melt alone if any turn out to be 1942-1945 war nickels",
        "confidence": "low",
        "notes": "Quick tell for a war nickel: flip it over - if the mint mark letter (P, D, or S) is large and sits directly above Monticello's dome, it's 35% silver. 3 nickels in this spread were individually isolated above.",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
    {
        "photo_group": "Big Spread - remaining dimes", "source_images": "IMG_1237, IMG_1238, IMG_1239, IMG_1240",
        "category": "Circulating Dime", "denomination": "10 cents",
        "country": "USA", "year": None, "mint_mark": "not legible in photo",
        "design_variety": "Roosevelt Dimes, various, scattered in the same spread",
        "coin_spec_key": "Roosevelt Dime (clad, 1965-present)",
        "obverse_text": "LIBERTY / IN GOD WE TRUST", "reverse_text": "not photographed close enough to read",
        "condition_notes": "Glare on a couple of these obscures the date",
        "qty": 6,
        "est_value_low_usd": 0.60, "est_value_high_usd": 12,
        "value_basis": "Face value if clad; ~$2+ each in silver melt if any are 1964-or-earlier (90% silver)",
        "confidence": "low",
        "notes": "Same silver-date check applies here as the other dime groups. 1 dime in this spread was individually isolated above (see \"Big Spread dime\").",
        "crop_file": None, "box_id": None, "wheat_reverse": False,
    },
]

INVENTORY += DIMES + NICKEL_LOOSE + CENT_GRID_ROWS + PILE_ROWS + BATCH2_CENT_ROWS + BATCH2_NICKEL_ROWS + BIG_SPREAD_ROWS + BIG_SPREAD_RESIDUAL_ROWS

# make sure every row has the newer optional keys so build_inventory.py can rely on them
for _row in INVENTORY:
    _row.setdefault("crop_file", None)
    _row.setdefault("box_id", None)
    _row.setdefault("wheat_reverse", False)
    _row.setdefault("flagged", False)
    _row.setdefault("flag_reason", "")
