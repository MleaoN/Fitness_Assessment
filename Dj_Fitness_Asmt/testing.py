import pandas as pd
import numpy as np
from pathlib import Path
from io import BytesIO
from PIL import Image
import base64

from Dj_Fitness_Asmt.logics import (
    generate_threshold_tables,
    plot_bmi_curve,
    plot_ramp_test
)
from Dj_Fitness_Asmt.constants import (
    BODY_FAT_TABLE,
    EXPLOSIVE_POWER_TABLE,
    push_thresholds,
    squat_thresholds,
    plank_percentiles,
    OLS_THRESHOLDS,
    TOE_TOUCH_THRESHOLDS,
    BMI_CATEGORIES
)

def save_base64_image(img_base64, filename):
    """Convert Base64 string to image file."""
    img_bytes = BytesIO(base64.b64decode(img_base64))
    img = Image.open(img_bytes)
    img.save(filename)

def test_tables_and_plots():
    output_dir = Path("test_outputs")
    output_dir.mkdir(exist_ok=True)

    print("=== Testing Threshold Tables ===")
    tables = generate_threshold_tables()
    for test_name, df in tables.items():
        print(f"[OK] {test_name} table generated with {len(df)} rows.")
        df.to_csv(output_dir / f"{test_name}_table.csv", index=False)

    # Test BMI plot
    print("=== Testing BMI Plot ===")

    weight_kg = 75  # example weight
    height_cm = 175  # example height
    bmi_plot_buf = plot_bmi_curve(weight_kg, height_cm)

    # Save the plot
    # Correct way to open the BytesIO buffer
    bmi_plot_buf.seek(0)  # ensure buffer is at the start
    img = Image.open(bmi_plot_buf)
    img.save(output_dir / "bmi_plot.png")

    print("[OK] BMI plot saved.")

    # Test Ramp Test plot
    print("=== Testing Ramp Test Plot ===")
    ramp_loads = [50, 100, 150, 200, 250]
    rpe_values = [2, 4, 6, 8, 10]
    ramp_plot_base64 = plot_ramp_test(ramp_loads, rpe_values)
    save_base64_image(ramp_plot_base64, output_dir / "ramp_test_plot.png")
    print("[OK] Ramp test plot saved.")

    print(f"All test files saved to: {output_dir.resolve()}")

if __name__ == "__main__":
    test_tables_and_plots()
