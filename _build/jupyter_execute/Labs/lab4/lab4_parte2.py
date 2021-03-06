#!/usr/bin/env python
# coding: utf-8

# **Recuerda que una vez abierto, Da clic en "Copiar en Drive", de lo contrario no podras almacenar tu progreso**
# 
# Nota: no olvide ir ejecutando las celdas de código de arriba hacia abajo para que no tenga errores de importación de librerías o por falta de definición de variables.

# In[ ]:


#configuración del laboratorio
# Ejecuta esta celda!
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
#for local 
#import sys ; sys.path.append('../commons/utils/')
get_ipython().system('wget https://raw.githubusercontent.com/jdariasl/ML_2020/master/Labs/commons/utils/general.py -O general.py --no-cache')
from general import configure_lab4
configure_lab4()
from lab4 import *
GRADER = part_2()
import seaborn as sns


# # Laboratorio 4 - Parte 2. Regularización de modelos.

# En este laboratorio vamos analizar el efecto del sobre-ajuste (*over-fitting*), como identificarlo y como podemos regualizar los modelos para evitarlo o disminuir su efecto. 
# 
# En este laboratorio, vamos a enfocarnos en 2 modelos (usando libreria de sklearn): 
# 
# 1. Regresión logistica 
# 2. MLP
# 
# El sobre-ajuste tambien puede ser causado por la **maldición de la dimensionalidad**. **No vamos enfocarnos en como tratar esta condición** ya que esto lo vamos a ver un poco más adelante cuando evaluemos las tecnicas de selección de caracteristicas.

# Vamos usar [el dataset iris](https://archive.ics.uci.edu/ml/datasets/iris) para realizar nuestra practica. Vamos a convertir el problema a un problema de clasificación biclase

# In[ ]:


x,y = load_wine(return_X_y=True)
unique, counts  = np.unique(y, return_counts=True)
print("distribución original (claves las etiquetas, valores el número de muestras): \n", dict(zip(unique, counts )))
y = np.where(y==0, 0, 1)
unique, counts  = np.unique(y, return_counts=True)
print("distribución luego de conversión (claves las etiquetas, valores el número de muestras): \n", dict(zip(unique, counts )))


# Una de las condiciones para que se presenten sobre-ajustes es tener un conjunto de entrenamiento pequeño. 
# 
# En nuestra practica vamos a simular esta condición para ver que tecnicas podemos usar para reducir el efecto del sobre-ajuste. 
# 
# **Nota**
# 1. En un problema real, si se observa que las medidas de rendimiento no satisfacen las necesidades, la respuesta puede ser que se necesiten más datos en el conjunto de entrenamiento. Las condiciones que usaremos en esta practica son para ver el efecto del sobre ajuste.
# 

# In[ ]:


# simular conjunto de datos pequeño
x, x_test, y, y_test = train_test_split(x, y, test_size=0.6, random_state=10, stratify = y)
scaler = StandardScaler().fit(x)
x = scaler.transform(x)
x_test = scaler.transform(x_test)


# ### Ejercicio 1 - Detectar sobre ajuste

# En nuestro primer ejercicio vamos a crear una función para detectar las diferencias entre los errores de entrenamiento y de prueba.
# 1. calcular error de entrenamiento y prueba
# 2. la función recibe de manera arbitraria un estimador de sklearn
# 3. [usar accuracy score como medida de rendimiento](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score)
# 4. Se debe retornar la diferencia absoluta (solo numeros positivos) entre entrenamiento y prueba.

# In[ ]:


# ejercicio de código
def diff_train_test(Xtrain, Ytrain, Xtest, Ytest, sklearnModel):
    """función que retorna error de entrenamiento
    Xtrain: matriz numpy con las caracteristicas de entrenaniento
    Ytrain: matrix numpy con las etiquetas de entrenamiento
    Xtest: matriz numpy con las caracteristicas de prueba
    Ytest: matrix numpy con las etiquetas de prueba
    sklearnModel: objeto estimador de sklearn ya entrenado
    
    retorna: tupla con tres elementos:
        error entrenamiento, error test y 
        diff absoluta entre error y test
    """
    error_train = accuracy_score(y_true = , y_pred = sklearnModel.predict( ) )
    error_test = accuracy_score(y_true=  , y_pred = sklearnModel.predict( ))
    diff =  
    return (error_train, error_test, diff)
        


# In[ ]:


## la funcion que prueba tu implementacion
GRADER.run_test("ejercicio1", diff_train_test)


# Con la función construida, vamos a usarla para verificar la differencia entre el error de entrenamiento y prueba para los dos modelos que vamos a usar:
# 1. MLP con dos capas, cada una con 64 neuornas. `random_state=1` es usado para lograr tener los mismos resultados siempre
# 2. [Regresión logistica forzada para que no use ninguna regularización](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression). `random_state=1` es usado para lograr tener los mismos resultados

