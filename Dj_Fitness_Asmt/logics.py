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
    return round((jump_height_cm * 9.81 * weight) / 1000, 2)

def calculate_body_fat(gender, age, skinfolds):
    sum_folds = sum(v for v in skinfolds.values() if v is not None)
    if gender.lower() == "male":
        # chest, abdomen, thigh
        density = 1.10938 - 0.0008267 * sum_folds + 0.0000016 * sum_folds**2 - 0.0002574 * age
    else:
        # triceps, suprailiac, thigh
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
    """
    Plot Ramp Test RPE vs Load with aerobic, moderate, and anaerobic zones.
    """
        
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(loads, rpe_values, marker='o', color='black', label='RPE')

    ax.set_xlabel("Load")
    ax.set_ylabel("RPE")
    ax.set_ylim(0, 10)

    # Convert lists to numpy arrays for easier filtering
    loads_arr = np.array(loads)
    rpes_arr = np.array(rpe_values)

    # Compute thresholds
    aerobic_mask = (rpes_arr > 2) & (rpes_arr <= 6)
    moderate_mask = (rpes_arr > 6) & (rpes_arr < 9)

    aerobic_thres = loads_arr[aerobic_mask].mean() if np.any(aerobic_mask) else None
    anaerobic_thres = loads_arr[moderate_mask].mean() if np.any(moderate_mask) else None

    # Plot threshold zones if computed
    if aerobic_thres is not None and anaerobic_thres is not None:
        ax.axvspan(min(loads), aerobic_thres, facecolor='lightgreen', alpha=0.3, label='Aerobic Zone')
        ax.axvspan(aerobic_thres, anaerobic_thres, facecolor='khaki', alpha=0.3, label='Moderate Zone')
        ax.axvspan(anaerobic_thres, max(loads), facecolor='lightcoral', alpha=0.3, label='Anaerobic Zone')

    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper left')
    fig.tight_layout()
    
    return save_plot_to_memory(fig)


# ----------------------
# TEST_CONSTANTS for classify_metric
# ----------------------
TEST_CONSTANTS = {
    "BMI": {"Male": [18.5, 25, 30], "Female": [18.5, 25, 30]},
    "vertical_jump_power":EXPLOSIVE_POWER_TABLE,
    "WHR": WHR_RANGES,
    "BodyFat": BODY_FAT_TABLE,
    "PushUp": push_thresholds,
    "Squat": squat_thresholds,
    "Plank": plank_percentiles,
    "OLS": OLS_THRESHOLDS,
    "ToeTouch": TOE_TOUCH_THRESHOLDS,
    "ExplosivePower": EXPLOSIVE_POWER_TABLE,
}

# ----------------------
# Classification
# ----------------------
def classify_metric(test_name, gender, age, value):
    gender_key = gender.capitalize()
    thresholds_dict = TEST_CONSTANTS.get(test_name)
    if not thresholds_dict:
        return None

    # OLS special case
    if test_name == "OLS":
        return "Good" if value >= 0 else "Poor"
    
    if test_name == "ToeTouch":
        # find correct age range
        matched_range = None
        for age_range in thresholds_dict:
            min_age, max_age = map(int, age_range.split("-"))
            if min_age <= age <= max_age:
                matched_range = age_range
                break
        if not matched_range:
            return None

        values = thresholds_dict[matched_range]

        # classification logic: higher = worse
        if value <= values[1]:
            return "Excellent"
        elif value <= values[2]:
            return "Good"
        elif value <= values[3]:
            return "Average"
        else:
            return "Poor"


    # Plank special
    if test_name == "Plank":
        perc = thresholds_dict.get(gender_key)
        if not perc: return None
        if value >= perc[8]: return "Excellent"
        elif value >= perc[6]: return "Good"
        elif value >= perc[4]: return "Average"
        elif value >= perc[2]: return "Below Average"
        return "Poor"

     # BMI special case
    if test_name == "BMI":
        if value < 18.5:
            return "Underweight"
        elif value < 25:
            return "Normal"
        elif value < 30:
            return "Overweight"
        else:
            return "Obese"
    # Standard thresholds
    age_ranges = thresholds_dict.get(gender_key)
    
    # If it's a dict (age ranges), find correct range
    if isinstance(age_ranges, dict):
        matched_range = None
        for age_range in age_ranges:
            if "-" in age_range:
                min_age, max_age = map(int, age_range.split("-"))
            else:
                min_age, max_age = int(age_range.replace("+","")), 200
            if min_age <= age <= max_age:
                matched_range = age_range
                break
        if not matched_range:
            return None
        values = age_ranges[matched_range]
    # If it's a list (no age ranges)
    elif isinstance(age_ranges, list):
        values = age_ranges
    else:
        return None

    order = threshold_order[1:] if test_name != "BodyFat" else threshold_order
    if test_name == "BodyFat":
        for i, threshold in enumerate(values):
            if value <= threshold:
                return order[i]
        return order[-1]
    else: 
        for i, threshold in enumerate(values):
            if value >= threshold:
                return order[i]
        return order[-1]


