from flask import Flask, request, render_template, jsonify, redirect, url_for
from modules.llm_provider import LLMProvider
from modules.story_processor import SimpleStoryProcessor
from modules.corpus_manager import process_entire_corpus
from modules.visualization import prepare_visualization_data, export_for_html_visualization
import os

app = Flask(__name__)

API_KEYS = {}
CORPUS_DIR = os.path.join(os.getcwd(), 'corpus_uploads')
os.makedirs(CORPUS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api_keys', methods=['GET', 'POST'])
def api_keys():
    if request.method == 'POST':
        provider = request.form['provider']
        key = request.form['key']
        API_KEYS[provider] = key
        return redirect(url_for('api_keys'))
    return render_template('api_keys.html', api_keys=API_KEYS)

@app.route('/upload_corpus', methods=['POST'])
def upload_corpus():
    file = request.files['corpus_file']
    if file:
        filepath = os.path.join(CORPUS_DIR, file.filename)
        file.save(filepath)
        return jsonify({'status': 'success', 'filename': file.filename})
    return jsonify({'status': 'error'})

@app.route('/process_corpus', methods=['POST'])
def process_corpus():
    provider = request.form.get('provider', 'ollama')
    model = request.form.get('model', 'gpt-oss-32k')
    llm = LLMProvider(provider, model, API_KEYS)
    processor = SimpleStoryProcessor(llm)
    results = process_entire_corpus(CORPUS_DIR, processor)
    viz_data = prepare_visualization_data(results)
    json_file = export_for_html_visualization(viz_data)
    return jsonify({'status': 'complete', 'json_file': str(json_file)})

@app.route('/visualization')
def visualization():
    json_path = os.path.join(os.getcwd(), 'scene_analysis_visualization.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = f.read()
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
