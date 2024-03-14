from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"

related_model = BertForSequenceClassification.from_pretrained("FedericoDamboreana/stdb_related_question_classification")
related_tokenizer = BertTokenizer.from_pretrained("FedericoDamboreana/stdb_related_question_classification")

chained_model = BertForSequenceClassification.from_pretrained("FedericoDamboreana/chained_question_classification")
chained_tokenizer = BertTokenizer.from_pretrained("FedericoDamboreana/chained_question_classification")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
related_model.to(device)
chained_model.to(device)

print(">>> model loaded on: ", device)

def is_related(question):
    inputs = related_tokenizer(question, return_tensors='pt', padding=True, truncation=True)
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    related_model.eval()

    with torch.no_grad():
        outputs = related_model(input_ids, attention_mask=attention_mask)

    _, predicted_class = torch.max(outputs.logits, dim=1)
    return 1 - predicted_class.item()

def is_chained(question):
    inputs = chained_tokenizer(question, return_tensors='pt', padding=True, truncation=True)
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    chained_model.eval()

    with torch.no_grad():
        outputs = chained_model(input_ids, attention_mask=attention_mask)

    _, predicted_class = torch.max(outputs.logits, dim=1)
    return predicted_class.item()

@app.route('/related', methods=['POST'])
@cross_origin()
def related():
    data = request.json
    question = data['question']
    prediction = is_related(question)

    result = {
        'result': prediction, 
        'is_related': prediction == 1
    }

    return jsonify(result)

@app.route('/chained', methods=['POST'])
@cross_origin()
def chained():
    data = request.json
    question = data['question']
    prediction = is_chained(question)

    result = {
        'result': prediction, 
        'is_chained': prediction == 1
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)