import os
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_guide', methods=['POST'])
def generate_guide():
    data = request.json
    topic = data.get('topic')
    subject = data.get('subject')
    level = data.get('level', 'high school')

    prompt = f"""Create a comprehensive study guide for the topic '{topic}' in {subject} at {level} level. 
    Structure it with:
    1. Introduction (overview and importance)
    2. Key Concepts (clear definitions)
    3. Detailed Explanations
    4. Real-world Examples
    5. Practice Questions with solutions
    6. Summary of main points
    Use clear headings and formatting for readability."""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a knowledgeable and patient study assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return jsonify({'guide': response['choices'][0]['message']['content']})

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    data = request.json
    topic = data.get('topic')
    subject = data.get('subject')
    difficulty = data.get('difficulty', 'medium')

    prompt = f"""Generate a 5-question multiple choice quiz on '{topic}' in {subject} at {difficulty} difficulty level.
    For each question:
    - Provide 4 options (A-D)
    - Mark the correct answer with an asterisk
    - Include a brief explanation of why it's correct
    Format each question like:
    1. [Question text]
       A) Option 1
       B) Option 2
       C) Option 3*
       D) Option 4
       Explanation: [Explanation text]"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a quiz generator that creates fair, educational assessments."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return jsonify({'quiz': response['choices'][0]['message']['content']})

if __name__ == '__main__':
    app.run(debug=True)