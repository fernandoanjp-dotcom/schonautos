# Schön Autos: demostraciones independientes

Publicación autorizada por el usuario el 6 de noviembre de 2026 en Fernando's workspace de Render.

## Alcance

- Comparador: `/` (abre la versión editorial por defecto).
- Propuesta editorial: `/editorial/`.
- Propuesta tecnológica/IA: `/ia/`.
- Los tres HTML se conservan byte a byte, incluidas sus fotografías integradas.
- Formularios de demostración: preparan texto localmente, no envían solicitudes ni reservan citas.
- No se altera el dominio del taller ni ningún servicio existente de Cartas Digitales.
- Meta noindex/nofollow y robots.txt con Disallow: /; esto no equivale a control de acceso.

## Publicación

Comando: `python3 demos/schon-autos/build.py`
Directorio público: `demos/schon-autos/public`
Rama aislada: `demo/schon-autos-20261106`

La instantánea original se conserva en un archivo tar.xz dividido en tres fragmentos binarios. El script verifica SHA-256 del archivo y de cada HTML antes de publicar. No descarga dependencias ni incorpora el resto del repositorio al sitio público.

Para editar la demo, extraer con el script y preparar una nueva instantánea comprobada. No fusionar cambios ajenos a esta demostración ni desplegar esta rama en servicios existentes.
