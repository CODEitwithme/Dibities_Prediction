

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages

import numpy as np
import os
from django.http import HttpResponse


def index(request):
     return render(request, 'index.html')
def about(request):
     return render(request,'about.html')
def home(request):
    return render(request, 'index.html')
def result(request):
    result = request.session.get('result')
    error = request.session.get('error')
    return render(request, 'result.html', {'prediction': result, 'error': error})





MODEL_PATH = os.path.join('static', 'savedmodel1.pkl')
model = None
MODEL_LOADED = False

import joblib


def load_model():
    global model, MODEL_LOADED
    try:
        model = joblib.load(MODEL_PATH)  # Update with the correct path to your model
        MODEL_LOADED = True
        print("Model loaded successfully.")
        print(f"Model type: {type(model)}")
        print(f"Model attributes: {dir(model)}")
    except Exception as e:
        MODEL_LOADED = False
        print(f"Error loading model: {e}")


def test_model():
    if not MODEL_LOADED:
        print("Model not loaded.")
        return

    try:
        # Example input_data; replace with actual data as needed
        input_data = [[0, 120, 70, 20, 80, 25.0, 0.5, 30]]

        # Print the model type and its available methods
        print(f"Model type: {type(model)}")
        print(f"Available methods: {dir(model)}")

        # Test with the method you think is correct
        if hasattr(model, 'predict'):
            prediction = model.predict(input_data)
        elif hasattr(model, 'prediction'):
            prediction = model.prediction(input_data)
        else:
            print("Model does not have the expected methods.")
            return

        print("Prediction:", prediction)
    except Exception as e:
        print(f"Error during prediction: {e}")


# Call the load_model and test_model functions
load_model()
test_model()


def prediction(request):
    if request.method == 'POST':
        error = None
        if not MODEL_LOADED:
            error = 'Model is not available. Please try again later.'
        else:
            try:
                # Validate and get form data
                required_fields = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'dpf', 'age']
                input_data = []
                for field in required_fields:
                    if field in request.POST and request.POST[field].strip():
                        input_data.append(float(request.POST[field]))
                    else:
                        error = f"Missing or invalid data for {field}"
                        break

                if error is None:
                    # Convert to numpy array
                    input_data = np.array([input_data])

                    # Make prediction
                    prediction = model.predict(input_data)

                    # Map the prediction to a readable format
                    result = 'Diabetic' if prediction[0] == 1 else 'Non-Diabetic'

                    # Store the result in the session
                    request.session['result'] = result
                    return redirect('result')

            except Exception as e:
                error = f"Error during prediction: {e}"
                request.session['error'] = error
                return redirect('result')

    return render(request, 'prediction.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if password.startswith('1'):
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to another page after login
        else:
            messages.error(request, 'Password must start with 1.')
            return render(request, 'login.html')

    return render(request, 'login.html')

def contact (request):
    return render(request,'contact.html')
def savedmodel(request):
    return HttpResponse("This is the savedmodel view.")