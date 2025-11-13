# USO DE INTELIGENCIA ARTIFICIAL PARA EL ANALISIS DE PRECIOS DE LIBROS EN PRENSA HISTÓRICA

_Use of Artificial Intelligence for the analysis of book prices in historical press._

[![web final](/img/output.png)](https://rafav.github.io/diariomercantil/1807/ventas.html)

## 1. Introducción

Este artículo detalla cómo la Inteligencia Artificial permite localizar e identificar automáticamente noticias en prensa decimonónica relativas a la venta de libros, periódicos, libretos y material impreso en general. El procedimiento informático desarrollado, aplicable a diversas cabeceras periodísticas, reduce significativamente el tiempo requerido en la búsqueda manual de información. Para comprobar la validez científica del procedimiento se realiza una validación estadística del resultado. Además, se describen los entregables generados automáticamente a partir de los hallazgos realizados.

**La propuesta se enmarca dentro de las necesidades de investigación de ...**

## 2. Caso de estudio: Diario Mercantil de Cádiz

La selección del Diario Mercantil de Cádiz como objeto de análisis fue determinada por los profesores [Jaime Galbarro](https://www.jaimegalbarro.com/)  y [Carlos Collantes](https://www.uco.es/investigacion/proyectos/phebo/es/equipo/carlos-m-collantes-s%C3%A1nchez) de las universidades de Sevilla y Córdoba respectivamente, **en el contexto de investigación de.....** Los ejemplares se encuentran disponibles en formato digital en el [portal de Prensa Histórica](https://prensahistorica.mcu.es/es/publicaciones/numeros_por_mes.do?idPublicacion=3625).

Esta publicación, que abarca desde 1807 hasta 1830, comprende 7.456 ejemplares con un total de 37.381 páginas. Constituye un conjunto documental idóneo por diversos motivos:

**a)** Es un periódico generalista con amplia variedad temática (noticias económicas, culturales y sociales).

**b)** Cubre un período histórico crucial como la Guerra de la Independencia, donde la vida cotidiana experimentó alteraciones significativas, incluyendo interrupciones en la actividad cultural.

**c)** Presenta etapas de suspensión temporal de actividades teatrales y otras diversiones públicas por motivos diversos, como los períodos de Cuaresma.

**d)** Ofrece ejemplares digitalizados de buena calidad para el procesamiento automatizado.


## 3. Diseño del prompt inicial

La implementación de IA en este proyecto ha tenido en cuenta dos consideraciones fundamentales:

**a)** La necesidad de prevenir que la IA alucine y genere datos inexistentes en las fuentes originales.

**b)** La importancia de obtener información sistemática y exhaustiva, sin omisión de referencias relevantes.

Las pruebas realizadas con modelos como Qwen y Claude revelaron que disponemos de soluciones bastante fiables para el procesamiento integral de prensa histórica. Herramientas especializadas en reconocimiento óptico de caracteres (OCR) como Transkribus, eScriptorium o Surya ofrecen buenos resultados en la transcripción pero no están diseñadas para la localización automática de ventas y menos aún en la extracción de los distintos campos a estudiar: título, autor, formato, tomos, encuadernación, precio, lugares de venta y la transcripción literal de la información. Por ello se opta por el uso de LLM (modelos grandes de lenguaje) para localizar y extraer la información relevante. 

Con el objetivo de optimizar la utilidad de los datos extraídos, se ha establecido que los resultados proporcionados por la IA deben presentarse normalizados y organizados sistemáticamente, a fin de facilitar búsquedas posteriores, filtrados y la localización ágil de hallazgos relevantes.

Partiendo de estas consideraciones, se seleccionaron 6 ejemplares al azar, y se analizaron de foram manual para comprobar la calidad de las salidas de los modelos y los sucesivos prompts. 

Se parte de un prompt simple y básico, que sirve para conocer cómo interpretan los modelos la pregunta y la calidad de las respuestas.

*Localiza sistemáticamente toda referencia a venta, anuncio, catálogo, reseña o mención de libros, folletos, impresos, obras literarias o publicaciones periódicas, por pequeña que sea. Devuelve exclusivamente un JSON con los campos autor    traductor    título    número_de_tomos    formato    encuadernación    precio    lugares_de_venta    día_periódico    que figura en el pdf, página del pdf del hallazgo y números de página del periódico, transcripción con la transcripción literal de la noticia.  Doble check. La autoría  puede incluir fórmulas como 'autor de...', 'traductor de...', ..'compuesta por..' etc. en cuyo caso omite la fórmula.*

Se genera una primera selección de modelos candiatos y descartados.



Una vez seleccionados los modelos candidatos se continua con la fase de refinar el prompt, creando hasta 6 versiones.



El prompt final es el siguiente:

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

