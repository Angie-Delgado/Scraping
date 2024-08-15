import spacy

class EstructurarDatos:
    def __init__(self):
        # Cargar el modelo en español de spaCy
        self.nlp = spacy.load("es_core_news_sm")

    def procesarTexto(self):
        doc = self.nlp(texto)

        caracteristicas = {}
        for sent in doc.sents:
            if "procesador" in sent.text.lower():
                caracteristicas["procesador"] = sent.text
            elif "pantalla" in sent.text.lower():
                caracteristicas["pantalla"] = sent.text
            elif "teclado" in sent.text.lower():
                caracteristicas["teclado"] = sent.text
            elif "almacenamiento" in sent.text.lower() or "puertos" in sent.text.lower():
                caracteristicas["almacenamiento_y_puertos"] = sent.text
            elif "dimensiones" in sent.text.lower() or "peso" in sent.text.lower():
                caracteristicas["dimensiones_y_peso"] = sent.text
        return caracteristicas
    

# Crear una instancia de la clase
mi_instancia = MiClase("valor1", "valor2")

# Llamar a los métodos
mi_instancia.metodo1()
mi_instancia.metodo2("nuevo_valor")


    

    # Texto del producto
    texto = """
    Sobre este artículo
    Procesador y sistema: el procesador Intel Quad-Core Pentium N200, 2.7 GHz-4 núcleos-4 hilos, Windows 11 Home.
    Pantalla: pantalla de 15.6 pulgadas (1366 x 768) con biseles estrechos y diseño antirreflejos que ofrece una experiencia visual vívida y clara. La batería soporta hasta 11 horas y 45 minutos de reproducción de video.
    Teclado: teclado suave de tamaño completo con teclado numérico y teclas de función como obturador de cámara, tecla de silencio de micrófono y tecla de modo avión.
    Almacenamiento y puertos: 16 GB de RAM, 128 GB UFS y 128 GB de almacenamiento externo SSD. Alta velocidad y fiabilidad. Múltiples puertos: USB Type-C, USB Type-A, HDMI, Wi-Fi 6 y Bluetooth 5.
    Dimensiones y peso: Mide 20.47 x 12.01 x 2.72 pulgadas y pesa solo 3.24 libras, su diseño elegante garantiza una portabilidad de moda sobre la marcha.
    """

    # Procesar el texto
    doc = nlp(texto)

    # Definir una función para extraer características del texto
    def extraer_caracteristicas(doc):
        

    # Extraer las características
    caracteristicas_producto = extraer_caracteristicas(doc)

    # Imprimir las características extraídas
    for clave, valor in caracteristicas_producto.items():
        print(f"{clave}: {valor}")





