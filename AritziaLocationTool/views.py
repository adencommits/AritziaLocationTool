from flask import Blueprint, render_template, request
import os
import json
import subprocess

from main import main
from Retail.main_retail import main_retail
from Retail.ai_model import run_model

views = Blueprint('views', __name__)

latitude = None
longitude = None


@views.route('/')
def home():
    return render_template('index.html')


@views.route('/distribution-centres')
def distribution_centres():
    return render_template('distribution-centres.html')


@views.route('/distribution-centres_results')
def distribution_centres_results():
    result = main()
    if result is None:
        result = {}  # or provide a default value
    return render_template('distribution-centres-results.html', result=result)


@views.route('/boutiques')
def boutiques():
    return render_template('boutiques.html')


@views.route('/a-ok-cafe')
def a_ok_cafe():
    return render_template('a-ok-cafe.html')


@views.route('/run_retail_scripts', methods=['GET'])
def run_retail_scripts():
    # Import the scripts

    # Run the main_retail script
    main_retail()

    # Run the ai_model script and get the output
    output = run_model()

    # Print the output to the console
    print(output)

    # Return a success message
    return 'Scripts executed successfully.', 200


@views.route('/run_main_script', methods=['GET'])
def run_main_script():
    result = main()
    return result


@views.route('/save_coordinates', methods=['POST'])
def save_coordinates():
    print(request.form)

    global latitude
    global longitude

    latitude = request.form.get('lat')  # Corrected from 'latitude' to 'lat'
    longitude = request.form.get('lng')  # Corrected from 'longitude' to 'lng'

    with open('coordinates.txt', 'w') as f:
        f.write(f'{latitude},{longitude}')

    print(f"Coordinates saved to file: {latitude}, {longitude}")

    return 'Coordinates saved successfully.'


@views.route('/boutique-results')
def boutique_results():
    data_string = main_retail()  # Ensure this reads the latest coordinates
    print(f"Data string from main_retail: {data_string}")  # Debug print
    data = json.loads(data_string)
    ai_prompt = run_model()
    ai_prompt = ai_prompt.replace(" - ", "<br>- ")
    return render_template('boutique-results.html', data=data, ai_prompt=ai_prompt)
