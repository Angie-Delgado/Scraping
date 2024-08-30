import json
import os
import csv

class Utils():
    
    @staticmethod
    def pull_full_json_file(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)       
        return data

    @staticmethod   
    def pull_json_file(file_path, indices):
        try:
            contenido = []
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for i, objeto in enumerate(data):
                    if i in indices:
                        contenido.append(objeto)
            return contenido
        except FileNotFoundError as e:
            raise FileNotFoundError(f"El archivo {file_path} no fue encontrado: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Error al decodificar el archivo JSON: {e}")


    @staticmethod
    def batch_push_json_file(data, file_name):        
        try:
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as currfile:
                    try:
                        existing_data = json.load(currfile)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            # Asegurarse de que existing_data es una lista
            if not isinstance(existing_data, list):
                raise ValueError("El archivo JSON no contiene una lista. El formato del archivo no es compatible.")

            # Agregar los nuevos datos a la lista existente
            existing_data.append(data)

            # Escribir el contenido actualizado en el archivo
            with open(file_name, 'w', encoding='utf-8') as currfile:
                json.dump(existing_data, currfile, ensure_ascii=False, indent=4)
                
        except Exception as e:
            raise Exception(f"Ocurrio un error escribiendo en el archivo: {e}")

    @staticmethod
    def push_json_file(data, file_name):        
        try:        
            # Escribir el contenido por elemento
            with open(file_name, 'w', encoding='utf-8') as currfile:
                json.dump(data, currfile, ensure_ascii=False, indent=4)
                currfile.write('\n')
                
        except Exception as e:
            raise Exception(f"Ocurrio un error escribiendo en el archivo: {e}")
    

    @staticmethod
    def get_list_from_txt(file_name):        
        try:
            with open(file_name, 'r', encoding='utf-8') as currfile:
                llist = [line.strip() for line in currfile if line.strip()]
            return llist
        except Exception as e:
            raise Exception(f'Ocurrio un error leyendo el archivo txt: {e}')
    
    @staticmethod
    def write_file(data,name):
        try:
            for item in data:
                Utils.push_json_file(item,name)
        except Exception as e:
            raise Exception(f'Error escribiendo en el archivo : {e}')
    
    @staticmethod
    def save_to_csv(data, file_name):

        file_exists = os.path.exists(file_name) and os.path.getsize(file_name) > 0
        # Obtener los nombres de las columnas (keys del diccionario)
        fieldnames = data[0].keys()

        # Abrir el archivo en modo apendice
        with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
            # Crear el objeto DictWriter
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Escribir la cabecera
            if not file_exists:
                writer.writeheader()

            # Escribir las filas
            writer.writerows(data)
