import anthropic
import base64
import argparse
from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.beta.messages.batch_create_params import Request
from anthropic import Anthropic

def main():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Process PDF files with Claude API')
    parser.add_argument('--file_name', required=True, help='Path to the PDF file')
    parser.add_argument('--custom_id', required=True, help='Custom ID for the request')
    args = parser.parse_args()

    # Read and encode the PDF file
    with open(args.file_name, "rb") as pdf_file:
        binary_data = pdf_file.read()
        base64_encoded_data = base64.standard_b64encode(binary_data)
        base64_string = base64_encoded_data.decode("utf-8")

    prompt = """
    # TAREA: Extracción exhaustiva de anuncios de venta de material impreso
Identifica TODAS las referencias a **venta** de material impreso en el documento:
- Anuncios de venta de libros
- Catálogos de librería en venta
- Revistas y publicaciones periódicas en venta
- Folletos e impresos en venta
- Cualquier material bibliográfico ofrecido para la venta
**Requisito crítico**: Extrae únicamente anuncios de venta de material impreso, NO reseñas, menciones o noticias sin intención comercial. No omitas ningún anuncio de venta, por breve que sea.
## FORMATO DE SALIDA
Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta:
```json
{
  "día_periódico": "dd/mm/AAAA",
  "hallazgos": [
    {
      "autor": "string o null",
      "traductor": "string o null",
      "título": "string",
      "número_de_tomos": "string o null",
      "formato": "string o null",
      "encuadernación": "string o null",
      "precio": "string o null",
      "lugares_de_venta": "string o null",
      "página_pdf": "número",
      "página_periódico": "número",
      "transcripción": "string"
    }
  ]
}
```
INSTRUCCIONES ESPECÍFICAS

Autor/Traductor: Extrae solo el nombre, omitiendo fórmulas como "autor de...", "traductor de...", "compuesta por...", etc.
Transcripción:

Incluye el texto literal y completo de CADA anuncio de venta individual
CRÍTICO: Identifica correctamente dónde termina un anuncio y comienza otro
Cada anuncio debe ser una unidad semántica completa (con inicio y fin claros)
Si varios productos se anuncian en el mismo párrafo, sepáralos en entradas diferentes
Busca marcadores de separación: precios finales, cambios de tema, nuevos títulos, frases como "También hay...", "Asimismo se vende..."


Separación de anuncios múltiples:

Si un párrafo contiene múltiples obras en venta, créa una entrada separada para cada una
Cada entrada debe contener solo la información relevante a ese producto específico
No mezcles información de diferentes productos en una sola transcripción


Verificación doble: Revisa el documento dos veces para asegurar que:

No se omite ningún anuncio de venta de libros
Cada anuncio está completo y correctamente delimitado
No hay texto de un anuncio mezclado con otro


Campos nulos: Si un campo no tiene información, usa null en lugar de omitir el campo.
No añadas texto adicional: Solo el JSON, sin explicaciones, comentarios o texto previo/posterior.
    """

    client = anthropic.Anthropic()

    message_batch = client.beta.messages.batches.create(
    betas=["pdfs-2024-09-25", "message-batches-2024-09-24"],
    requests=[
        {
            "custom_id": args.custom_id,
            "params": {
                "model": "claude-sonnet-4-5-20250929", 
                "max_tokens": 64000, 
                 "thinking" : {
                    "type": "disabled"
    },
                
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "base64",
                                    "media_type": "application/pdf",
                                    "data": base64_string
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
        }
    ]
)



    print(message_batch)

if __name__ == "__main__":
    main()
