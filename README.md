# golfScript v1.0 Beta

Implementación Python de golfScript

Esta es una implementación de juguete de un interprete golfScript. Es una prueba de concepto.


**Instalación**

Copiar los archivos a un directorio.

**Ejecución**

```python gs.py```

inicia una sesión en un REPL.

También puede pasar scripts en la llamada:

```python gs.py "1 1+"```

el script se ejecuta dentro del REPL.

**Pruebas**

El proyecto incluye las pruebas unitarias en el subdirectorio tests.

El programa `batch_test.py test_file` puede usarse para ejecutar
pruebas usando archivos como entrada. Se incluyen los archivos de
prueba `test.src' y `test_complement.src`.

El archivo `builtin-example.gs` contiene más pruebas que se puede
ejecutar dentro de una sesión REPL.

Finalmente, se incluye el interprete oficial de golfScript. Si tiene Ruby instalado, puede ejecutar `ruby golfscript.rb`.

**Notas**

1. Debido a las diferencias de implementación entre Python y Ruby, se producen algunas diferencias en el tratamiento de strings.
2. Los strings no admiten interpolación
3. El REPL no tiene capacidades de edición ni historia.



Candid Moe
Diciembre/2022
 