def overall_balance(ols_results: dict) -> str:
    """
    Takes the 4 OLS classifications and returns an overall balance score.
    Expected ols_results format:
    {
        "OLS_Open_Right": "Good",
        "OLS_Open_Left": "Poor",
        "OLS_Closed_Right": "Excellent",
        "OLS_Closed_Left": "Fair"
    }
    """
    
    values = list(ols_results.values())

    # Normalize (capitalize first letter only)
    normalized = [v.lower() for v in values]

    bad_count = sum(1 for v in normalized if v == "poor")

    if all(v == "good" or v == "excellent" for v in normalized):
        return "Excellent"
    elif bad_count == 0:  
        # No "poor" values but not all good/excellent → mix
        return "Good"
    elif bad_count == 1:
        return "Good"
    elif bad_count >= 2 and bad_count < 4:
        return "Below Average"
    elif bad_count == 4:
        return "Poor"

# ----------------------
# Master function
# ----------------------
def process_client_data(data):
    # Normalize gender
    gender_key = data["gender"].capitalize()  # "male" -> "Male"
    
    # Gender-specific skinfold selection
    if gender_key == "Male":
        skinfolds = {
            "chest": data.get("chest"),
            "abdomen": data.get("abdomen"),
            "thigh": data.get("thigh")
        }

    else:
        skinfolds = {
            "triceps": data.get("triceps"),
            "suprailiac": data.get("suprailiac"),
            "thigh": data.get("thigh")
        }


    # Calculations
    bmi = calculate_bmi(data["weight_kg"], data["height_cm"])
    whr = calculate_whr(data["waist_cm"], data["hip_cm"])
    body_fat = calculate_body_fat(data["gender"], data["age"], skinfolds)
    vertical_jump_power= calculate_whr(data["weight_kg"], data["vertical_jump_height_cm"])

    # Ramp Test
    ramp_loads = [float(x.strip()) for x in data["ramp_test_loads"].split(",")]
    ramp_rpe = [float(x.strip()) for x in data["ramp_test_rpes"].split(",")]

    # Classifications
    # Classifications
    classifications = {
        "BMI": classify_metric("BMI", data["gender"], data["age"], bmi),
        "WHR": classify_metric("WHR", data["gender"],  data["age"], whr),
        "Body Fat": classify_metric("BodyFat", data["gender"], data["age"], body_fat),
        "vertical_jump_power": classify_metric("vertical_jump_power", data["gender"], data["age"], vertical_jump_power)
        "PushUps": classify_metric("PushUp", data["gender"], data["age"], data["pushup_count"]),
        "Squats": classify_metric("Squat", data["gender"], data["age"], data["squat_count"]),
        "Plank": classify_metric("Plank", data["gender"], data["age"], data["plank_hold_seconds"]),
        "ToeTouch": classify_metric("ToeTouch", data["gender"], data["age"], data["toe_touch_cm"]),
    }

    # Compute balance separately
    ols_results = {
        "OLS_Open_Right": classify_metric("OLS", data["gender"], data["age"], data["one_leg_stance_rigth_eyes_open_sec"]),
        "OLS_Open_Left": classify_metric("OLS", data["gender"], data["age"], data["one_leg_stance_Left_eyes_open_sec"]),
        "OLS_Closed_Right": classify_metric("OLS", data["gender"], data["age"], data["one_leg_stance_rigth_eyes_closed_sec"]),
        "OLS_Closed_Left": classify_metric("OLS", data["gender"], data["age"], data["one_leg_stance_left_eyes_closed_sec"]),
    }

    # Add only overall balance to classifications
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

    # Plots
    plots = {
        "bmi_plot": plot_bmi_curve(data["weight_kg"], data["height_cm"]),
        "ramp_plot": plot_ramp_test(ramp_loads, ramp_rpe)
    }

    return {
        "calculations": {"BMI": bmi, "WHR": whr, "BodyFat": body_fat, "vertical_jump_power": vertical_jump_height_cm},
        "classifications": classifications,
        "circumferences": circumferences,
        "plots": plots
    }
