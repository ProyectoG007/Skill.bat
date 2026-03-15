import os

print("=" * 40)
print("RESULTADO DEL PROCESO:")
print("=" * 40)

if os.path.exists("resultado_proceso.txt"):
    with open("resultado_proceso.txt", "r", encoding="utf-8") as f:
        print(f.read())
    os.remove("resultado_proceso.txt")
else:
    print("No hay resultados.")
print("=" * 40)
