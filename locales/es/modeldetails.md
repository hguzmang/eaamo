### Cómputo de los resultados
Las soluciones mostradas han sido cuidadosamente seleccionadas usando el algoritmo. En particular, nuestro mecanismo se asegura de que ninguna solución sea mejor en todos los objetivos que otra de ellas.

Los tamaños de grupo para cada prueba están limitados a 1, 3, 5 o 10 personas por grupo (derivado de tamaños típicos en pruebas grupales).

Para evaluar el plan de pruebas, generamos todas las combinaciones válidas de tamaños de grupo y pruebas asignadas a cada categoría, asegurándonos de que se han utilizado todas las pruebas y que ninguna persona sea probada más de una vez. Después de ello, el algoritmo toma en cuenta los parámetros definidos en las tablas y se calculan los siguientes objetivos:

- El número de infecciones prevenidas.
- El número de aislamientos innecesarios en cada categoría.

Para este ejemplo particular, la calidad de un plan de prueba está expresado en cuatro números: el número esperado de infecciones prevenidas, así como el número de personas en cuarentena innecesaria para cada una de las tres categorías. Después, estas soluciones son ordenadas por el número de infecciones prevenidas y después filtradas, así que las únicas que permanecen están en la frontera de Pareto, lo que significa que ninguna de ellas ha sido superada en todos sus aspectos respecto a otra.

## Detalles del modelo
Los detalles matemáticos de nuestro modelo se encuentran [aquí](assets/companion.pdf).

En esta sección describimos brevemente los parámetros del modelo y se explica de manera general el cómputo de los resultados.

### Parámetros
#### Pobalción de la universidad
El tamaño de la población por categoría se puede observar en la tabla de arriba a la izquierda (aislamientos innecesarios), en la columna de tamaño.

#### Conectividad
Se calculó la cantidad de interacción de personas entre las diferentes categorías de la población, de acuerdo a datos obtenidos del campus. Esto puede resultar en que un estudiante de licenciatura interactúa con 5.47 profesores y 0.73 estudiantes de secundaria/prepa. Similarmente, un profesor puede interactuar con menos profesores, pero con más estudiantes. Véase la tabla de conectividad.


#### Tasas de infección entre categorías
Estar en contacto cercano con personas no es suficiente para que ocurra una infección automáticamente. Dependiendo de la naturaleza de su interacción y las características individuales de cada categoría, usamos diferentes tasas de infección (%) para cada par.

De acuerdo a \[1\], se puede pensar en diferentes probabilidades de infección entre categorías. Véase la tabla de co-infección.

\[1\] Buonanno, G., Morawska, L., & Stabile, L. (2020). Quantitative assessment of the risk of airborne transmission of SARS-CoV-2 infection: Prospective and retrospective applications. Environment international, 145, 106112.  [ver artículo](https://doi.org/10.1016/j.envint.2020.106112)


#### Tasas de infección general
De acuerdo a las estadísticas generales del municipio, se hizo un ajuste considerando que hay muchos casos sin registrar. Véase la tabla de infección.

#### Vulnerabilidad
Una vez infectados, cada categoría tiene diferentes tasas para enfermarse gravemente. Por ahora consideramos que todos enfermarán gravemente.

