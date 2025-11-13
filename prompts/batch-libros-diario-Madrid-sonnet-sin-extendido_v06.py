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

---

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

---

## INSTRUCCIONES CRÍTICAS PARA ANUNCIOS MÚLTIPLES EN EL MISMO PÁRRAFO

### 1. IDENTIFICACIÓN DE ANUNCIOS SEPARADOS

Cuando un párrafo contiene MÚLTIPLES obras en venta:
- **Crea una entrada JSON separada para cada obra**
- Busca estos marcadores de separación:
  - Nuevos títulos de obras
  - Frases introductorias: "También hay...", "Asimismo se vende...", "Igualmente...", "Del mismo modo..."
  - Cambios de autor
  - Precios diferentes o repetición de información de precio
  - Conjunciones enumerativas: "uno de..., otro de...", "primero..., segundo..."

### 2. DISTRIBUCIÓN DE INFORMACIÓN COMPARTIDA

Cuando varios libros comparten información común (lugar de venta, condiciones):
- **Repite la información compartida en cada entrada individual**
- Ejemplo: Si 4 libros se venden en el mismo lugar, incluye el lugar en las 4 entradas

### 3. TRANSCRIPCIÓN PRECISA

**REGLA DE ORO**: La transcripción debe contener SOLO el texto que se refiere específicamente a ESA obra.

- ❌ MAL: Copiar todo el párrafo en cada entrada
- ✅ BIEN: Extraer únicamente la porción de texto relevante a cada obra

**Estrategia de delimitación**:
1. Identifica el inicio: título de la obra o frase introductoria
2. Identifica el final: 
   - Antes del siguiente título
   - Antes de "También...", "Asimismo...", etc.
   - En el punto donde se completa la información de precio/venta
3. Para información compartida al final (lugar de venta común), inclúyela en TODAS las transcripciones relevantes

---

## EXTRACCIÓN DE CAMPOS ESPECÍFICOS

### AUTOR y TRADUCTOR
- Extrae SOLO el nombre propio, sin fórmulas de cortesía
- ❌ Elimina: "por el", "compuesta por", "autor de", "del Doctor", "el M.R.P.", "Fr.", "D.", "Doña"
- ✅ Conserva: el nombre completo después de limpiar fórmulas
- **ATENCIÓN**: En oraciones fúnebres o sermones, el autor es quien "dixo" u "pronunció" el sermón, no el personaje homenajeado
- Ejemplo: "dixo el Doctor D. Joseph Ruiz" → autor: "Joseph Ruiz y Roman"

### NÚMERO_DE_TOMOS
- Extrae SOLO la cantidad y la palabra "tomos"/"tomo"
- ❌ NO incluyas el formato en este campo
- ✅ Correcto: "cuatro tomos", "un tomo", "tres tomos"
- ❌ Incorrecto: "tres tomos en 8º", "dos tomos en octavo"

### FORMATO
- Campo SEPARADO del número de tomos
- Formatos comunes: "4º", "8º", "12º", "octavo", "cuarto", "folio"
- ✅ Correcto: "8º", "octavo", "4º prolongado"
- ❌ Incorrecto: mezclar con tomos

### ENCUADERNACIÓN
- Términos: "rústica", "en pasta", "en pergamino", "holandesa", etc.
- Campo independiente

### PRECIO
- Extrae la cifra completa tal como aparece
- Incluye la moneda: "rs.", "reales", "rs. vn.", "maravedís"
- Incluye detalles: "cada tomo", "el juego completo"
- Si hay costes adicionales (portes), inclúyelos: "15 rs. cada tomo, más 2 rs. por portes"

### LUGARES_DE_VENTA
- Extrae la dirección COMPLETA tal como aparece
- Incluye:
  - Nombre del establecimiento o librero
  - Calle y número
  - Piso o detalles adicionales
  - Frases como "y en los despachos de papeles públicos"
