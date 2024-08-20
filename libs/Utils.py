import json
import os

class Utils():
    
    @staticmethod
    def load_json_data(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)       
        return data

    def export_to_json(data, file_name):
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
          