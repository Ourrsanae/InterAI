from flask import Blueprint, render_template, request, jsonify
import google.generativeai as genai
import re

import pandas as pd 
import json
import plotly
import plotly.express as px

genai.configure(api_key="your_gemini_api_key_here")

#home_bp = Blueprint('home', __name__)
home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route("/")
def index():
       
    df = px.data.medals_wide()
    fig1 = px.bar(df, x="nation", y=['gold', 'silver', 'bronze'], title="Wide-form Input")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    df = px.data.iris()
    fig2 = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width', color='petal_length', symbol='species')
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    df = px.data.gapminder().query("continent=='Oceania'")
    fig3 = px.line(df, x="year", y="lifeExp", color='country',  title="Life Expectancy")
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graph1JSON=graph1JSON,  graph2JSON=graph2JSON, graph3JSON=graph3JSON)

def read_csv_from_request(file):
    df = pd.read_csv(file)
    return df.to_string(index=False), df

def read_excel_from_request(file):
    df = pd.read_excel(file)
    return df.to_string(index=False), df

def create_interpretation_prompt(csv_data):
    prompt = f"""
    Given the following data:
    {csv_data}

    Interpret the data and provide insights or patterns you observe with more details.
    """
    return prompt


def format_interpretation_text(text):
    # Format main headings (h1) with large size and bold style
    text = re.sub(r'(?m)^# (.+)', r'<h1 style="font-size: 36px; font-weight: bold; color: #333; margin-bottom: 20px;"><strong>\1</strong></h1>', text)

    # Format subheadings (h2) with a slightly smaller but still bold style
    text = re.sub(r'(?m)^## (.+)', r'<h2 style="font-size: 28px; font-weight: bold; color: #444; margin-bottom: 16px;">\1</h2>', text)

    # Format bold text wrapped in double asterisks
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    # Handle paragraph separation without wrapping everything inside a <p> tag
    text = re.sub(r'\n\n+', '</p><p>', text)

    # Convert single newlines to line breaks
    text = re.sub(r'\n', '<br>', text)

    # Return the final text with no extra wrapping, allowing the HTML tags to control formatting
    return text


'''def interpret_data(data):
    try:
        prompt = create_interpretation_prompt(data)
        response = genai.generate(prompt=prompt)
        interpretation_text = response.generations[0].text.strip()
        formatted_interpretation = format_interpretation_text(interpretation_text)
        return formatted_interpretation
    except Exception as e:
        print(f"Erreur lors du traitement du fichier : {str(e)}")
        return f"Erreur lors du traitement du fichier : {str(e)}"
'''
'''def interpret_data(data):
    try:
        prompt = create_interpretation_prompt(data)
        response = genai.generate_text(prompt=prompt)
        print("Réponse brute de l'API Gemini:", response)
        #interpretation_text = response.generations[0].text.strip()
        interpretation_text = response.result #.text.strip()
        formatted_interpretation = format_interpretation_text(interpretation_text)
        return formatted_interpretation
    except Exception as e:
        print(f"Erreur lors du traitement du fichier : {str(e)}")
        return f"Erreur lors du traitement du fichier : {str(e)}"
'''
def interpret_data(data):
    try:
        prompt = create_interpretation_prompt(data)
        model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "text/plain"})
        response = model.generate_content(prompt)
        interpretation_text = response.text.strip()
        formatted_interpretation = format_interpretation_text(interpretation_text)
        return formatted_interpretation
    except Exception as e:
        print(f"Erreur lors du traitement du fichier : {str(e)}")
        return f"Erreur lors du traitement du fichier : {str(e)}"

@home_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            if file.filename.endswith('.csv'):
                data, df = read_csv_from_request(file)
            elif file.filename.endswith('.xls') or file.filename.endswith('.xlsx'):
                data, df = read_excel_from_request(file)
            else:
                print("Format de fichier non valide")
                return jsonify({"error": "Format de fichier non valide"}), 400

            interpretation = interpret_data(data)

            # Sauvegarde du fichier CSV pour la visualisation
            df.to_csv('test.csv', index=False)

            # Extraction des colonnes pour l'affichage dans la page de visualisation
            columns = df.columns.tolist()

            # Redirection vers la page de visualisation en passant les colonnes
            return render_template('home/visualization.html', columns=columns, interpretation=interpretation)
        
    # Si la méthode est GET ou si aucun fichier n'est reçu
    print("Affichage du formulaire d'upload")
    return render_template('home/upload.html', title='Upload')
@home_bp.route('/visualization', methods=['POST'])
def visualization():
    plot_type = request.form['plot_type']
    x_axis = request.form['x_axis']
    y_axis = request.form['y_axis']
    z_axis = request.form.get('z_axis')  # z_axis peut être None si non applicable

    # Charger le fichier CSV
    df = pd.read_csv('test.csv')
    
    # Génération du graphique
    if plot_type == 'bar':
        fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Chart")
    elif plot_type == 'scatter_3d':
        fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, title="3D Scatter Plot")
    elif plot_type == 'line':
        fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
    else:
        return jsonify({"error": "Type de graphique non valide"}), 400

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Génération de la conclusion
    summary = interpret_data(df.to_string(index=False))  # Utiliser votre fonction d'interprétation

    return render_template('home/visualization.html', graphJSON=graphJSON, summary=summary)