# In[ ]:


mlp = MLPClassifier(hidden_layer_sizes=[20,20], max_iter=500, alpha =1e-6, random_state=1)
mlp.fit(x, y)
# aca usamos el * para pasa cadar elemento como argumento 
print("MLP entrenamiento:{0:.3f}, test:{1:.3f} y diff {2:.3f}".format(*diff_train_test(x,y, x_test, y_test,mlp)))


# In[ ]:


reg = LogisticRegression(penalty='none', max_iter=500,  random_state=1)
reg.fit(x, y)
print("Logistic Regresion entrenamiento:{0:.3f}, test:{1:.3f} y diff {2:.3f}".format(*diff_train_test(x,y, x_test, y_test, reg)))


# ### Ejercicio 2 - Experimentar con MLP regularizado

# Vamos a comenzar regularizar el modelo, el primer metodo que vamos a usar es el de parada anticipada (*early-stopping*). Este ya se encuentra implementado dentro de la libreria, vamos a experimentar con este parametro y el numero de neuronas en el MLP.

# In[ ]:


#@title Pregunta Abierta
#@markdown ¿Explique en sus palabras a que corresponde el metodo de parada anticipada?
respuesta_1 = "" #@param {type:"string"}


# In[ ]:


#@title Pregunta Abierta
#@markdown ¿basandose en la documentación de sklearn para MLPClassifier que relación tiene el parametro validation_fraction con la parada anticipada?
respuesta_2 = "" #@param {type:"string"}


# In[ ]:


# ejercicio de código
def exp_mlp_early_stop(num_neurons, is_early_stop, Xtrain,Xtest,Ytrain, Ytest):
    """ función para realizar experimentos con el MLP con early stopping
    num_neurons: list de enteros con el numero de neuronas a usar
    is_early_stop: list de boolean para confirmar si se aplica early stop
    Xtrain: matriz de numpy con caracteristicas de entrenamiento
    Xtest: matriz de numpy con caracteristicas de prueba
    ytrain: vector numpy con etiqueta de entrenamiento
    ytest: vector numpy con etiqueta de prueba
    
    Retorna: dataframe con 5 columnas:
        - numero de neuronas
        - error de entrenamiento
        - error de prueba
        - diferencia entrenamiento y prueba  
    """
    resultados = pd.DataFrame()
    idx = 0
    for early_stop in is_early_stop:
        for neurons in num_neurons:
            #Haga el llamado a la función para crear y entrenar el modelo usando los datos de entrenamiento
            # prestar atención a los parametros, correctos.
            hidden_layer_sizes = tuple(2*[neurons])
            # llame el parametro que el MLP pare anticipadamente
            mlp = MLPClassifier(hidden_layer_sizes= hidden_layer_sizes, max_iter = 1000,random_state=1 ... )
            # entrenar
            mlp.fit(X=..., y=...)
            # llamar la funcion creada anteriomente
            error_train, error_test, diff = diff_train_test(mlp, Xtrain, Ytrain, Xtest, Ytest)

            resultados.loc[idx,'neuronas en capas ocultas'] = neurons 
            resultados.loc[idx,'error de entrenamiento'] = ...
            resultados.loc[idx,'error de prueba'] = ...
            resultados.loc[idx,'diferencia entrenamiento y prueba'] = ...
            resultados.loc[idx,'is_early_stop'] = early_stop
            idx+=1
    return (resultados)


# In[ ]:


## la funcion que prueba tu implementacion
GRADER.run_test("ejercicio2", exp_mlp_early_stop)


# In[ ]:


res_early_stop = exp_mlp_early_stop( [4,8,16], [True, False], x, x_test, y, y_test)


# In[ ]:


sns.relplot(x = 'neuronas en capas ocultas', y='diferencia entrenamiento y prueba', hue = 'is_early_stop', data = res_early_stop, kind = 'line', aspect=2)


# Ahora vamos a experimentar con el parametro L2 del MLP.

# In[ ]:


#@title Pregunta Abierta
#@markdown ¿explique en sus palabras en qué consiste la regularización L2?
respuesta_3 = "" #@param {type:"string"}


# In[ ]:


# ejercicio de código
def exp_mlp_l2(num_neurons, l2_values, Xtrain,Xtest,Ytrain, Ytest):
    """ función para realizar experimentos con el MLP con regularización L2

    num_neurons: list de enteros con el numero de neuronas a usar
    l2: list de floats con valores para regularizacion l2
    Xtrain: matriz de numpy con caracteristicas de entrenamiento
    Xtest: matriz de numpy con caracteristicas de prueba
    ytrain: vector numpy con etiqueta de entrenamiento
    ytest: vector numpy con etiqueta de prueba
    
    Retorna: dataframe con 5 columnas:
        - numero de neuronas
        - error de entrenamiento
        - error de prueba
        - diferencia entrenamiento y prueba  
    """

    resultados = pd.DataFrame()
    idx = 0
    for l2 in l2_values:
        for neurons in num_neurons:
            #Haga el llamado a la función para crear y entrenar el modelo usando los datos de entrenamiento
            # prestar atención a los parametros, correctos.
            hidden_layer_sizes = tuple(2*[neurons])
            # llame el parametro adecuado del MLPClassifier
            mlp = MLPClassifier(hidden_layer_sizes= hidden_layer_sizes, max_iter = 1000, random_state=1,  ...)
            mlp.fit(X=..., y=...)
            # llamar la funcion creada anteriomente
            error_train, error_test, diff = diff_train_test(...)
            resultados.loc[idx,'neuronas en capas ocultas'] = neurons 
            resultados.loc[idx,'error de entrenamiento'] = ...
            resultados.loc[idx,'error de prueba'] = ...
            resultados.loc[idx,'diferencia entrenamiento y prueba'] = ...
            resultados.loc[idx,'l2'] = l2
            idx+=1
    return (resultados)


# In[ ]:


## la funcion que prueba tu implementacion
GRADER.run_test("ejercicio3", exp_mlp_l2)


# In[ ]:


res_l2 = exp_mlp_l2([4,16,64], [1e-3,1e-1,1e0, 1e1, 2e2, 1e3], x, x_test, y, y_test)


# In[ ]:


sns.relplot(x = 'l2', y='diferencia entrenamiento y prueba',
            hue = 'neuronas en capas ocultas', 
            data = res_l2, kind = 'line', 
            aspect=2, palette=sns.color_palette('viridis', n_colors=res_l2['neuronas en capas ocultas'].nunique()))


# ### Ejercicio 3 - Experimentar con regresión logistica regularizada

# Ahora vamos explorar la opciones de regularización de la regresión logistica. En la libreria se implementan más formas de regularizar, pero solo vamos a comprobar la regularización de norma L2.

# In[ ]:


# ejercicio de código
def exp_reg_l2(l2_values, Xtrain,Xtest,Ytrain, Ytest):
    """ función para realizar experimentos con el MLP con early stopping

    l2_values: list de floats con valores para regularizacion l2
    Xtrain: matriz de numpy con caracteristicas de entrenamiento
    Xtest: matriz de numpy con caracteristicas de prueba
    ytrain: vector numpy con etiqueta de entrenamiento
    ytest: vector numpy con etiqueta de prueba
    
    Retorna: dataframe con 5 columnas:
        - numero de neuronas
        - error de entrenamiento
        - error de prueba
        - diferencia entrenamiento y prueba  
    """
    resultados = pd.DataFrame()
    idx = 0
    for l2 in l2_values:
        #Haga el llamado a la función para crear y entrenar el modelo usando los datos de entrenamiento
        # prestar atención a los parametros, correctos., para lograr
        # la regularizacion deseada (pasar el valor de "l2" directamente al parametro de la libreria asociado)
        reg = LogisticRegression(max_iter = 500, random_state=1, ...)
        reg.fit(X=..., y=...)
        # llamar la funcion creada anteriomente
        error_train, error_test, diff = diff_train_test(...)
        resultados.loc[idx,'error de entrenamiento'] = ...
        resultados.loc[idx,'error de prueba'] = ...
        resultados.loc[idx,'diferencia entrenamiento y prueba'] = ...
        resultados.loc[idx,'l2'] = l2
        idx+=1
    return (resultados)


# In[ ]:


## la funcion que prueba tu implementacion
GRADER.run_test("ejercicio4", exp_reg_l2)


# In[ ]:


reg_l2 = exp_reg_l2([1e-6,1e-3,1e-1,1e0, 1e1], x, x_test, y, y_test)


# In[ ]:


g = sns.relplot(x = 'l2', y='diferencia entrenamiento y prueba',
               data = reg_l2, kind = 'line', 
                aspect=2)

g.set(xscale="log")


# In[ ]:


#@title Pregunta Abierta
#@markdown ¿qué efecto tiene el parametro que controla L2 en la regresión logistica en el overfitting? es diferente al MLP?
respuesta_4= "" #@param {type:"string"}


# ### Ejercicio 4 Efecto del tamaño del conjunto de entrenamiento
# 
# Finalmente como mencionamos anteriormente, en los ejercicios que hemos resuelto, estabamos simulando la situación de un conjunto de datos de entrenamiento pequeño. En nuestro ultimo ejercicio vamos comprobar el efecto del tamaño del conjunto de entrenamiento.

