# COMPLEJIDAD DE MODELOS Y VALIDACIÓN

## Métricas de evaluación para clasificación

**Tipos de error y matrices de confusión**: <br/> Se introducen las convenciones sobre Falsos Positivos y Falsos Negativos, la matriz de confusión y su uso en el análisis de los errores que comete un sistema de clasificación.

**Medidas de error para problemas de clasificación**: <br/> Se introducen las principales medidas de error para problemas de clasificación y su importancia en la interpretación del desempeño del sistema.

**Medidas de error para problemas desbalanceados**: <br/> Se discute el problema de sesgo en la medición del error de clasificación en problemas desbalanceados y las medidas de error apropiadas para estos casos.

**Figuras de mérito: Curva ROC**: <br/> Se presenta una figura típicamente usada para la evaluación del desempeño de sistemas de clasificación, su interpretación y forma de cálculo.


## Métricas de evaluación para regresión

**Medidas de error para problemas de regresión**: <br/> Se introducen las principales medidas de error para problemas de regresión y se discuten sus ventajas y desventajas.


## Complejidad de datos y complejidad de modelos

**Complejidad de modelos y tamaño de muestra**:  <br/> Se analiza la complejidad de los modelos en términos de las funciones que pueden reconstruir y el efecto que tiene la cantidad de muestras en la complejidad del modelo resultante.

**Sesgo vs Varianza**:  <br/> Se introducen los conceptos de error por sesgo y varianza y su relación con los fenómenos de sobreajuste y subajuste.


## Metodologías de validación

**Validación cruzada vs Bootstrapping (shuffle split)**: <br/> Se presentan los principios de funcionamiento de las metodologías de validación más usadas y algunas de sus variantes.

**Metodologías de validación estratificadas**: <br/> Se discute la necesidad de utilizar variantes apropiadas de las metodologías de validación para problemas de clasificación desbalanceados.

**Metodologías de validación por grupos**: <br/> Se presentan variantes de las metodologías de validación que deben ser usadas en problemas donde las muestras provienen de fuentes similares (grupos de muestras) o en problemas de múltiples instancias (multi-instance learning), en los cuales las suposiciones de independencia entre las muestras no se satisface para todas las muestras y que pueden dar lugar a estimaciones erróneas del desempeño del sistema si no se usan metodologías de validación apropiadas. Se presenta un ejemplo con datos reales en el que además de ver el efecto de usar la validación por grupos, se introduce el uso del método GridSearch para automatizar el proceso de validación. Finalmente, se analizan las curvas de aprendizaje como herramientas para establecer la proporción correcta de muestras de entrenamiento/validación.

## Sobreajuste y regularización

**Sobreajuste**: <br/> Se define el problema de sobreajuste tanto en problemas de clasifiación como de regresión y se introduce la estrategia de parada anticipada que ayuda a evitar el sobreajuste en modelos cuyo algoritmo de entrenamiento se basa en la optimización de una función de costo de manera iterativa.


**Regularización**:  <br/> Se presenta una de las estrategias más ampliamente usadas para evitar el problema de sobreajuste y se muestra su efecto en un modelo de regresión logística.

