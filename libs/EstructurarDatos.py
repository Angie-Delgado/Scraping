import spacy
import re

class EstructurarDatosEs:
    def __init__(self, texto):
        try:
            # Cargar el modelo en español de spaCy
            self.nlp = spacy.load("es_core_news_sm")
            self.texto = texto
            
            # Ejecutar el método procesarTexto al instanciar la clase
            self.caracteristicas = self.procesarTexto()
        except Exception as e:
            raise Exception(f"Error en __init__: {e}")

    def procesarTexto(self):
        try:
            doc = self.nlp(self.texto)

            caracteristicas = {}
            for sent in doc.sents:
                sent_text = sent.text.lower()
                # Lista de palabras clave
                palabras_clave = ["intel", "GHz", "procesador"]
                patron = "|".join(re.escape(palabra) for palabra in palabras_clave)

                # Buscar coincidencias en el texto
                if re.search(patron, sent_text):
                    caracteristicas["procesador"] = self.extraer_caracteristica(sent_text, "procesador")
                elif "pantalla" in sent_text:
                    caracteristicas["pantalla"] = self.extraer_caracteristica(sent_text, "pantalla")
                elif "teclado" in sent_text:
                    caracteristicas["teclado"] = self.extraer_caracteristica(sent_text, "teclado")
                elif "almacenamiento" in sent_text:
                    caracteristicas["almacenamiento"] = self.extraer_dato(doc, "gb")
                elif "peso" in sent_text:
                    caracteristicas["peso"] = self.extraer_caracteristica(sent_text, "pesa")
                elif re.search(patron, sent_text):
                    caracteristicas["velocidad"] = self.extraer_dato(sent_text, "hz")
                else:
                    caracteristicas["velocidad"] = self.extraer_dato(doc, "hz")
            
            return caracteristicas
        except Exception as e:
            raise Exception(f"Error en procesarTexto: {e}")

    def extraer_caracteristica(self, texto, clave):
        try:
            doc = self.nlp(texto)
            palabras_ignorar = {"y", "sistema", ":", "el", "la", "puertos", "de", "solo"}
            palabras_ignorar.add(clave)
            unidades = ["ghz", "mhz", "gb", "mb", "tb", "kb", "w", "v", "mah", "in", "kg", "pulgadas", "libras", "lb", "lbs", "inches"]
            caracteristica = []
            
            for token in doc:
                if token.text.lower() == clave:
                    for i in range(token.i + 1, len(doc)):
                        siguiente_token = doc[i]
                        if siguiente_token.text.lower() != ',':
                            if siguiente_token.text.lower() not in palabras_ignorar:
                                caracteristica.append(siguiente_token.text)
                                if siguiente_token.text.lower() in unidades:
                                    break
                        else:
                            break
                    break
            return ' '.join(caracteristica) if caracteristica else None
        except Exception as e:
            raise Exception(f"Error en extraer_caracteristica: {e}")

    def extraer_dato(self, doc, unidad):
        try:
            caracteristica = []
            for i in range(len(doc)):
                if unidad in doc[i].text.lower():
                    if i > 0:
                        anterior_token = doc[i - 1]
                        valor = re.findall(r'\d+\.?\d*', anterior_token.text[::-1])
                        return anterior_token.text + doc[i].text
                        break
            return None
        except Exception as e:
            raise Exception(f"Error en extraer_dato: {e}")

