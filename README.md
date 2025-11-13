# USO DE INTELIGENCIA ARTIFICIAL PARA EL ANALISIS DE PRECIOS DE LIBROS EN PRENSA HISTÓRICA

_Use of Artificial Intelligence for the analysis of book prices in historical press._

[![web final](/img/output.png)](https://rafav.github.io/diariomercantil/1807/ventas.html)

## 1. Introducción

Este artículo detalla cómo la Inteligencia Artificial permite localizar e identificar automáticamente noticias en prensa decimonónica relativas a la venta de libros, periódicos, libretos y material impreso en general. El procedimiento informático desarrollado, aplicable a diversas cabeceras periodísticas, reduce significativamente el tiempo requerido en la búsqueda manual de información. Para comprobar la validez científica del procedimiento se realiza una validación estadística del resultado. Además, se describen los entregables generados automáticamente a partir de los hallazgos realizados.

**La propuesta se enmarca dentro de las necesidades de investigación de ...**

## 2. Caso de estudio: Diario Mercantil de Cádiz

La selección del Diario Mercantil de Cádiz como objeto de análisis fue determinada por los profesores [Jaime Galbarro](https://www.jaimegalbarro.com/)  y [Carlos Collantes](https://www.uco.es/investigacion/proyectos/phebo/es/equipo/carlos-m-collantes-s%C3%A1nchez) de las universidades de Sevilla y Córdoba respectivamente, **en el contexto de investigación de.....** Los ejemplares se encuentran disponibles en formato digital en el [portal de Prensa Histórica](https://prensahistorica.mcu.es/es/publicaciones/numeros_por_mes.do?idPublicacion=3625).

Esta publicación, que abarca desde 1807 hasta 1830, comprende 7.456 ejemplares con un total de 37.381 páginas. Constituye un conjunto documental idóneo por diversos motivos:

**a)** Es un periódico generalista con amplia variedad temática (noticias económicas, culturales y sociales) a la vez que un de marcado enfoque mercantil.

**b)** Cubre un período histórico crucial como la Guerra de la Independencia, donde la vida cotidiana experimentó alteraciones significativas, incluyendo interrupciones en la actividad cultural.

**c)** Ofrece ejemplares digitalizados de buena calidad para el procesamiento automatizado.


## 3. Diseño del prompt inicial

La implementación de IA en este proyecto ha tenido en cuenta dos consideraciones fundamentales:

**a)** La necesidad de prevenir que la IA alucine y genere datos inexistentes en las fuentes originales.

**b)** La importancia de obtener información sistemática y exhaustiva, sin omisión de referencias relevantes.

Las pruebas realizadas con modelos como Qwen y Claude revelaron que disponemos de soluciones bastante fiables para el procesamiento integral de prensa histórica. Herramientas especializadas en reconocimiento óptico de caracteres (OCR) como Transkribus, eScriptorium o Surya ofrecen buenos resultados en la transcripción pero no están diseñadas para la localización automática de ventas y menos aún en la extracción de los distintos campos a estudiar: título, autor, formato, tomos, encuadernación, precio, lugares de venta y la transcripción literal de la información. Por ello se opta por el uso de LLM (modelos grandes de lenguaje) para localizar y extraer la información relevante. 

Con el objetivo de optimizar la utilidad de los datos extraídos, se ha establecido que los resultados proporcionados por la IA deben presentarse normalizados y organizados sistemáticamente, a fin de facilitar búsquedas posteriores, filtrados y la localización ágil de hallazgos relevantes.

Partiendo de estas consideraciones, se seleccionaron 6 ejemplares al azar, y se analizaron de forma manual para comprobar la calidad de las salidas de los modelos y los sucesivos prompts. La salida obtenida tras la revisión manual es la siguiente:

