import os
import matplotlib.pyplot as plt

def leer_phd1(nombre_archivo):
    """
    Lee un archivo .phd.1 de secuenciación Sanger
    y devuelve las puntuaciones Phred base a base.
    """
    phred_scores = []
    dentro_dna = False

    with open(nombre_archivo, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            linea = linea.strip()

            # Identifica el bloque BEGIN_DNA ... END_DNA
            if linea.upper().startswith("BEGIN_DNA"):
                dentro_dna = True
                continue
            if linea.upper().startswith("END_DNA"):
                break

            # Extrae valores dentro del bloque
            if dentro_dna and linea:
                partes = linea.split()
                if len(partes) >= 2:
                    try:
                        phred = int(partes[1])
                        phred_scores.append(phred)
                    except ValueError:
                        pass

    return phred_scores


def analizar_archivo(nombre_archivo):
    """
    Analiza un archivo y genera estadísticas + gráfico.
    """
    phred_scores = leer_phd1(nombre_archivo)
    if not phred_scores:
        print(f"⚠️ No se pudieron leer datos de {nombre_archivo}")
        return None

    promedio = sum(phred_scores) / len(phred_scores)
    minimo = min(phred_scores)
    maximo = max(phred_scores)

    # Detectar posiciones con baja calidad (<20)
    bajas = sum(1 for x in phred_scores if x < 20)
    porcentaje_bajas = (bajas / len(phred_scores)) * 100

    print(f"📄 {nombre_archivo}")
    print(f"   Bases: {len(phred_scores)}")
    print(f"   Promedio Phred: {promedio:.2f}")
    print(f"   Mínimo: {minimo}")
    print(f"   Máximo: {maximo}")
    print(f"   % Bases con Phred < 20: {porcentaje_bajas:.2f}%")
    print("-" * 60)

    # Graficar perfil de calidad
    plt.figure(figsize=(10, 4))
    plt.plot(phred_scores, linewidth=1.2)
    plt.axhline(20, color="red", linestyle="--", label="Phred = 20")
    plt.title(f"Perfil de calidad: {nombre_archivo}")
    plt.xlabel("Posición en la secuencia (base)")
    plt.ylabel("Valor Phred")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Crear carpeta de salida si no existe
    os.makedirs("../graficos", exist_ok=True)
    plt.savefig(f"graficos/{nombre_archivo}_calidad.png", dpi=150)
    plt.close()

    return {
        "archivo": nombre_archivo,
        "bases": len(phred_scores),
        "promedio": promedio,
        "min": minimo,
        "max": maximo,
        "porcentaje_bajas": porcentaje_bajas
    }


def analizar_todos():
    """
    Analiza todos los archivos .phd.1 en la carpeta actual.
    """
    archivos = [f for f in os.listdir("..") if f.lower().endswith(".phd.1")]

    if not archivos:
        print("⚠️ No se encontraron archivos .phd.1 en la carpeta actual.")
        return

    print(f"🔍 Analizando {len(archivos)} archivo(s)...\n")
    resultados = []

    for archivo in archivos:
        resultado = analizar_archivo(archivo)
        if resultado:
            resultados.append(resultado)

    # Guardar CSV
    if resultados:
        with open("../resultados_phred.csv", "w", encoding="utf-8") as out:
            out.write("Archivo,Bases,Promedio,Min,Max,%_Phred<20\n")
            for r in resultados:
                out.write(f"{r['archivo']},{r['bases']},{r['promedio']:.2f},{r['min']},{r['max']},{r['porcentaje_bajas']:.2f}\n")

        print("\n Resultados guardados en 'resultados_phred.csv'")
        print(" Gráficos individuales guardados en la carpeta 'graficos/'.")


if __name__ == "__main__":
    analizar_todos()
