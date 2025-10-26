import os

def leer_phd1(nombre_archivo):
    """
    Lee un archivo .phd.1 de secuenciación Sanger
    y calcula las estadísticas de calidad (Phred).
    """
    phred_scores = []
    dentro_dna = False

    with open(nombre_archivo, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            linea = linea.strip()

            # Normaliza mayúsculas/minúsculas y elimina espacios extra
            if linea.upper().startswith("BEGIN_DNA"):
                dentro_dna = True
                continue
            if linea.upper().startswith("END_DNA"):
                break

            # Procesa solo líneas dentro del bloque de ADN
            if dentro_dna and linea:
                partes = linea.split()
                # Ejemplo típico: A 40 1100  (base, phred, posición)
                if len(partes) >= 2:
                    try:
                        phred = int(partes[1])
                        phred_scores.append(phred)
                    except ValueError:
                        pass

    if not phred_scores:
        print(f"No se encontraron valores de calidad en {nombre_archivo}")
        return None

    calidad_promedio = sum(phred_scores) / len(phred_scores)
    calidad_min = min(phred_scores)
    calidad_max = max(phred_scores)

    print(f"📄 Archivo: {nombre_archivo}")
    print(f"   Bases analizadas: {len(phred_scores)}")
    print(f"   Calidad promedio (Phred): {calidad_promedio:.2f}")
    print(f"   Calidad mínima: {calidad_min}")
    print(f"   Calidad máxima: {calidad_max}")
    print("-" * 50)

    return {
        "archivo": nombre_archivo,
        "bases": len(phred_scores),
        "promedio": calidad_promedio,
        "min": calidad_min,
        "max": calidad_max
    }


def analizar_todos():
    """
    Analiza todos los archivos .phd.1 de la carpeta actual.
    """
    archivos = [f for f in os.listdir("..") if f.lower().endswith(".phd.1")]
    if not archivos:
        print(" No se encontraron archivos .phd.1 en la carpeta actual.")
        return

    print(f" Analizando {len(archivos)} archivo(s)...\n")

    resultados = []
    for archivo in archivos:
        resultado = leer_phd1(archivo)
        if resultado:
            resultados.append(resultado)

    # Guardar en CSV
    if resultados:
        with open("../resultados_phred.csv", "w", encoding="utf-8") as out:
            out.write("Archivo,Bases,Promedio,Min,Max\n")
            for r in resultados:
                out.write(f"{r['archivo']},{r['bases']},{r['promedio']:.2f},{r['min']},{r['max']}\n")

        print("\n Resultados guardados en 'resultados_phred.csv'.")
        print("Verifica que los valores cambien entre archivos para confirmar diferencias reales.")


if __name__ == "__main__":
    analizar_todos()
