# Per-image bounding boxes (fractions of width/height) for isolating each
# individual coin out of a multi-coin batch photo. Only ONE canonical photo
# per physical group is boxed (duplicate-angle re-shoots of the same coins
# are noted in coin_inventory_data.py instead of re-boxed).
#
# Box format: {"id": "<image>_c##", "x0","y0","x1","y1": fraction 0-1,
#              "flagged": bool, "flag_reason": str}

DR = 0.052   # half-width fraction for a dime
DRY = 0.07   # half-height fraction for a dime
QR = 0.075   # half-width fraction for a quarter
QRY = 0.095  # half-height fraction for a quarter

def _cent_grid():
    """The ~40-coin hand-laid grid in IMG_1209 (also re-photographed in
    IMG_1210/1211, which we don't re-box). Columns/rows are only
    approximately even since the coins were placed by hand."""
    cols_x = [0.065, 0.19, 0.305, 0.42, 0.54, 0.655, 0.775, 0.895]
    rows_y_left = [0.193, 0.353, 0.51, 0.667, 0.807]   # cols 0-4
    rows_y_right = [0.14, 0.307, 0.46, 0.627, 0.767]   # cols 5-7 (sit a bit higher)
    cr, cry = 0.058, 0.077  # cent half-width / half-height fractions
    boxes = []
    for ci, cx in enumerate(cols_x):
        rows_y = rows_y_left if ci < 5 else rows_y_right
        for ri, cy in enumerate(rows_y):
            boxes.append({
                "id": f"grid_c{ci+1}r{ri+1}",
                "x0": cx - cr, "y0": cy - cry, "x1": cx + cr, "y1": cy + cry,
            })
    # an extra coin wedged in next to grid_c3r5/grid_c4r5 at the bottom
    boxes.append({"id": "grid_extra1", "x0": 0.355 - cr, "y0": 0.793 - cry, "x1": 0.355 + cr, "y1": 0.793 + cry})
    return boxes


