from django import forms


# ----------------------
# SESSION 1 – Client Info & Basic Vitals
# ----------------------
class Session1Form(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=50)
    last_name = forms.CharField(label="Last Name", max_length=50)
    age = forms.IntegerField(label="Age", min_value=0)
    gender = forms.ChoiceField(
        label="Gender",
        choices=[("male", "Male"), ("female", "Female")]
    )
    height_cm = forms.FloatField(label="Height (cm)", min_value=0)
    weight_kg = forms.FloatField(label="Weight (kg)", min_value=0)
    resting_hr = forms.IntegerField(label="Resting Heart Rate (bpm)", min_value=0)
    systolic_bp = forms.IntegerField(label="Systolic BP (mmHg)", min_value=0)
    diastolic_bp = forms.IntegerField(label="Diastolic BP (mmHg)", min_value=0)


# ----------------------
# SESSION 2 – Body Composition & Anthropometrics
# ----------------------
class Session2Form(forms.Form):
    # Skinfolds
    chest = forms.FloatField(label="Chest (mm)", required=False)
    abdomen = forms.FloatField(label="Abdomen (mm)", required=False)
    thigh = forms.FloatField(label="Thigh (mm)", required=False)
    triceps = forms.FloatField(label="Triceps (mm)", required=False)
    suprailiac = forms.FloatField(label="Suprailiac (mm)", required=False)

    # Anthropometrics
    arms_rigth_cm = forms.FloatField(label="Right Biceps Circumference (cm)", min_value=0)
    arms_left_cm = forms.FloatField(label="Left Biceps Circumference (cm)", min_value=0)
    chest_cm = forms.FloatField(label="Chest Circumference (cm)", min_value=0)
    waist_cm = forms.FloatField(label="Waist Circumference (cm)", min_value=0)
    hip_cm = forms.FloatField(label="Hip Circumference (cm)", min_value=0)
    thigh_rigth_cm = forms.FloatField(label="Right Thigh Circumference (cm)", min_value=0)
    thigh_left_cm = forms.FloatField(label="Left Thigh Circumference (cm)", min_value=0)

    def __init__(self, *args, **kwargs):
        gender = kwargs.pop('gender', None)
        super().__init__(*args, **kwargs)

        if gender == 'male':
            for field in ['triceps', 'suprailiac']:
                self.fields.pop(field, None)
        elif gender == 'female':
            for field in ['chest', 'abdomen']:
                self.fields.pop(field, None)


# ----------------------
# SESSION 3 – Aerobic (Ramp Test)
# ----------------------
class Session3Form(forms.Form):
    ramp_test_loads = forms.CharField(
        label="Ramp Test Loads (comma-separated watts)",
        help_text="Example: 50,75,100,125,150"
    )
    ramp_test_rpes = forms.CharField(
        label="Ramp Test RPEs (comma-separated, match loads)",
        help_text="Example: 2,4,6,8,10"
    )


# ----------------------
# SESSION 4 – Power, Strength, Balance, Flexibility
# ----------------------
class Session4Form(forms.Form):
    # Explosive Power – Jump Height
    vertical_jump_height_cm = forms.FloatField(label="Vertical Jump-Height Distance (cm)", min_value=0)

    # Muscular Endurance Tests
    pushup_count = forms.IntegerField(label="Push-Up Test - Reps", min_value=0)
    squat_count = forms.IntegerField(label="Squat Test - Reps", min_value=0)
    plank_hold_seconds = forms.IntegerField(label="Plank Test - Seconds", min_value=0)

    # Balance
    one_leg_stance_rigth_eyes_open_sec = forms.FloatField(label="Right-Leg-Eyes-Open (s)", min_value=0)
    one_leg_stance_Left_eyes_open_sec = forms.FloatField(label="Left-Leg-Eyes-Open (s)", min_value=0)
    one_leg_stance_rigth_eyes_closed_sec = forms.FloatField(label="Right-Leg-Eyes-Closed (s)", min_value=0)
    one_leg_stance_left_eyes_closed_sec = forms.FloatField(label="Left-Leg-Eyes-Closed (s)", min_value=0)

    # Flexibility
    toe_touch_cm = forms.FloatField(label="Toe Touch Test (cm)", min_value=0)
