import spacy

class EstructurarDatos:
    def __init__(self):
        # Cargar el modelo en espa�ol de spaCy
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

# Llamar a los m�todos
mi_instancia.metodo1()
mi_instancia.metodo2("nuevo_valor")


    

    # Texto del producto
    texto = """
    Sobre este art�culo
    Procesador y sistema: el procesador Intel Quad-Core Pentium N200, 2.7 GHz-4 n�cleos-4 hilos, Windows 11 Home.
    Pantalla: pantalla de 15.6 pulgadas (1366 x 768) con biseles estrechos y dise�o antirreflejos que ofrece una experiencia visual v�vida y clara. La bater�a soporta hasta 11 horas y 45 minutos de reproducci�n de video.
    Teclado: teclado suave de tama�o completo con teclado num�rico y teclas de funci�n como obturador de c�mara, tecla de silencio de micr�fono y tecla de modo avi�n.
    Almacenamiento y puertos: 16 GB de RAM, 128 GB UFS y 128 GB de almacenamiento externo SSD. Alta velocidad y fiabilidad. M�ltiples puertos: USB Type-C, USB Type-A, HDMI, Wi-Fi 6 y Bluetooth 5.
    Dimensiones y peso: Mide 20.47 x 12.01 x 2.72 pulgadas y pesa solo 3.24 libras, su dise�o elegante garantiza una portabilidad de moda sobre la marcha.
    """

    # Procesar el texto
    doc = nlp(texto)

    # Definir una funci�n para extraer caracter�sticas del texto
    def extraer_caracteristicas(doc):
        

    # Extraer las caracter�sticas
    caracteristicas_producto = extraer_caracteristicas(doc)

    # Imprimir las caracter�sticas extra�das
    for clave, valor in caracteristicas_producto.items():
        print(f"{clave}: {valor}")





