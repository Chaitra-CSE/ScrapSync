import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import os

class WasteClassifier:
    def __init__(self):
        """Load MobileNetV2 model for waste classification"""
        
        # Suppress TensorFlow warnings
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        tf.get_logger().setLevel('ERROR')
        
        # Look for model in multiple locations
        model_paths = [
            'models/mobilenetv2_garbage.h5',
            '../Garbage-Classification-Using-MobileNetV2/models/mobilenetv2_garbage.h5',
            'mobilenetv2_garbage.h5'
        ]
        
        self.model = None
        for path in model_paths:
            if os.path.exists(path):
                print(f"✅ Loading model from {path}")
                self.model = tf.keras.models.load_model(path)
                break
        
        # If no model found, create the architecture
        if self.model is None:
            print("🔄 Creating MobileNetV2 model with pre-trained weights...")
            self.model = self._create_mobilenetv2()
        
        # Class names (matches the model output)
        self.class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        
        # Map to ScrapSync categories
        self.category_mapping = {
            'cardboard': 'Paper',
            'paper': 'Paper',
            'plastic': 'Plastic',
            'metal': 'Metal',
            'glass': 'Recyclable',
            'trash': 'Other'
        }
        
        # Prices per kg (₹)
        self.prices = {
            'Paper': 15,
            'Plastic': 20,
            'Metal': 45,
            'Recyclable': 10,
            'Other': 2
        }
        
        print("✅ ScrapSync AI Ready!")
        print(f"📊 Model loaded with {len(self.model.layers)} layers")
    
    def _create_mobilenetv2(self):
        """Create MobileNetV2 model with transfer learning"""
        
        # Load pre-trained MobileNetV2
        base_model = tf.keras.applications.MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        # Freeze base model
        base_model.trainable = False
        
        # Build classification head
        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(6, activation='softmax')
        ])
        
        # Compile
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def preprocess_image(self, image):
        """Preprocess image for MobileNetV2 input"""
        
        # Convert PIL to numpy array if needed
        if isinstance(image, Image.Image):
            image = image.convert('RGB')
            image = np.array(image)
            
        # Ensure RGB format for raw numpy arrays
        if len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        elif len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            if image[0,0,0] > image[0,0,2]:  # Simple check if BGR
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize to 224x224 (MobileNetV2 input size)
        image = cv2.resize(image, (224, 224))
        
        # Normalize to [0,1]
        image = image.astype('float32') / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def predict(self, image):
        """Predict waste category from image"""
        
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Get predictions
        predictions = self.model.predict(processed_image, verbose=0)
        
        # Get class with highest probability
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        
        # Get class name
        predicted_class = self.class_names[class_idx]
        mapped_category = self.category_mapping[predicted_class]
        price_per_kg = self.prices[mapped_category]
        
        # Determine confidence level
        if confidence > 0.8:
            confidence_level = "🟢 Very High"
        elif confidence > 0.6:
            confidence_level = "🟡 High"
        elif confidence > 0.4:
            confidence_level = "🟠 Medium"
        else:
            confidence_level = "🔴 Low"
        
        # Return results
        return {
            'predicted_class': predicted_class,
            'predicted_class_upper': predicted_class.upper(),
            'confidence': confidence,
            'confidence_percent': f"{confidence*100:.1f}%",
            'confidence_level': confidence_level,
            'mapped_category': mapped_category,
            'price_per_kg': price_per_kg,
            'all_probabilities': {
                name: float(prob) 
                for name, prob in zip(self.class_names, predictions[0])
            }
        }