| Fecha | Página | Autor | Traductor | Título | Tomos | Formato | Encuadernación | Precio | Puesto de venta |
|---|---|---|---|---|---|---|---|---|---|
| 1807-03-20 | 3-4 (315-316) | | | Minerva. Revisor General | 4 | | | 15 rs. cada tomo | Despacho principal |
| 1807-03-20 | 3-4 (315-316) | | | Minerva. Quadro de la Europa | 1 | | | 20 rs. cada tomo | Despacho principal |
| 1807-03-20 | 3-4 (315-316) | | | Minerva. Cartas atenienses | 1 | | | 20 rs. cada tomo | Despacho principal |
| 1807-03-20 | 3-4 (315-316) | | | Minerva. Londres y los ingleses | 1 | | | 20 rs. cada tomo | Despacho principal |
| 1807-03-20 | 3-4 (315-316) | Doctor Akerlio Rapsodiano | | Ensayo de una historia de las Pelucas, de tomitos | | | | 5 rs. más 1 cuarto | Despacho principal |
| 1807-03-27 | 4 (344) | Doctor Joseph Ruiz y Romero | | Oración funebre que en las solemnes exequias | | | | | Imprenta de Vega y compañía |
| 1809-01-20 | 4 (80) | F. Pedro de San Josef | | Glorias militares de los españoles | 3 | Octavo | | 10 rs. de vellón | Librería de Dávila |
| 1823-07-26 | 4 () | Say | | Tratado de economía política | 2 | 8° prolongado | rustica | 80 rs. | Librería de Igual |
| 1823-07-26 | 4 () | Prepean | | Estenografía exacta | 1 | 8° | rustica | 50 rs. | Librería de Igual |
| 1823-07-26 | 4 () | Thevenot | | Compendio de taquigrafía | 1 | 12° | | 18 rs. | Librería de Igual |
| 1823-07-26 | 4 () | Vidal | | Notografía | 1 | 4° | rustica | 60 rs. | Librería de Igual |
| 1823-07-26 | 4 () | Delavigne | | Las vísperas sicilianas tragedia | | | | 12 rs. | Librería de Igual |
| 1823-07-26 | 4 () | Ancelot | | Luis IX tragedia | | | | 12 rs. | Librería de Igual |
| 1829-04-24 | 6 (6) | | | El reglamento para el puerto franco de Cádiz | | | | | Imprenta García |
| 1829-04-24 | 6 (6) | Roche y Sanson | | Nuevos elementos de patología | 5 | 4° | | | Librería de Hernando |
| 1829-07-10 | 6 (6) | autor de Cádiz Restaurado | | Canto funebre, en la muerte de la Reyna de España Doña María Josefa | 3 rs. | | | | Imprenta García |



Se parte de un prompt simple y básico, que sirve para conocer cómo interpretan los modelos la pregunta y la calidad de las respuestas.

*Localiza sistemáticamente toda referencia a venta, anuncio, catálogo, reseña o mención de libros, folletos, impresos, obras literarias o publicaciones periódicas, por pequeña que sea. Devuelve exclusivamente un JSON con los campos autor    traductor    título    número_de_tomos    formato    encuadernación    precio    lugares_de_venta    día_periódico    que figura en el pdf, página del pdf del hallazgo y números de página del periódico, transcripción con la transcripción literal de la noticia.  Doble check. La autoría  puede incluir fórmulas como 'autor de...', 'traductor de...', ..'compuesta por..' etc. en cuyo caso omite la fórmula.*



Se comienza con un ejemplar del 1829_07_10
### 3.1 Claude

