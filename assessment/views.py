# assessment/views.py
from django.shortcuts import render, redirect
from .forms import Session1Form, Session2Form, Session3Form, Session4Form
from Dj_Fitness_Asmt.logics import process_client_data   # master function

# ----------------------
# SESSION 1 
# ----------------------
def session1(request):
    if request.method == "POST":
        form = Session1Form(request.POST)
        if form.is_valid():
            request.session['session1_data'] = form.cleaned_data
            return redirect('session2')
    else:
        form = Session1Form()
    return render(request, "assessment/session1.html", {"form": form})


# ----------------------
# SESSION 2 
# ----------------------
def session2(request):
    gender = request.session.get('session1_data', {}).get('gender', None)
    if request.method == "POST":
        form = Session2Form(request.POST, gender=gender)
        if form.is_valid():
            request.session['session2_data'] = form.cleaned_data
            return redirect('session3')
    else:
        form = Session2Form(gender=gender)
    return render(request, "assessment/session2.html", {"form": form})


# ----------------------
# SESSION 3  (Ramp Test Only)
# ----------------------
def session3(request):
    if request.method == 'POST':
        ramp_rpes, ramp_loads = [], []
        for key in request.POST:
            if key.startswith("rpe_"):
                try:
                    ramp_rpes.append(float(request.POST[key]))
                    ramp_loads.append(int(key.split("_")[1]))  # load index from field name
                except ValueError:
                    pass

        if ramp_rpes:
            request.session['session3_data'] = {
                'ramp_test_rpes': ramp_rpes,
                'ramp_test_loads': ramp_loads,
            }
            return redirect('session4')

    return render(request, 'assessment/session3.html')


# ----------------------
# SESSION 4 (Power, Strength, Balance, Flexibility)
# ----------------------
def session4(request):
    if request.method == 'POST':
        form = Session4Form(request.POST)
        if form.is_valid():
            request.session['session4_data'] = form.cleaned_data
            return redirect('summary')
    else:
        form = Session4Form()

    return render(request, 'assessment/session4.html', {
        'form': form,
        'jump_fields': [form['vertical_jump_height_cm']],
        'endurance_fields_row1': [
            form['pushup_count'],
            form['squat_count'],
            form['plank_hold_seconds'],
            form['toe_touch_cm'],
        ],
        'endurance_fields_row2': [
            form['one_leg_stance_right_eyes_open_sec'],
            form['one_leg_stance_left_eyes_open_sec'],
            form['one_leg_stance_right_eyes_closed_sec'],
            form['one_leg_stance_left_eyes_closed_sec'],
        ],
    })


# ----------------------
# SUMMARY (Final Report)
# ----------------------
def summary(request):
    # Collect all session data
    session1_data = request.session.get('session1_data', {})
    session2_data = request.session.get('session2_data', {})
    session3_data = request.session.get('session3_data', {})
    session4_data = request.session.get('session4_data', {})

    # Combine data for processing
    combined_data = {**session1_data, **session2_data, **session3_data, **session4_data}

    # Add ramp_test_loads/rpes if not strings yet
    if 'ramp_test_loads' in session3_data and isinstance(session3_data['ramp_test_loads'], list):
        combined_data['ramp_test_loads'] = ",".join(map(str, session3_data['ramp_test_loads']))
    if 'ramp_test_rpes' in session3_data and isinstance(session3_data['ramp_test_rpes'], list):
        combined_data['ramp_test_rpes'] = ",".join(map(str, session3_data['ramp_test_rpes']))

    # Process client data to get classifications, plots, circumferences
    processed = process_client_data(combined_data)

    return render(request, 'assessment/summary.html', {
        'session1_data': session1_data,
        'session2_data': session2_data,
        'session3_data': processed['plots'],  # ramp_plot
        'session4_data': processed['plots'],  # bmi_plot
        'calculations': processed['calculations'],
        'classifications': processed['classifications'],
        'circumferences': processed['circumferences'],
    })