El término *scrapping* designa un conjunto de técnicas destinadas a extraer datos de páginas web. En el caso del portal de Prensa Histórica, los resultados de búsqueda muestran enlaces a ejemplares en formato PDF, que facilita su descarga. Esta cabecera que analizamos se había descargado previamente, enmarcado dentro de las necesidades de investigación del proyecto «La institución del "Siglo de Oro". Procesos de construcción en la prensa periódica (1801-1868). SILEM III» (PID2022-136995NB-I00), financiado por el Plan Nacional de Investigación del Ministerio de Ciencia e Innovación y dirigido por Mercedes Comellas (Universidad de Sevilla). La documentacion técnica está disponile en [Análisis de la literatura aúrea en el Diario Mercantil de Cádiz](https://github.com/Rafav/AI-HISTORICAL-NEWSPAPERS/tree/main).



## 5. Validación estadística

En esta etapa del proyecto contamos ya con un prompt validado y el corpus completo. Es necesario verificar que la IA proporciona resultados correctos utilizando una muestra estadísticamente significativa. Para ello, solicitamos a la propia IA la selección de un conjunto representativo de ejemplares. Considerando que disponemos de una población finita de aproximadamente 7.500 documentos, con un nivel de confianza deseado del 95%, un margen de error del 5% y asumiendo una variabilidad esperada del 50% (todos los ejemplares tienen idéntica probabilidad de contener o no la información objeto de estudio), obtenemos la siguiente distribución muestral:

### 5.1 Muestra estratificada por años

#### Sin fecha
- 1 (único ejemplar)

#### 1807 (18 ejemplares)
73, 124, 140, 156, 167, 182, 190, 201, 215, 230, 245, 267, 278, 290, 301, 322, 340, 351

#### 1808 (17 ejemplares)
15, 34, 52, 78, 95, 112, 145, 167, 189, 210, 234, 256, 278, 290, 312, 334, 347

#### 1809 (18 ejemplares)
21, 45, 67, 89, 112, 134, 156, 178, 200, 223, 245, 267, 289, 301, 323, 334, 345, 358

#### 1810 (16 ejemplares)
23, 45, 67, 89, 112, 134, 156, 178, 201, 223, 245, 267, 289, 301, 312, 323

#### 1811 (17 ejemplares)
22, 44, 67, 89, 111, 133, 156, 178, 200, 222, 245, 267, 289, 311, 333, 345, 355

#### 1812 (16 ejemplares)
21, 43, 65, 87, 109, 131, 154, 176, 198, 220, 242, 264, 286, 308, 330, 335

#### 1816 (6 ejemplares)
12, 34, 56, 78, 98, 112

_[Continúa la lista para todos los años hasta 1830]_

## 6. IA para el procesado del dataset



Se decide usar el modelo Sonnet 4.5 con pensamiento extedido y se crean las salidas para los ejemplares:

### Se procesan masivamente todos los pdf


```
for file in *.pdf;  do     if [ -f "$file" ];      then        python3  ../batch-libros-diario-Madrid-sonnet-extendido_v06.py --file_name "$file" --custom_id "$(basename "$file" .pdf)"> $(basename "$file" .pdf)_batch_order.txt; fi; done
```

### 6.2 Se recuperan los resultados

for file in *_batch_order.txt; do     if [ -f "$file" ]; then         id=$(grep -o "msgbatch_[[:alnum:]]\+" "$file");                  output_file=$(basename "$file" "_batch_order.txt")_batch_output.txt;                  if [ ! -z "$id" ]; then             echo "Procesando archivo $file con ID: $id";             echo "Guardando resultado en: $output_file";             python ../../recuperar_batch.py "$id" > "$output_file";         else             echo "No se encontró ID en el archivo $file";         fi;     fi; done

### 6.3 se extraen los datos JSON de cada pdf

for file in *_batch_output.txt; do     grep -oP '```json\K.*?(?=```)' "$file" |     sed 's/\\n/\n/g; s/\\"/"/g; s/\\\\/\\/g; s/\\'\''/'\''/g' |     python3 -c "import json,sys; json.dump(json.load(sys.stdin), sys.stdout, ensure_ascii=False, indent=2)"     > "${file%_batch_output.txt}.json"; done


### 6.4 Se unen las salidas de cada año

```
./combinar_json_add_ejemplares.sh    
```

## 7. Desarrollo de la interfaz web para cotejar ejemplares y resultados

En esta fase, disponemos del prompt validado, los resultados procesados para cada ejemplar. El siguiente objetivo consiste en proporcionar a los expertos una herramienta efectiva para validar los resultados. Con este fin se ha diseñado una interfaz web que ofrece las siguientes funcionalidades:

- Visualización de resultados por ejemplar
- Consulta simultánea de los documentos PDF originales
- Desplazamiento independiente por resultados y documentos
- Navegación directa a páginas específicas donde aparecen noticias literarias o artísticas

Al tratarse de datos estructurados en formato JSON, la solución implementada consiste en una única página web reutilizable para cada año. La interfaz lee el archivo *combined.json* (que contiene todos los resultados agregados) y presenta la información mediante código JavaScript que itera dinámicamente sobre los datos, independientemente del año, número de ejemplares o cantidad de referencias encontradas.


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