class EstructurarDatosEn:
    def __init__(self, texto):
        try:
            # Cargar el modelo en inglés de spaCy
            self.nlp = spacy.load("en_core_web_sm")
            self.texto = texto
            
            self.caracteristicas = self.procesarTexto()
        except Exception as e:
            raise Exception(f"Error en __init__: {e}")

    def procesarTexto(self):
        try:
            doc = self.nlp(self.texto)

            caracteristicas = {}
            for sent in doc.sents:
                sent_text = sent.text.lower()
                palabras_clave = ["intel", "hz", "processor", "screen", "keyboard", "storage", "weight", "lb"]
                patron = "|".join(re.escape(palabra) for palabra in palabras_clave)

                if re.search(patron, sent_text):
                    if "processor" in sent_text:
                        caracteristicas["processor"] = self.extraer_caracteristica(sent_text, "processor")
                    if "display" in sent_text:
                        caracteristicas["display"] = self.extraer_dato(sent_text, '/')
                    if "keyboard" in sent_text:
                        caracteristicas["keyboard"] = self.extraer_caracteristica(sent_text, "keyboard")
                    if "storage" in sent_text:
                        caracteristicas["storage"] = self.extraer_dato(sent_text, "gb")
                    if "lb" in sent_text:
                        caracteristicas["weight"] = self.extraer_dato(sent_text, "lb")
                    if "pounds" in sent_text:
                        caracteristicas["weight"] = self.extraer_dato(sent_text, "pounds")
                    if "hz" in sent_text:
                        caracteristicas["speed"] = self.extraer_dato(sent_text, "hz")  
            
            return caracteristicas
        except Exception as e:
            raise Exception(f"Error en procesarTexto: {e}")

    def extraer_caracteristica(self, texto, clave):
        try:
            doc = self.nlp(texto)
            palabras_ignorar = {"and", "system", ":", "the", "of", "ports", "only"}
            palabras_ignorar.add(clave)
            unidades = ["ghz", "mhz", "gb", "mb", "tb", "kb", "w", "v", "mah", "in", "kg", "inches", "pounds","lb", "lbs", "inches"]
            caracteristica = []
            
            for token in doc:
                if token.text.lower() == clave:
                    for i in range(token.i + 1, len(doc)):
                        siguiente_token = doc[i]
                        if siguiente_token.text.lower() != ',':
                            if siguiente_token.text.lower() not in palabras_ignorar:
                                caracteristica.append(siguiente_token.text)
                                if siguiente_token.text.lower() in unidades:
                                    break
                        else:
                            break
                    break
            return ' '.join(caracteristica) if caracteristica else None
        except Exception as e:
            raise Exception(f"Error en extraer_caracteristica: {e}")

    def extraer_dato(self, texto, unidad):
        try:
            doc = self.nlp(texto)
            caracteristica = []
            for i in range(len(doc)):
                if unidad in doc[i].text.lower():
                    if i > 0:
                        anterior_token = doc[i - 1]
                        valor = re.findall(r'\d+\.?\d*', anterior_token.text)
                        return anterior_token.text + doc[i].text
                        break
            return None
        
        except Exception as e:
            raise Exception(f"Error en extraer_dato: {e}")

descripcion = """
descripcion = Sobre este artículo    Procesador y sistema: el procesador Intel Quad-Core Pentium N200, 2.7 GHz-4 núcleos-4 hilos, Windows 11 Home.    Pantalla: pantalla de 15.6 pulgadas (1366 x 768) con biseles estrechos y diseño antirreflejos que ofrece una experiencia visual vívida y clara. La batería soporta hasta 11 horas y 45 minutos de reproducción de video.    Teclado: teclado suave de tamaño completo con teclado numérico y teclas de función como obturador de cámara, tecla de silencio de micrófono y tecla de modo avión.    Almacenamiento y puertos: 16 GB de RAM, 128 GB UFS y 128 GB de almacenamiento externo SSD. Alta velocidad y fiabilidad. Múltiples puertos: USB Type-C, USB Type-A, HDMI, Wi-Fi 6 y Bluetooth 5.    【Dimensiones y peso】Mide 20.47 x 12.01 x 2.72 pulgadas y pesa solo 3.24 libras, su diseño elegante garantiza una portabilidad de moda sobre la marcha.    \n›  Ver los detalles del producto
"""

datos = {}
from_description = EstructurarDatosEs(descripcion)

for clave, valor in from_description.caracteristicas.items():
    datos[clave] = valor  
print(datos)

texto= "About this item    MULTITASKING MASTER - The IdeaPad 1 is a thin and compact laptop that offers responsive performance and anticipates your every need for effortless on-the-go multitasking    MORE EXPANSIVE DISPLAY - Indulge in a better binging experience by immersing yourself in your favorite shows with a borderless display for more screen while listening to clear, rich audio from two Dolby Audio speakers    PERFORMANCE ON THE GO - Zip along while multitasking across several tabs, the new AMD Ryzen 5 5500U processor built on UMA architecture delivers punchy mobile performance with a 20W thermal design point    LIGHTEST PART OF YOUR DAY - Weighing just 3.5 lbs, the effortlessly cool cloud grey laptop is lighter than your water bottle and just as essential    SOLID SECURITY - Keep your home life private and be seen only when you want to be with the 720p camera that comes with a physical privacy shutter    PRODUCTIVITY WITH NO LIMITS - No Wi-Fi? No worries, with 512GB storage, 12 hours of battery life, and rapid charge you can access and edit your files offline, anywhere and still have space for all your family's needs    A SMARTER WAY TO LEARN - Flip to Start turns on your IdeaPad 1 immediately upon opening the lid, so you can hop on that urgent video call and let your ideas be heard thanks to Smart Noise Cancelling minimizing background noise    \n   EQUIPPED FOR WORK AND PLAY - Ready to connect to your world with 2 USB ports, USB-C port, HDMI port, SD card reader, and a combination headphone/mic jack SIZE UNPACKED (D x H x W) - 360 x 236 x 17.9 mm or 14.17 x 9.29 x 0.70 inches INCLUDED ITEMS - Computer, Charger, User Guide   Show more"
datos2 = {}
from_description_en = EstructurarDatosEn(texto)

for clave, valor in from_description_en.caracteristicas.items():
    datos2[clave] = valor
print(datos2)
