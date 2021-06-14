## Guía de usuario

#### Bienvenida

¡Bienvenido(a) a la guía de usuario! El objetivo de la plataforma es guiar al usuario en la asignación de un número fijo de pruebas a través de la población de la universidad de manera óptima. En las siguientes secciones, explicaremos como utilizar esta herramienta.


#### Antecedentes

Esta aplicación web asiste en la búsqueda de la asignación de pruebas que se ajuste mejor a las prioridades de un usuario administrador de una institución. Hemos precargado información de un modelo para una universidad. La sección de detalles del modelo describe la configuración de parámetros.


#### Instrucciones

Para cada solución posible, la gráfica de barras muestra qué tan bien funcionan cada uno de los cuatro objetivos con esta solución. Las barras en morado representan los objetivos de contención, es decir el número de personas que se esperan sean aisladas innecesariamente en esta categoría (menos es mejor). La barra en naranja representa el objetivo en salud, es decir el número de infecciones graves prevenidas (más es mejor).

La tarea de un usuario es seleccionar la solución que mejor se ajuste a las prioridades de su institución. Para ayudarlo en esta tarea, la aplicación le permite establecer umbrales para los diferentes objetivos. Por ejemplo, en el caso de preferir evitar tantas infecciones como sean posibles y que no sea muy importante cuántos individuos se tienen que aislar innecesariamente, se pueden establecer en cero los umbrales de "Aislamientos innecesarios" para cada categoría de la población, y entonces elegir la solución que ofrezca el mayor número de infecciones prevenidas. Sin embargo, esto puede llevar a soluciones donde la universidad no pueda permanecer abierta porque habría muchos profesores en aislamiento. Por lo tanto, estableciendo un umbral de 250 para los profesores, significaría que sería excluida cualquier solución donde haya más de 250 profesores en aislamiento innecesario. Lo mismo podría ser aplicado para cualquiera de las categorías de la población, para efecto de mostrar únicamente las soluciones que se ajusten a sus criterios.

El usuario puede explorar cuántas pruebas se asignan en la solución actual para cada categoría de la población en la sección de "Detalles de la solución" a la derecha.

En general, habrá más de una solución que satisfaga los umbrales. La aplicación le indica cuántas soluciones existen, y el usuario puede explorarlas, una por una, usando la caja de selección.

Si el usuario desea guardar la solución temporalmente, puede oprimir el botón "Guardar" y ésta aparecerá abajo.
