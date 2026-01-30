# Archivo: food_analyzer.py
# Tecnología: Python con la librería de Google Cloud Vision

# --- Requisitos para que funcione ---
# 1. Instalar la librería: pip install google-cloud-vision
# 2. Configurar la autenticación de Google Cloud en tu entorno.

from google.cloud import vision
import io

# --- SIMULACIÓN DE BASE DE DATOS NUTRICIONAL ---
# En una app real, esto sería una conexión a una base de datos extensa
# como USDA FoodData Central o una API de nutrición.
# Los valores son por cada 100g.
MOCK_NUTRITION_DB = {
    'food': {'calories': 0, 'protein': 0, 'carbs': 0}, # Etiqueta genérica
    'salad': {'calories': 152, 'protein': 10, 'carbs': 8},
    'chicken': {'calories': 239, 'protein': 27, 'carbs': 0},
    'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28},
    'pasta': {'calories': 131, 'protein': 5, 'carbs': 25},
    'pizza': {'calories': 266, 'protein': 11, 'carbs': 33},
    'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23},
    'apple': {'calories': 52, 'protein': 0.3, 'carbs': 14},
    'salmon': {'calories': 208, 'protein': 20, 'carbs': 0},
}

def analyze_food_image(image_path):
    """
    Analiza una imagen de comida, identifica los alimentos y devuelve sus valores nutricionales.
    """
    try:
        # Crea un cliente para la API de Vision
        client = vision.ImageAnnotatorClient()

        # Carga la imagen en memoria
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Realiza la detección de etiquetas (label detection)
        response = client.label_detection(image=image)
        labels = response.label_annotations

        if response.error.message:
            raise Exception(f"Error en la API de Vision: {response.error.message}")

        print("--- IA ha detectado las siguientes etiquetas ---")
        detected_foods = []
        for label in labels:
            print(f"- {label.description} (Confianza: {label.score:.2f})")
            # Agregamos la etiqueta si la IA tiene una confianza razonable
            if label.score > 0.75:
                 detected_foods.append(label.description.lower())
        
        print("\n--- Calculando Valores Nutricionales ---")
        total_nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'identified_foods': []}
        
        # Busca cada alimento detectado en nuestra "base de datos"
        for food in detected_foods:
            # Aquí se podría tener una lógica más compleja para buscar sinónimos
            if food in MOCK_NUTRITION_DB:
                nutrition_data = MOCK_NUTRITION_DB[food]
                print(f"Añadiendo valores para: {food}")
                total_nutrition['calories'] += nutrition_data['calories']
                total_nutrition['protein'] += nutrition_data['protein']
                total_nutrition['carbs'] += nutrition_data['carbs']
                total_nutrition['identified_foods'].append(food)

        # Si no se identificó nada específico, se devuelve un resultado vacío.
        if not total_nutrition['identified_foods']:
            print("No se pudo identificar un alimento conocido en la imagen.")
            return None

        return total_nutrition

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None

# --- EJEMPLO DE USO ---
# Simula que el usuario ha subido una imagen llamada "mi_comida.jpg"
# Para probarlo, guarda una imagen de, por ejemplo, pollo con ensalada y llámala "mi_comida.jpg"
image_file_path = 'mi_comida.jpg' 

# Llamamos a la función principal
nutritional_results = analyze_food_image(image_file_path)

if nutritional_results:
    print("\n========= RESULTADO FINAL =========")
    print(f"Alimentos identificados: {', '.join(nutritional_results['identified_foods'])}")
    print(f"Calorías totales estimadas: {nutritional_results['calories']:.0f} kcal")
    print(f"Proteínas totales estimadas: {nutritional_results['protein']:.1f} g")
    print(f"Carbohidratos totales estimados: {nutritional_results['carbs']:.1f} g")
    print("===================================")

