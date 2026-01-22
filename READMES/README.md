# data-analysis-testing

# Plan de acción:
1. Crear un agente especializado en la extracción de datos 
2. Configurar al agente para que tome los docs de markdown y cree un json con los docs como objetos - indextados

comprobación importante antes de seguir:
- que el prompt del agente sea suficientemente explicito para que solo guarde en el .json lo más importante
- que no alucine datos

3. Crear otro agente que vectorice mediante embeddings cada doc del .json para crear relaciones entre ellos
4. Comprobar que el clustering funciona

5. Hacer sistema interactivo: test queries 