- ✅ Correcto: "Despacho principal del Diario Mercantil, calle del Molino núm. 65 quarto entrsuelo"
- ✅ Correcto: "imprenta Gaditana, plazuela del Palillero, y en los despachos de papeles públicos"
- ❌ Incorrecto: Incluir información que NO es lugar de venta (fechas de publicación, descripción del libro)

---

## VERIFICACIÓN EN DOS PASADAS

### PRIMERA PASADA: Identificación
1. Lee el documento completo
2. Marca TODOS los anuncios de venta
3. Cuenta cuántos anuncios hay en cada párrafo

### SEGUNDA PASADA: Extracción
1. Para cada anuncio identificado:
   - Delimita exactamente su transcripción
   - Extrae cada campo por separado
   - Verifica que no mezclas información de otros anuncios
2. Para campos compartidos:
   - Identifica qué información se comparte entre múltiples obras
   - Repítela en cada entrada correspondiente

---

## EJEMPLOS DE CASOS COMPLEJOS

### Ejemplo 1: Múltiples obras con precio y lugar compartidos

**Texto original**: "Los siete tomos publicados son cuatro con el título de Revisor General, uno del Quadro de la Europa, uno de las Cartas Atenienses, uno de Londres y los Ingleses; de estos tres últimos, se podrá vender separadamente lo que quisieren. Los precios son de 15 rs. cada tomo por el Revisor General y 20 por cada uno de los otros tres, á lo que se ha de añadir 2 rs. por tomo, por los portes. Se vende en el Despacho principal del Diario Mercantil, calle del Molino núm. 65."

**Salida correcta**: 4 entradas separadas

Entrada 1 (Revisor General):
```json
{
  "título": "Revisor General",
  "número_de_tomos": "cuatro tomos",
  "precio": "15 rs. cada tomo, más 2 rs. por tomo por portes",
  "lugares_de_venta": "Despacho principal del Diario Mercantil, calle del Molino núm. 65",
  "transcripción": "Los siete tomos publicados son cuatro con el título de Revisor General. Los precios son de 15 rs. cada tomo, á lo que se ha de añadir 2 rs. por tomo, por los portes. Se vende en el Despacho principal del Diario Mercantil, calle del Molino núm. 65."
}
```

Entrada 2 (Quadro de la Europa):
```json
{
  "título": "Quadro de la Europa",
  "número_de_tomos": "un tomo",
  "precio": "20 rs., más 2 rs. por portes",
  "lugares_de_venta": "Despacho principal del Diario Mercantil, calle del Molino núm. 65",
  "transcripción": "uno del Quadro de la Europa; de estos se podrá vender separadamente. Los precios son 20 rs., á lo que se ha de añadir 2 rs. por tomo, por los portes. Se vende en el Despacho principal del Diario Mercantil, calle del Molino núm. 65."
}
```

[Y así para cada obra individual]

---

### Ejemplo 2: Formato y tomos separados

**Texto**: "cinco tomos en 8º"

**Salida correcta**:
```json
{
  "número_de_tomos": "cinco tomos",
  "formato": "8º"
}
```

**Salida incorrecta** (NO HACER):
```json
{
  "número_de_tomos": "cinco tomos en 8º",
  "formato": null
}
```

---

## CASOS ESPECIALES

### Oraciones fúnebres y sermones
- El autor es quien pronunció/dijo el sermón, NO el personaje homenajeado
- Busca: "dixo", "pronunció", "por el Doctor", "por el Padre"

### Obras teatrales
- Distingue entre:
  - Anuncio de venta del texto impreso → SÍ extraer
  - Cartelera de representación teatral → NO extraer (a menos que mencione venta del texto)

### Transcripciones con nombres mal OCR'd
- Transcribe exactamente como aparece en el documento
- No corrijas errores de OCR en la transcripción
- Los errores se corregirán en pasos posteriores

---

## CAMPOS NULOS

Si un campo no tiene información, usa `null` en lugar de omitir el campo o usar string vacío.

---

## SALIDA FINAL

- Solo el JSON, sin texto adicional
- Sin comentarios, explicaciones o markdown
- JSON válido y bien formateado
- Verifica que cada entrada tenga TODOS los campos (incluso si son null)
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
