import os
import zipfile

def procesar_zips(ruta_directorio):
    # Cambiar al directorio de trabajo
    try:
        os.chdir(ruta_directorio)
    except FileNotFoundError:
        print(f"No se encontró la ruta: {ruta_directorio}")
        return

    # Listar archivos zip
    archivos = [f for f in os.listdir() if f.endswith('.zip')]

    if not archivos:
        print("No se encontraron archivos .zip para procesar.")
        return

    for archivo in archivos:
        nombre_carpeta = archivo[:-4]  # Quita el .zip
        
        try:
            print(f"Descomprimiendo: {archivo}...")
            with zipfile.ZipFile(archivo, 'r') as zip_ref:
                # Crea una carpeta con el nombre del zip para evitar desorden
                os.makedirs(nombre_carpeta, exist_ok=True)
                zip_ref.extractall(nombre_carpeta)
            
            # Una vez extraído, borramos el zip
            os.remove(archivo)
            print(f"Completado y borrado: {archivo}")
            
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")

if __name__ == "__main__":
    ruta = r"C:\Users\Usuario\Desktop\La_Orga\MarkDown"
    procesar_zips(ruta)