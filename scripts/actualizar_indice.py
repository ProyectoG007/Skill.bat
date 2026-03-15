import os
import json
from datetime import datetime

categorias = sorted(
    [
        d
        for d in os.listdir("scripts")
        if os.path.isdir(os.path.join("scripts", d))
        and d.startswith(("0", "1"))
        and d not in ["000.A_Definir"]
    ]
)

with open("scripts/indice_carpetas.md", "w", encoding="utf-8") as f:
    f.write("# Indice de Carpetas - La Orga\n")
    f.write(f"# Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write("| Categoria | N | Carpeta | Descripcion |\n")
    f.write("|---|---|---|---|\n")
    for cat in categorias:
        for item in sorted(os.listdir(os.path.join("scripts", cat))):
            num = item.split(".")[0]
            desc = "---"
            for meta in ["_meta.json", "package.json", "skill.json", "metadata.json"]:
                ruta = os.path.join("scripts", cat, item, meta)
                if os.path.exists(ruta):
                    try:
                        with open(ruta, "r", encoding="utf-8") as mf:
                            data = json.load(mf)
                            desc = (
                                data.get("description") or data.get("name") or "---"
                            )[:50]
                            break
                    except:
                        pass
            f.write(f"| {cat} | {num} | {item} | {desc} |\n")

print("Indice actualizado!")
