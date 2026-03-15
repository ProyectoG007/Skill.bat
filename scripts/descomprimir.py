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
    archivos = [f for f in os.listdir() if f.endswith(".zip")]

    if not archivos:
        print("No se encontraron archivos .zip para procesar.")
        return

    for archivo in archivos:
        nombre_carpeta = archivo[:-4]  # Quita el .zip

        # Si ya existe la carpeta, eliminarla para evitar duplicados
        if os.path.exists(nombre_carpeta):
            import shutil

            shutil.rmtree(nombre_carpeta)
            print(f"  Carpeta existente eliminada: {nombre_carpeta}")

        try:
            print(f"Descomprimiendo: {archivo}...")
            with zipfile.ZipFile(archivo, "r") as zip_ref:
                # Crea una carpeta con el nombre del zip para evitar desorden
                os.makedirs(nombre_carpeta, exist_ok=True)
                zip_ref.extractall(nombre_carpeta)

            # Una vez extraído, borramos el zip
            os.remove(archivo)
            print(f"Completado y borrado: {archivo}")

        except Exception as e:
            print(f"Error procesando {archivo}: {e}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raiz = os.path.dirname(script_dir)
    os.chdir(raiz)
    ruta = os.path.join(script_dir, "000.A_Definir")
    procesar_zips(ruta)