1)[prompt simple con Sonnet 4.5 sin pensamiento extendido.](https://claude.ai/share/58a9bbaa-187f-47be-943a-ab9a11b823a7)

2)[prompt exhaustivo con Sonnet 4.5 sin pensamiento extendido, que no reconoce nada.]( https://claude.ai/chat/9493fa73-472b-4772-8b5a-5624fd23420e) Este modelo queda descartado para automatizar.

3)[prompt exhaustivo con Sonnet 4.5 con pensamiento extendido.](https://claude.ai/share/d4b953de-93af-46c2-bc4e-fa7c95b76039)

4)[prompt exhaustivo con Sonnet 4.5 con pensamiento extendido, analizando ela transcripción obtenida previamente](https://claude.ai/share/50ba4406-395a-4c4f-8d4b-f5f4c2dfa51e)


La diferencia entre 3 y 4 es que se pierde la referencia visual,  por ejemplo:
```
 "extension_anuncio_lineas": 3,
    "posicion_en_pagina": "centro, dentro de la sección de avisos",
    "elementos_tipograficos_destacados": [],
    "acompañamiento_visual": "",
```

### 3.2 QWen
Se analiza con Qwen-3-vl y aunque parece que los resultados son similares se descarta porque la transcripción es peor: 

[Qwen3-VL-235B-A22B salida simple](https://chat.qwen.ai/s/bd609038-1799-4c71-ad89-923aba6fa79b?fev=0.0.237) 
[Qwen3-VL-235B-A22B salida compleja](https://chat.qwen.ai/s/f6dc53af-e0b6-4843-a0f2-2b2a55c63e3c?fev=0.0.237)


### 3.3 Refinamiento del prompt.

Una vez seleccionados los modelos candidatos (Sonnet 4.5 con y sin pensamiento extendido) se continua con la fase de refinar el prompt, creando hasta [6 versiones distintas](https://github.com/Rafav/Venta-libros/tree/main/prompts).

Los resultados pueden rse en estos enlaces:
 
#### 6 pdf validados manualmente

[Comparativa](validacion-manual/comparativa.ods)


#### 1807


[V01](https://rafav.github.io/diariomercantil/1807/ventas_prompt_v01.html)
[V02](https://rafav.github.io/diariomercantil/1807/ventas_prompt_v02.html)
[V03](https://rafav.github.io/diariomercantil/1807/ventas_v03.html)
[V04](https://rafav.github.io/diariomercantil/1807/ventas_v04.html)
[V05](https://rafav.github.io/diariomercantil/1807/ventas_prompt_v05.html)
[V06 extendida](https://rafav.github.io/diariomercantil/1807/ventas_v06_extendida.html)

Finalmente se opta por usar Sonnet 4.5 con pensamiento extendido y como prompt final:

```
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
json
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
json
{
  "título": "Revisor General",
  "número_de_tomos": "cuatro tomos",
  "precio": "15 rs. cada tomo, más 2 rs. por tomo por portes",
  "lugares_de_venta": "Despacho principal del Diario Mercantil, calle del Molino núm. 65",
  "transcripción": "Los siete tomos publicados son cuatro con el título de Revisor General. Los precios son de 15 rs. cada tomo, á lo que se ha de añadir 2 rs. por tomo, por los portes. Se vende en el Despacho principal del Diario Mercantil, calle del Molino núm. 65."
}


Entrada 2 (Quadro de la Europa):
json
{
  "título": "Quadro de la Europa",
  "número_de_tomos": "un tomo",
  "precio": "20 rs., más 2 rs. por portes",
  "lugares_de_venta": "Despacho principal del Diario Mercantil, calle del Molino núm. 65",
  "transcripción": "uno del Quadro de la Europa; de estos se podrá vender separadamente. Los precios son 20 rs., á lo que se ha de añadir 2 rs. por tomo, por los portes. Se vende en el Despacho principal del Diario Mercantil, calle del Molino núm. 65."
}


[Y así para cada obra individual]

---

### Ejemplo 2: Formato y tomos separados

**Texto**: "cinco tomos en 8º"

**Salida correcta**:
json
{
  "número_de_tomos": "cinco tomos",
  "formato": "8º"
}


**Salida incorrecta** (NO HACER):
json
{
  "número_de_tomos": "cinco tomos en 8º",
  "formato": null
}

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

```

La verificación manual de las respuestas con estos dos ejemplares confirmó su corrección, lo que permitió avanzar a la siguiente etapa del proyecto.

## 4. Automatizaciones

La incorporación de especialistas en informática a proyectos de Humanidades Digitales permite diseñar procesos automatizados, que optimizan tiempos, sistematizan procedimientos y aportan seguridad cuando se abordan proyectos de análisis a gran escala.

### 4.1 Scrapping

El término *scrapping* designa un conjunto de técnicas destinadas a extraer datos de páginas web. En el caso del portal de Prensa Histórica, los resultados de búsqueda muestran enlaces a ejemplares en formato PDF, que facilita su descarga. Esta cabecera que analizamos se había descargado previamente, enmarcado dentro de las necesidades de investigación del proyecto «La institución del "Siglo de Oro". Procesos de construcción en la prensa periódica (1801-1868). SILEM III» (PID2022-136995NB-I00), financiado por el Plan Nacional de Investigación del Ministerio de Ciencia e Innovación y dirigido por Mercedes Comellas (Universidad de Sevilla). La documentación técnica está disponible en [Análisis de la literatura aúrea en el Diario Mercantil de Cádiz](https://github.com/Rafav/AI-HISTORICAL-NEWSPAPERS/tree/main).



## 5. Validación estadística

En esta etapa del proyecto contamos ya con un prompt validado y el corpus completo. Es necesario verificar que la IA proporciona resultados correctos utilizando una muestra estadísticamente significativa. Para ello, solicitamos a la propia IA la selección de un conjunto representativo de ejemplares. Considerando que disponemos de una población finita de aproximadamente 7.500 documentos, con un nivel de confianza deseado del 95%, un margen de error del 5% y asumiendo una variabilidad esperada del 50% (todos los ejemplares tienen idéntica probabilidad de contener o no la información objeto de estudio), obtenemos la siguiente distribución muestral:

### 5.1 Muestra estratificada por años

Se proponen para analizar los pdfs siguientes:

    "1807": [73, 124, 140, 156, 167, 182, 190, 201, 215, 230, 245, 267, 278, 290, 301, 322, 340, 351],
    "1808": [15, 34, 52, 78, 95, 112, 145, 167, 189, 210, 234, 256, 278, 290, 312, 334, 347],
    "1809": [21, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 301, 323, 334, 345, 358],
    "1810": [23, 45, 67, 89, 112, 134, 156, 178, 201, 223, 245, 267, 289, 301, 312, 323],
    "1811": [22, 44, 67, 89, 111, 133, 156, 178, 200, 222, 245, 267, 289, 311, 333, 345, 355],
    "1812": [21, 43, 65, 87, 109, 131, 154, 176, 198, 220, 242, 264, 286, 308, 330, 335],
    "1816": [12, 34, 56, 78, 98, 112],
    "1817": [23, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 311, 323, 334, 345, 356],
    "1818": [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 352, 360],
    "1819": [21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 353, 361],
    "1820": [25, 48, 71, 94, 117, 140, 163, 186, 209, 232, 255, 278, 301, 324, 347, 370, 383, 396, 409, 422, 428],
    "1821": [24, 47, 70, 93, 116, 139, 162, 185, 208, 231, 254, 277, 300, 323, 346, 369, 382, 395, 408, 421, 427],
    "1822": [23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 362],
    "1823": [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 359],
    "1824": [24, 46, 68, 90, 112, 134, 156, 178, 200, 222, 244, 266, 288, 310, 332, 344, 355, 363],
    "1825": [23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 361],
    "1826": [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 360],
    "1827": [21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 352, 359],
    "1828": [23, 45, 67, 89, 111, 133, 155, 177, 199, 221, 243, 265, 287, 309, 331, 343, 354, 362],
    "1829": [22, 44, 66, 88, 110, 132, 154, 176, 198, 220, 242, 264, 286, 308, 330, 342, 353, 361],
    "1830": [21, 43, 65, 87, 109, 131, 153, 175, 197, 219, 241, 263, 285, 307, 329, 341, 358]

## 6. IA para el procesado del dataset

Se decide usar el modelo Sonnet 4.5 con pensamiento extendido y se crean las salidas para los ejemplares, siguiendo estos pasos:

### 6.1 Procesado masivo de todos los pdf

```
for file in *.pdf;  do     if [ -f "$file" ];      then        python3  ../batch-libros-diario-Madrid-sonnet-extendido_v06.py --file_name "$file" --custom_id "$(basename "$file" .pdf)"> $(basename "$file" .pdf)_batch_order.txt; fi; done
```

### 6.2 Recuperación de los resultados

for file in *_batch_order.txt; do     if [ -f "$file" ]; then         id=$(grep -o "msgbatch_[[:alnum:]]\+" "$file");                  output_file=$(basename "$file" "_batch_order.txt")_batch_output.txt;                  if [ ! -z "$id" ]; then             echo "Procesando archivo $file con ID: $id";             echo "Guardando resultado en: $output_file";             python ../../recuperar_batch.py "$id" > "$output_file";         else             echo "No se encontró ID en el archivo $file";         fi;     fi; done

### 6.3 Extracción de los datos JSON de cada pdf

for file in *_batch_output.txt; do     grep -oP '```json\K.*?(?=```)' "$file" |     sed 's/\\n/\n/g; s/\\"/"/g; s/\\\\/\\/g; s/\\'\''/'\''/g' |     python3 -c "import json,sys; json.dump(json.load(sys.stdin), sys.stdout, ensure_ascii=False, indent=2)"     > "${file%_batch_output.txt}.json"; done


### 6.4 Generación de salida de los resultados de cada año

```
./combinar_json_add_ejemplares.sh    
```

## 7. Desarrollo de la interfaz web para cotejar ejemplares y resultados

En esta fase, disponemos del prompt validado, los resultados procesados para cada ejemplar. El siguiente objetivo consiste en proporcionar a los expertos una herramienta efectiva para validar los resultados. Con este fin se ha diseñado una interfaz web que ofrece las siguientes funcionalidades:

- Visualización de resultados por ejemplar.
- Consulta simultánea de los documentos PDF originales.
- Desplazamiento independiente por resultados y documentos.
- Navegación directa las páginas concretas donde aparecen noticias literarias o artísticas.

Al tratarse de datos estructurados en formato JSON, la solución implementada consiste en una única página web reutilizable para cada año. La interfaz muestra el resultado de añalizar cada ejemplar junto con enlaces tanto al pdf completo como a la página concreta de cada hallazgo.


## 8. Acceso a los datos

Se publica la muestra a validar en GitHub Pages, plataforma que permite alojar sitios web:

[1807](https://rafav.github.io/diariomercantil/1807/ventas.html)
[1808](https://rafav.github.io/diariomercantil/1808/ventas.html)
[1809](https://rafav.github.io/diariomercantil/1809/ventas.html)
[1810](https://rafav.github.io/diariomercantil/1810/ventas.html)
[1811](https://rafav.github.io/diariomercantil/1811/ventas.html)
[1812](https://rafav.github.io/diariomercantil/1812/ventas.html)
[1816](https://rafav.github.io/diariomercantil/1816/ventas.html)
[1817](https://rafav.github.io/diariomercantil/1817/ventas.html)
[1818](https://rafav.github.io/diariomercantil/1818/ventas.html)
[1819](https://rafav.github.io/diariomercantil/1819/ventas.html)
[1820](https://rafav.github.io/diariomercantil/1820/ventas.html)
[1821](https://rafav.github.io/diariomercantil/1821/ventas.html)
[1822](https://rafav.github.io/diariomercantil/1822/ventas.html)
[1823](https://rafav.github.io/diariomercantil/1823/ventas.html)
[1824](https://rafav.github.io/diariomercantil/1824/ventas.html)
[1825](https://rafav.github.io/diariomercantil/1825/ventas.html)
[1826](https://rafav.github.io/diariomercantil/1826/ventas.html)
[1827](https://rafav.github.io/diariomercantil/1827/ventas.html)
[1828](https://rafav.github.io/diariomercantil/1828/ventas.html)
[1829](https://rafav.github.io/diariomercantil/1829/ventas.html)
[1830](https://rafav.github.io/diariomercantil/1830/ventas.html)

## 9. Exportación a hoja de cálculo.

Se ha creado un *script* (pequeño programa) que une los hallazgos y genera una [hoja de cálculo](libros_completo.csv) para ayudar al análisis de los hallazgos. 

## 10. Análisis por IA

Con el cojunto de noticias de interés se pide a la IA, *Claude code* en este caso un paper sobre el mercado de libros. Se introduce al programa la siguiente instrucción *analiza libros_completo.csv y crea un paper universitario sobre la venta de libros y material impreso a partir de las noticas del Diario Mercantil de Cádiz *