# In[ ]:


# ejercicio de codigo
def train_size_experiments(train_pcts,X,Y,sk_estimator):
    """funcion que realiza experimentos para
        comprobar la influencia del tamaño de conjunto
        de entrenamiento.
    
    train_pcts: lista de floats con los pct de entrenamiento a evaluar
    X: matriz de numpy del conjunto de caracteristicas
    Y: vector numpy con las etiquetas
    sk_estimator: estimador/modelo de sklearn definido (sin entrenar)
    
    Retorna: dataframe con 5 columnas:
        - tamaño del conjunto de entrenamiento
        - error de entrenamiento
        - error de prueba
        - diferencia entrenamiento y prueba 
    """
    resultados = pd.DataFrame()
    idx = 0
    for train_pct in train_pcts:
        #complete el con train_pct
        # preste atencion a que parametro usar!
        # recuerde que son porcentajes
        # ¿que nos asegura el parametro stratify?
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y,  stratify = Y random_state=10, ...)
        # normalizamos
        scaler = StandardScaler().fit(Xtrain)
        Xtrain = scaler.transform(Xtrain)
        Xtest = scaler.transform(Xtest)
        # entrenar!
        sk_estimator.fit(X=..., y=...)
        # llamar la funcion creada anteriomente
        error_train, error_test, diff = diff_train_test(...)
        resultados.loc[idx,'error de entrenamiento'] = ...
        resultados.loc[idx,'error de prueba'] = ...
        resultados.loc[idx,'diferencia entrenamiento y prueba'] = ...
        # complete con el tamaño del entrenamiento
        resultados.loc[idx,'tamaño de entrenamiento'] = ...
        idx+=1
    
    return (resultados)
    


# In[ ]:


## la funcion que prueba tu implementacion
GRADER.run_test("ejercicio5", train_size_experiments)


# In[ ]:


x,y = load_iris(return_X_y=True)
unique, counts  = np.unique(y, return_counts=True)
print("distribución original (claves las etiquetas, valores el número de muestras): \n", dict(zip(unique, counts )))
y = np.where(y==2, 0, 1)
unique, counts  = np.unique(y, return_counts=True)
print("distribución luego de conversión (claves las etiquetas, valores el número de muestras): \n", dict(zip(unique, counts )))


# In[ ]:


# comprobamos con un MLP
mlp = MLPClassifier(hidden_layer_sizes=[64,64], max_iter=1000, random_state=1)
train_size_exp = train_size_experiments([0.2,0.3,0.5,0.7,0.9], x, y, mlp)


# In[ ]:


# vemos las tres medidas
ax = train_size_exp.plot(x="tamaño de entrenamiento", y="error de entrenamiento", color="b", legend=False, figsize = (9,6))
train_size_exp.plot(x="tamaño de entrenamiento", y="error de prueba",  ax=ax, legend=False, color="r")
ax2 = ax.twinx()
ax2.set_ylabel("diff train y test")
ax.set_ylabel("eficiencia")
train_size_exp.plot(x="tamaño de entrenamiento", y="diferencia entrenamiento y prueba", ax=ax2, legend=False, color="k")
ax.figure.legend()
plt.show()


# **Notas Finales** 
# 
# Para tener en cuenta: [Sklearn hay una libreria que realiza algo similar a lo que creamos en el anterior ejercicio.](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.learning_curve.html)

# Debemos notar que en esta practica exageramos algunas situaciones para lograr medir y ver el efecto del sobre-ajuste. En un problema fuera de la didactica del laboratorio un flujo de trabajo ideal es el siguiente:
# 
# <img src="https://scikit-learn.org/stable/_images/grid_search_workflow.png" alt="grid_search_workflow" width="500"/>
# 

# 1. dividimos el conjunto al inicio, reservando un conjunto de test. 
# 2. verificamos los mejores parametros mediante validación cruzada. 
# 3. reentrenamos con los mejores parametros y realizamos la evaluación final. 
# 4. En esta última etapa es donde validamos si existe sobre ajuste. Si existe, se deben incluir parametros para mitigar el sobre ajuste en la validación cruzada y volver al paso 2.

# In[ ]:


#@title Pregunta Abierta
#@markdown Usando lo aprendido, ¿en cuales etapas del anterior proceso se puede detectar el sobre-entrenamiento y aplicar las técnicas de regularización?
respuesta_5 = "" #@param {type:"string"}


# In[ ]:


GRADER.check_tests()


# In[ ]:


#@title Integrantes
codigo_integrante_1 ='' #@param {type:"string"}
codigo_integrante_2 = ''  #@param {type:"string"}


# ----
# esta linea de codigo va fallar, es de uso exclusivo de los profesores
# 

# In[ ]:


GRADER.grade()

