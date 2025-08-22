# Dj_Fitness_Asmt/logics.py

import matplotlib
matplotlib.use("Agg")  # prevent GUI backend errors in Django
import io
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from .constants import (
    BMI_CATEGORIES, WHR_RANGES, BODY_FAT_TABLE, EXPLOSIVE_POWER_TABLE,
    push_thresholds, squat_thresholds, plank_percentiles,
    OLS_THRESHOLDS, TOE_TOUCH_THRESHOLDS, threshold_order, TEST_UNITS
)

# ----------------------
# Helper functions
# ----------------------
def save_plot_to_memory(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    base64_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return base64_img

# ----------------------
# Calculations
# ----------------------
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 2)

def calculate_whr(waist, hip):
    return round(waist / hip, 2)

def calculate_power(weight, jump_height_cm):
    return round((jump_height_cm * 60.7) + (45.3 * weight) - 2055, 2)

def calculate_body_fat(gender, age, skinfolds):
    sum_folds = sum(v for v in skinfolds.values() if v is not None)
    if gender.lower() == "male":
        density = 1.10938 - 0.0008267 * sum_folds + 0.0000016 * sum_folds**2 - 0.0002574 * age
    else:
        density = 1.0994921 - 0.0009929 * sum_folds + 0.0000023 * sum_folds**2 - 0.0001392 * age
    body_fat = (495 / density) - 450
    return round(body_fat, 2)

# ----------------------
# Plotting functions
# ----------------------
def plot_bmi_curve(weight_kg, height_cm):
    heights = list(range(140, 200))
    heights_m = [h / 100 for h in heights]
    under = [18.5*(h**2) for h in heights_m]
    ideal = [22*(h**2) for h in heights_m]
    over = [25*(h**2) for h in heights_m]
    BMI = calculate_bmi(weight_kg, height_cm)

    fig, ax = plt.subplots(figsize=(4,3))
    ax.plot(under, heights, '--', color='blue', label='Underweight 18.5')
    ax.plot(ideal, heights, '-', color='green', label='Ideal 22')
    ax.plot(over, heights, '--', color='red', label='Overweight 25')
    ax.scatter(weight_kg, height_cm, color='black', label=f"You - {BMI}")
    ax.set_xlabel("Weight (kg)")
    ax.set_ylabel("Height (cm)")
    ax.grid(True)
    ax.legend(fontsize=6)
    fig.tight_layout()
    return save_plot_to_memory(fig)


def plot_ramp_test(loads, rpe_values):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(loads, rpe_values, marker='o', color='black', label='RPE')
    ax.set_xlabel("Load")
    ax.set_ylabel("RPE")
    ax.set_ylim(0, 10)

    loads_arr = np.array(loads)
    rpes_arr = np.array(rpe_values)

    aerobic_mask = (rpes_arr > 2) & (rpes_arr <= 6)
    moderate_mask = (rpes_arr > 6) & (rpes_arr < 9)

    aerobic_thres = loads_arr[aerobic_mask].mean() if np.any(aerobic_mask) else None
    anaerobic_thres = loads_arr[moderate_mask].mean() if np.any(moderate_mask) else None

    if aerobic_thres is not None and anaerobic_thres is not None:
        ax.axvspan(min(loads), aerobic_thres, facecolor='lightgreen', alpha=0.3, label='Aerobic Zone')
        ax.axvspan(aerobic_thres, anaerobic_thres, facecolor='khaki', alpha=0.3, label='Moderate Zone')
        ax.axvspan(anaerobic_thres, max(loads), facecolor='lightcoral', alpha=0.3, label='Anaerobic Zone')

    # Force all load values as xticks
    ax.set_xticks(loads)
    ax.set_xticklabels([str(int(l)) if l.is_integer() else str(l) for l in loads], rotation=45)

    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper left')
    fig.tight_layout()
    return save_plot_to_memory(fig)



# ----------------------
# TEST_CONSTANTS
# ----------------------
TEST_CONSTANTS = {
    "BMI": {"Male": [18.5, 25, 30], "Female": [18.5, 25, 30]},
    "vertical_jump_power": EXPLOSIVE_POWER_TABLE,
    "WHR": WHR_RANGES,
    "BodyFat": BODY_FAT_TABLE,
    "PushUp": push_thresholds,
    "Squat": squat_thresholds,
    "Plank": plank_percentiles,
    "OLS": OLS_THRESHOLDS,  # expects nested dict by gender → age → {"open":val, "closed":val}
    "ToeTouch": TOE_TOUCH_THRESHOLDS,
}

# ----------------------
# Helpers
# ----------------------
def get_age_range(age, thresholds_dict):
    for age_range in thresholds_dict:
        min_age, max_age = map(int, age_range.split("-"))
        if min_age <= age <= max_age:
            return age_range
    return None

