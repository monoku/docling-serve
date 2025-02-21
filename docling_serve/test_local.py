import json
from runpod_handler import handler

# Create a test input dictionary
test_input = {
    "urls": [
        "https://selloeditorial.unad.edu.co/images/Documentos/OJS/WP_ECAPMA/Gu%C3%ADa_para_autores_WP_ECAPMA.pdf"
    ]
}

# Save test input to JSON file
with open('test_input.json', 'w') as f:
    json.dump(test_input, f)

# Ejecutar la prueba local
if __name__ == "__main__":
    try:
        # Load test input from JSON file
        with open('test_input.json', 'r') as f:
            event = json.load(f)
        
        print("\nPrueba con URL:")
        response_url = handler(event)
        print(json.dumps(response_url, indent=4))
        
    except Exception as e:
        print(f"Error during execution: {str(e)}")