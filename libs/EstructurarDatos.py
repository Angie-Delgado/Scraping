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

