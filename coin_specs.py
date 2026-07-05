# Standard U.S. Mint specifications for the coin types found in this collection.
# Used to auto-fill physical specs (diameter/weight/composition/edge) for each
# inventory row instead of guessing them from a photo.

COIN_SPECS = {
    "Lincoln Cent (Wheat, bronze 1909-1942, 1944-1958)": {
        "diameter_mm": 19.05, "weight_g": 3.11,
        "composition": "95% copper, 5% tin/zinc (bronze)", "edge": "plain",
    },
    "Lincoln Cent (Memorial, bronze 1959-1982)": {
        "diameter_mm": 19.05, "weight_g": 3.11,
        "composition": "95% copper, 5% zinc (bronze)", "edge": "plain",
    },
    "Lincoln Cent (Memorial/Shield, copper-plated zinc 1982-present)": {
        "diameter_mm": 19.05, "weight_g": 2.5,
        "composition": "97.5% zinc, 2.5% copper plating", "edge": "plain",
    },
    "Jefferson Nickel": {
        "diameter_mm": 21.21, "weight_g": 5.0,
        "composition": "75% copper, 25% nickel", "edge": "plain",
    },
    "Roosevelt Dime (silver, 1946-1964)": {
        "diameter_mm": 17.91, "weight_g": 2.50,
        "composition": "90% silver, 10% copper", "edge": "reeded",
    },
    "Roosevelt Dime (clad, 1965-present)": {
        "diameter_mm": 17.91, "weight_g": 2.268,
        "composition": "copper-nickel clad over pure copper core", "edge": "reeded",
    },
    "Washington/State/ATB Quarter (silver, 1932-1964)": {
        "diameter_mm": 24.26, "weight_g": 6.25,
        "composition": "90% silver, 10% copper", "edge": "reeded",
    },
    "Washington/State/ATB Quarter (clad, 1965-present)": {
        "diameter_mm": 24.26, "weight_g": 5.67,
        "composition": "copper-nickel clad over pure copper core", "edge": "reeded",
    },
    "Kennedy Half Dollar (90% silver, 1964)": {
        "diameter_mm": 30.61, "weight_g": 12.5,
        "composition": "90% silver, 10% copper", "edge": "reeded",
    },
    "Kennedy Half Dollar (40% silver, 1965-1970)": {
        "diameter_mm": 30.61, "weight_g": 11.5,
        "composition": "40% silver clad", "edge": "reeded",
    },
    "Kennedy Half Dollar (clad, 1971-present)": {
        "diameter_mm": 30.61, "weight_g": 11.34,
        "composition": "copper-nickel clad over pure copper core", "edge": "reeded",
    },
    "Susan B. Anthony Dollar": {
        "diameter_mm": 26.5, "weight_g": 8.1,
        "composition": "copper-nickel clad over pure copper core", "edge": "reeded (11-sided rim)",
    },
    "Casino Token (base metal)": {
        "diameter_mm": None, "weight_g": None,
        "composition": "brass/nickel-alloy token metal (not U.S. legal tender)", "edge": "varies",
    },
    "Elongated Cent (souvenir)": {
        "diameter_mm": None, "weight_g": None,
        "composition": "copper (rolled from a genuine one-cent planchet)", "edge": "smooth, elongated",
    },
}