# ----------------------
# Classification
# ----------------------
def classify_metric(test_name, gender, age, value, condition=None):
    gender_key = gender.capitalize()
    thresholds_dict = TEST_CONSTANTS.get(test_name)
    if not thresholds_dict:
        return None

    # OLS
    if test_name == "OLS":
        matched_range = get_age_range(age, thresholds_dict.get(gender_key, {}))
        if not matched_range or not condition:
            return None
        threshold_value = thresholds_dict[gender_key][matched_range][condition]
        return "Good" if value >= threshold_value else "Poor"

    # ToeTouch
    if test_name == "ToeTouch":
        matched_range = get_age_range(age, thresholds_dict)
        if not matched_range:
            return None
        values = thresholds_dict[matched_range]
        if value <= values[1]: return "Excellent"
        elif value <= values[2]: return "Good"
        elif value <= values[3]: return "Average"
        else: return "Poor"

    # Plank
    if test_name == "Plank":
        perc = thresholds_dict.get(gender_key)
        if not perc: return None
        if value >= perc[7]: return "Excellent"
        elif value >= perc[5]: return "Good"
        elif value >= perc[3]: return "Average"
        elif value >= perc[1]: return "Below Average"
        return "Poor"

    # BMI
    if test_name == "BMI":
        if value < 18.5: return "Underweight"
        elif value < 25: return "Normal"
        elif value < 30: return "Overweight"
        else: return "Obese"

    # Standard thresholds
    age_ranges = thresholds_dict.get(gender_key)
    if isinstance(age_ranges, dict):
        matched_range = get_age_range(age, age_ranges)
        if not matched_range:
            return None
        values = age_ranges[matched_range]
    elif isinstance(age_ranges, list):
        values = age_ranges
    else:
        return None

    order = threshold_order[1:] if test_name != "BodyFat" else threshold_order
    if test_name == "BodyFat":
        for i, threshold in enumerate(values):
            if value <= threshold: return order[i]
        return order[-1]
    else:
        for i, threshold in enumerate(values):
            if value >= threshold: return order[i]
        return order[-1]

# ----------------------
# OLS Overall Balance
# ----------------------
def overall_balance(ols_results: dict) -> str:
    values = list(ols_results.values())
    normalized = [v.lower() for v in values if v]
    bad_count = sum(1 for v in normalized if v == "poor")

    if all(v in ("good", "excellent") for v in normalized):
        return "Excellent"
    elif bad_count == 1:
        return "Good"
    elif 2 <= bad_count < 4:
        return "Below Average"
    elif bad_count == 4:
        return "Poor"
    return "Average"

# ----------------------
# Master
# ----------------------
def process_client_data(data):
    gender_key = data.get("gender", "").capitalize()

    if not gender_key:
        return {}

    # skinfolds
    if gender_key == "Male":
        skinfolds = { "chest": data.get("chest"), "abdomen": data.get("abdomen"), "thigh": data.get("thigh") }
    else:
        skinfolds = { "triceps": data.get("triceps"), "suprailiac": data.get("suprailiac"), "thigh": data.get("thigh") }

    bmi = calculate_bmi(data["weight_kg"], data["height_cm"])
    whr = calculate_whr(data["waist_cm"], data["hip_cm"])
    body_fat = calculate_body_fat(data["gender"], data["age"], skinfolds)
    vertical_jump_power = calculate_power(data["weight_kg"], data["vertical_jump_height_cm"])

    ramp_loads = [float(x.strip()) for x in data["ramp_test_loads"].split(",")]
    ramp_rpe = [float(x.strip()) for x in data["ramp_test_rpes"].split(",")]

    classifications = {
        "BMI": classify_metric("BMI", data["gender"], data["age"], bmi),
        "WHR": classify_metric("WHR", data["gender"], data["age"], whr),
        "Body Fat": classify_metric("BodyFat", data["gender"], data["age"], body_fat),
        "vertical_jump_power": classify_metric("vertical_jump_power", data["gender"], data["age"], vertical_jump_power),
        "PushUps": classify_metric("PushUp", data["gender"], data["age"], data["pushup_count"]),
        "Squats": classify_metric("Squat", data["gender"], data["age"], data["squat_count"]),
        "Plank": classify_metric("Plank", data["gender"], data["age"], data["plank_hold_seconds"]),
        "ToeTouch": classify_metric("ToeTouch", data["gender"], data["age"], data["toe_touch_cm"]),
    }

    ols_results = {
        "OLS_Open_Right": classify_metric("OLS", data["gender"], data["age"], data["one_leg_stance_right_eyes_open_sec"], condition="open"),
        "OLS_Open_Left": classify_metric("OLS", data["gender"], data["age"], data["one_leg_stance_left_eyes_open_sec"], condition="open"),
        "OLS_Closed_Right": classify_metric("OLS", data["gender"], data["age"], data["one_leg_stance_right_eyes_closed_sec"], condition="closed"),
        "OLS_Closed_Left": classify_metric("OLS", data["gender"], data["age"], data["one_leg_stance_left_eyes_closed_sec"], condition="closed"),
    }
    classifications["Overall Balance"] = overall_balance(ols_results)

    circumferences = {
        "chest_cm": data["chest_cm"],
        "waist_cm": data["waist_cm"],
        "hip_cm": data["hip_cm"],
        "arm_left_cm": data["arms_left_cm"],
        "arm_right_cm": data["arms_rigth_cm"],
        "thigh_left_cm": data["thigh_left_cm"],
        "thigh_right_cm": data["thigh_rigth_cm"]
    }

    plots = {
        "bmi_plot": plot_bmi_curve(data["weight_kg"], data["height_cm"]),
        "ramp_plot": plot_ramp_test(ramp_loads, ramp_rpe)
    }

    return {
        "calculations": {"BMI": bmi, "WHR": whr, "BodyFat": body_fat, "vertical_jump_power": vertical_jump_power},
        "classifications": classifications,
        "circumferences": circumferences,
        "plots": plots
    }
