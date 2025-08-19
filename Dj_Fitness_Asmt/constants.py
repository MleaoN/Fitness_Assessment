# fitness_core/constants.py
"""
Refactored constant tables for fitness assessment web program.

Contents:
- BMI categories
- WHR ranges
- Body fat thresholds
- Explosive power thresholds
- Push-up and squat thresholds
- Plank percentiles
- One-Leg Stance thresholds
- Toe Touch thresholds
- Metadata for threshold order and units
"""

from dataclasses import dataclass

# -----------------------------
# BMI Categories
# -----------------------------
@dataclass
class BMIThreshold:
    bmi: float
    label: str
    linestyle: str
    color: str

BMI_CATEGORIES = {
    "underweight": BMIThreshold(18.5, "Underweight (BMI 18.5)", "--", "blue"),
    "ideal": BMIThreshold(22, "Ideal (BMI 22)", "-", "green"),
    "overweight": BMIThreshold(25, "Overweight (BMI 25)", "--", "red"),
}

# -----------------------------
# Waist-to-Hip Ratio (WHR) ranges
# -----------------------------
WHR_RANGES = {
    "Male": [0, 0.85, 0.90, 0.95, float("inf")],  # boundaries
    "Female": [0, 0.75, 0.80, 0.86, float("inf")],
}

# -----------------------------
# Body Fat (%) thresholds
# -----------------------------
BODY_FAT_TABLE = {
    "Male": {
        "20-29": [5, 10, 15, 20, 25, 30],
        "30-39": [6, 11, 16, 21, 26, 31],
        "40-49": [7, 12, 17, 22, 27, 32],
        "50-59": [8, 13, 18, 23, 28, 33],
        "60-69": [9, 14, 19, 24, 29, 34],
        "70-79": [10, 15, 20, 25, 30, 35],
    },
    "Female": {
        "20-29": [15, 20, 25, 30, 35, 40],
        "30-39": [16, 21, 26, 31, 36, 41],
        "40-49": [17, 22, 27, 32, 37, 42],
        "50-59": [18, 23, 28, 33, 38, 43],
        "60-69": [19, 24, 29, 34, 39, 44],
        "70-79": [20, 25, 30, 35, 40, 45],
    },
}

# -----------------------------
# Explosive Power thresholds (Watts)
# -----------------------------
EXPLOSIVE_POWER_TABLE = {
    "Male": {
        "15-19": [4644, 4185, 3858, 3323, 1500],
        "20-29": [5094, 4640, 4297, 3375, 1500],
        "30-39": [4860, 4389, 3967, 3485, 1500],
        "40-49": [4320, 3700, 3242, 2708, 1500],
        "50-59": [4019, 3567, 2937, 2512, 1500],
        "60-69": [3764, 3291, 2843, 2383, 1500],
    },
    "Female": {
        "15-19": [3167, 2795, 2399, 2156, 1000],
        "20-29": [3250, 2804, 2478, 2271, 1000],
        "30-39": [3193, 2550, 2335, 2147, 1000],
        "40-49": [2675, 2288, 2101, 1688, 1000],
        "50-59": [2559, 2161, 1701, 1386, 1000],
        "60-69": [2475, 1717, 1317, 1197, 1000],
    },
}

# -----------------------------
# Push-up and Squat thresholds
# Order: ["Excellent","Good","Average","Below Average","Poor"]
# -----------------------------

# Updated threshold order for push, squat, and body fat
threshold_order = ["Essential", "Excellent", "Good", "Average", "Below Average", "Poor"]


push_thresholds = {
    "Male": {
        "15-19": [39, 29, 23, 18, 0],
        "20-29": [36, 29, 22, 17, 0],
        "30-39": [30, 22, 17, 12, 0],
        "40-49": [25, 17, 13, 10, 0],
        "50-59": [21, 13, 10, 7, 0],
        "60-69": [18, 11, 8, 5, 0],
    },
    "Female": {
        "15-19": [33, 25, 18, 12, 0],
        "20-29": [30, 21, 15, 10, 0],
        "30-39": [27, 20, 13, 8, 0],
        "40-49": [24, 15, 11, 6, 0],
        "50-59": [21, 13, 7, 5, 0],
        "60-69": [17, 12, 5, 3, 0],
    },
}

squat_thresholds = {
    "Male": {
        "15-19": [60, 51, 41, 31, 30],
        "20-29": [55, 47, 38, 28, 27],
        "30-39": [50, 42, 34, 25, 24],
        "40-49": [45, 38, 30, 22, 21],
        "50-59": [40, 34, 26, 18, 17],
        "60-69": [35, 30, 22, 15, 14],
    },
    "Female": {
        "15-19": [50, 41, 31, 21, 20],
        "20-29": [45, 37, 28, 19, 18],
        "30-39": [40, 33, 24, 16, 15],
        "40-49": [35, 29, 20, 14, 13],
        "50-59": [30, 25, 18, 12, 11],
        "60-69": [25, 21, 15, 10, 9],
    },
}

# -----------------------------
# Plank percentiles (seconds)
# -----------------------------
plank_percentiles = {
    "Male":   [30, 45, 60, 75, 90, 105, 120, 150, 180, 210],
    "Female": [20, 35, 45, 60, 75, 90, 105, 120, 150, 180],
}

# -----------------------------
# One-Leg Stance (OLS) thresholds (seconds)
# -----------------------------
OLS_THRESHOLDS = {
    "Male": {
        "20-29": {"open": 44, "closed": 17},
        "30-39": {"open": 44, "closed": 17},
        "40-49": {"open": 42, "closed": 12},
        "50-59": {"open": 42, "closed": 9},
        "60-69": {"open": 34, "closed": 5},
    },
    "Female": {
        "20-29": {"open": 45, "closed": 13},
        "30-39": {"open": 45, "closed": 13},
        "40-49": {"open": 43, "closed": 13},
        "50-59": {"open": 41, "closed": 8},
        "60-69": {"open": 31, "closed": 4},
    },
}

# -----------------------------
# Toe Touch thresholds (cm)
# -----------------------------
TOE_TOUCH_THRESHOLDS = {
    "15-19": [0, 0, 5, 10],
    "20-29": [0, 1, 6, 11],
    "30-39": [0, 2, 7, 12],
    "40-49": [0, 3, 8, 13],
    "50-59": [0, 4, 9, 14],
    "60-69": [0, 5, 10, 15],
}

# -----------------------------
# Test units for display
# -----------------------------
TEST_UNITS = {
    "BMI": "kg/m²",
    "WHR": "",
    "BodyFat": "%",
    "ExplosivePower": "Watts",
    "PushUp": "reps",
    "Squat": "reps",
    "Plank": "seconds",
    "OLS": "seconds",
    "ToeTouch": "cm",
}

# -----------------------------
# Combined Test Constants for classification
# -----------------------------
TEST_CONSTANTS = {
    "PushUp": push_thresholds,
    "Squat": squat_thresholds,
    "Plank": plank_percentiles,
    "OLS": OLS_THRESHOLDS,
    "ToeTouch": TOE_TOUCH_THRESHOLDS,
    "BMI": None,      # special handling in classify_metric
    "BodyFat": BODY_FAT_TABLE
}