COIN_BOXES = {
    "IMG_1213.jpeg": [
        # --- dimes ---
        {"id": "d01", "x0": 0.31-DR, "y0": 0.22-DRY, "x1": 0.31+DR, "y1": 0.22+DRY},
        {"id": "d02", "x0": 0.44-DR, "y0": 0.22-DRY, "x1": 0.44+DR, "y1": 0.22+DRY},
        {"id": "d03", "x0": 0.31-DR, "y0": 0.393-DRY, "x1": 0.31+DR, "y1": 0.393+DRY},
        {"id": "d04", "x0": 0.44-DR, "y0": 0.393-DRY, "x1": 0.44+DR, "y1": 0.393+DRY},
        {"id": "d05", "x0": 0.31-DR, "y0": 0.567-DRY, "x1": 0.31+DR, "y1": 0.567+DRY},
        {"id": "d06", "x0": 0.44-DR, "y0": 0.567-DRY, "x1": 0.44+DR, "y1": 0.567+DRY},
        {"id": "d07", "x0": 0.20-DR, "y0": 0.727-DRY, "x1": 0.20+DR, "y1": 0.727+DRY},
        {"id": "d08", "x0": 0.31-DR, "y0": 0.727-DRY, "x1": 0.31+DR, "y1": 0.727+DRY},
        {"id": "d09", "x0": 0.44-DR, "y0": 0.727-DRY, "x1": 0.44+DR, "y1": 0.727+DRY},
        {"id": "d10", "x0": 0.20-DR, "y0": 0.887-DRY, "x1": 0.20+DR, "y1": 0.887+DRY},
        {"id": "d11", "x0": 0.31-DR, "y0": 0.887-DRY, "x1": 0.31+DR, "y1": 0.887+DRY},
        {"id": "d12", "x0": 0.44-DR, "y0": 0.887-DRY, "x1": 0.44+DR, "y1": 0.887+DRY},
        # --- quarters ---
        {"id": "q01_nc", "x0": 0.876-QR, "y0": 0.145-QRY, "x1": 0.876+QR, "y1": 0.145+QRY},
        {"id": "q02_wxc", "x0": 0.873-QR, "y0": 0.38-QRY, "x1": 0.873+QR, "y1": 0.38+QRY},
        {"id": "q03_unk", "x0": 0.685-QR, "y0": 0.575-QRY, "x1": 0.685+QR, "y1": 0.575+QRY},
        {"id": "q04_angelou", "x0": 0.876-QR, "y0": 0.575-QRY, "x1": 0.876+QR, "y1": 0.575+QRY},
        {"id": "q05_co", "x0": 0.674-QR, "y0": 0.80-QRY, "x1": 0.674+QR, "y1": 0.80+QRY},
        {"id": "q06_wv", "x0": 0.876-QR, "y0": 0.80-QRY, "x1": 0.876+QR, "y1": 0.80+QRY},
    ],
    "IMG_1203.jpeg": [
        # loose nickel (also visible in IMG_1205/1206/1207, not re-boxed)
        {"id": "n01", "x0": 0.115, "y0": 0.74, "x1": 0.22, "y1": 0.86},
    ],
    "IMG_1209.jpeg": _cent_grid(),
    "IMG_1208.jpeg": [
        {"id": "p01", "cx": 0.395, "cy": 0.18},
        {"id": "p02", "cx": 0.30, "cy": 0.313},
        {"id": "p03", "cx": 0.48, "cy": 0.327},
        {"id": "p04", "cx": 0.235, "cy": 0.433},
        {"id": "p05", "cx": 0.36, "cy": 0.433},
        {"id": "p06", "cx": 0.565, "cy": 0.427},
        {"id": "p07", "cx": 0.655, "cy": 0.46},
        {"id": "p08", "cx": 0.165, "cy": 0.553},
        {"id": "p09", "cx": 0.305, "cy": 0.553},
        {"id": "p10", "cx": 0.45, "cy": 0.553},
        {"id": "p11", "cx": 0.60, "cy": 0.567},
        {"id": "p12", "cx": 0.80, "cy": 0.547},
        {"id": "p13", "cx": 0.24, "cy": 0.653},
        {"id": "p14", "cx": 0.395, "cy": 0.667},
        {"id": "p15", "cx": 0.53, "cy": 0.667},
        {"id": "p16", "cx": 0.72, "cy": 0.667},
        {"id": "p17", "cx": 0.35, "cy": 0.773},
        {"id": "p18", "cx": 0.45, "cy": 0.787},
        {"id": "p19", "cx": 0.565, "cy": 0.773},
        {"id": "p20", "cx": 0.675, "cy": 0.78},
    ],
    "IMG_1233.jpeg": [
        {"id": "b01", "cx": 0.225, "cy": 0.40},
        {"id": "b02", "cx": 0.33, "cy": 0.41},
        {"id": "b03", "cx": 0.43, "cy": 0.407},
        {"id": "b04", "cx": 0.545, "cy": 0.413},
        {"id": "b05", "cx": 0.65, "cy": 0.433},
        {"id": "b06", "cx": 0.80, "cy": 0.46},
        {"id": "b07", "cx": 0.24, "cy": 0.60},
        {"id": "b08", "cx": 0.37, "cy": 0.613},
        {"id": "b09", "cx": 0.48, "cy": 0.62},
        {"id": "b10", "cx": 0.605, "cy": 0.633},
        {"id": "b11_gold", "cx": 0.71, "cy": 0.64, "flagged": True, "flag_reason": "Unusual brass/gold toning - worth a second look even though most likely just discoloration"},
    ],
    "IMG_1237.jpeg": [
        {"id": "s1_c2015", "cx": 0.34, "cy": 0.213},
        {"id": "s1_c2004", "cx": 0.56, "cy": 0.467},
        {"id": "s1_nickel", "cx": 0.115, "cy": 0.267},
    ],
    "IMG_1238.jpeg": [
        {"id": "s2_c2013", "cx": 0.115, "cy": 0.553},
        {"id": "s2_c2016", "cx": 0.56, "cy": 0.467},
        {"id": "s2_shield", "cx": 0.33, "cy": 0.553},
    ],
    "IMG_1239.jpeg": [
        {"id": "s3_c2015", "cx": 0.14, "cy": 0.407},
        {"id": "s3_c2020", "cx": 0.31, "cy": 0.227},
        {"id": "s3_c2023", "cx": 0.79, "cy": 0.48},
        {"id": "s3_c1986", "cx": 0.89, "cy": 0.647},
        {"id": "s3_nickel", "cx": 0.295, "cy": 0.487},
    ],
    "IMG_1240.jpeg": [
        {"id": "s4_nickel2022", "cx": 0.375, "cy": 0.433},
        {"id": "s4_nickel2009", "cx": 0.65, "cy": 0.633},
        {"id": "s4_gold", "cx": 0.28, "cy": 0.82, "flagged": True, "flag_reason": "Second unusual brass/gold-toned cent in this batch - same likely explanation as the other one (environmental discoloration), but worth comparing the two side by side"},
    ],
}

# convert any {"cx","cy"} shorthand entries into x0/y0/x1/y1 boxes
for _img, _boxes in COIN_BOXES.items():
    for _b in _boxes:
        if "cx" in _b:
            _b["x0"] = _b["cx"] - 0.058
            _b["x1"] = _b["cx"] + 0.058
            _b["y0"] = _b["cy"] - 0.077
            _b["y1"] = _b["cy"] + 0.077
