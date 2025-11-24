from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
MODEL_PATH = os.path.join('models', 'final_model.pkl')

model = None

def load_model():
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print(f"✓ Model loaded successfully from {MODEL_PATH}")
            return True
        else:
            print(f"✗ Model file not found at: {MODEL_PATH}")
            print(f"   Current directory: {os.getcwd()}")
            print(f"   Looking for: {os.path.abspath(MODEL_PATH)}")
            return False
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False

# Try to load model at startup
load_model()

@app.route('/', methods=['GET'])
def home():
    """Home endpoint - confirms API is running"""
    return jsonify({
        'message': 'Supply Chain Emissions Prediction API',
        'status': 'running',
        'version': '1.0',
        'model_loaded': model is not None,
        'current_directory': os.getcwd(),
        'model_path': os.path.abspath(MODEL_PATH),
        'endpoints': {
            'GET /': 'API information',
            'GET /health': 'Health check',
            'POST /predict': 'Make prediction',
            'POST /batch-predict': 'Batch predictions',
            'GET /model-info': 'Model information',
            'POST /reload-model': 'Reload model'
        }
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': pd.Timestamp.now().isoformat()
    }), 200

@app.route('/reload-model', methods=['POST'])
def reload_model():
    """Reload the model"""
    success = load_model()
    return jsonify({
        'success': success,
        'model_loaded': model is not None,
        'message': 'Model reloaded successfully' if success else 'Failed to reload model'
    }), 200 if success else 500

@app.route('/predict', methods=['POST'])
def predict():
    """Make a single prediction"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please check if final_model.pkl exists in models/ directory',
            'model_path': os.path.abspath(MODEL_PATH),
            'success': False
        }), 500
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No JSON data provided',
                'success': False
            }), 400
        
        # Expected feature names in order
        feature_names = [
            'Substance',
            'Unit',
            'Supply Chain Emission Factors without Margins',
            'Margins of Supply Chain Emission Factors',
            'DQ ReliabilityScore of Factors without Margins',
            'DQ TemporalCorrelation of Factors without Margins',
            'DQ TechnologicalCorrelation of Factors without Margins',
            'Source'
        ]
        
        # Extract features in correct order
        features = []
        missing_features = []
        
        for feature in feature_names:
            if feature not in data:
                missing_features.append(feature)
            else:
                features.append(data[feature])
        
        if missing_features:
            return jsonify({
                'error': f'Missing required features: {missing_features}',
                'required_features': feature_names,
                'success': False
            }), 400
        
        # Convert to numpy array and reshape for prediction
        input_array = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(input_array)[0]
        
        # Return prediction
        return jsonify({
            'prediction': float(prediction),
            'input_features': data,
            'success': True
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'error_type': type(e).__name__,
            'success': False
        }), 400

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Handle multiple predictions at once"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'predictions' not in data:
            return jsonify({
                'error': 'Invalid request format. Expected {"predictions": [...]}'
            }), 400
        
        predictions_list = []
        
        feature_names = [
            'Substance',
            'Unit',
            'Supply Chain Emission Factors without Margins',
            'Margins of Supply Chain Emission Factors',
            'DQ ReliabilityScore of Factors without Margins',
            'DQ TemporalCorrelation of Factors without Margins',
            'DQ TechnologicalCorrelation of Factors without Margins',
            'Source'
        ]
        
        for idx, item in enumerate(data.get('predictions', [])):
            try:
                features = [item[feature] for feature in feature_names]
                input_array = np.array(features).reshape(1, -1)
                prediction = model.predict(input_array)[0]
                
                predictions_list.append({
                    'index': idx,
                    'input': item,
                    'prediction': float(prediction),
                    'success': True
                })
            except Exception as e:
                predictions_list.append({
                    'index': idx,
                    'input': item,
                    'error': str(e),
                    'success': False
                })
        
        return jsonify({
            'predictions': predictions_list,
            'count': len(predictions_list),
            'success': True
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

@app.route('/model-info', methods=['GET'])
def model_info():
    """Return information about the model"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded',
            'success': False
        }), 500
    
    return jsonify({
        'model_type': str(type(model).__name__),
        'n_estimators': getattr(model, 'n_estimators', 'N/A'),
        'max_depth': getattr(model, 'max_depth', 'N/A'),
        'min_samples_split': getattr(model, 'min_samples_split', 'N/A'),
        'features': [
            'Substance',
            'Unit',
            'Supply Chain Emission Factors without Margins',
            'Margins of Supply Chain Emission Factors',
            'DQ ReliabilityScore of Factors without Margins',
            'DQ TemporalCorrelation of Factors without Margins',
            'DQ TechnologicalCorrelation of Factors without Margins',
            'Source'
        ],
        'feature_count': 8,
        'success': True
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested URL was not found on the server',
        'available_endpoints': {
            'GET /': 'API information',
            'GET /health': 'Health check',
            'POST /predict': 'Make prediction',
            'POST /batch-predict': 'Batch predictions',
            'GET /model-info': 'Model information'
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Supply Chain Emissions Prediction API")
    print("="*60)
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"📦 Model path: {os.path.abspath(MODEL_PATH)}")
    print(f"✓ Model loaded: {'Yes' if model else 'No'}")
    
    if not model:
        print("\n⚠️  WARNING: Model not loaded!")
        print(f"   Please ensure final_model.pkl is at: {os.path.abspath(MODEL_PATH)}")
        print(f"   Current files in models/:")
        if os.path.exists('models'):
            files = os.listdir('models')
            for f in files:
                print(f"   - {f}")
        else:
            print("   - models/ directory not found!")
    
    print("\n🌐 Server starting on: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)