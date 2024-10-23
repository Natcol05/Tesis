import pandas as pd
import datetime as dt 
import numpy as np 
import unicodedata
import matplotlib.pyplot as plt
import plotly as px
import plotly.graph_objects as go
import re
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

df = pd.read_csv("Bases_datos.csv")
df.drop(['El siguiente cuestionario hace parte de una tesis de maestría cuyo objetivo es indagar sobre las dinámicas de violencias basadas en género (VBG) en la Universidad de Antioquia. Su participación es completamente voluntaria y confidencial; puede retirarse en cualquier momento si así lo desea. Los datos serán anónimos y utilizados únicamente con fines académicos. Al continuar con esta encuesta, usted acepta participar de manera voluntaria y comprendiendo que puede omitir cualquier pregunta que le cause incomodidad. Si tiene preguntas, puede contactarme al correo Natalia.loperao@udea.edu.co. \n¿Desea continuar con el cuestionario? ', 'Marca temporal'], axis=1, inplace=True)

#Se le cambian los nombres a las columnas por practicidad
df.rename(columns={'¿Ha sido víctima de alguno de los siguientes hechos al interior de la facultad? Seleccione una o varias opciones.  ': 'victima_facultad',
                   '¿Ha tenido conocimiento de la ocurrencia de alguno de los siguientes hechos al interior de la facultad? Seleccione una o varias opciones': 'conocimiento_hecho',
                   'El último hecho del que tuvo conocimiento o ha sido víctima ocurrió': 'tiempo_ocurrencia',
                   'De los siguientes hechos, seleccione los que considera que tiene mayor ocurrencia en la facultad. (Elija solo dos opciones)': 'hechos_mayor_ocurrencia',
                   'Desde su perspectiva, ¿de cuáles actores suelen provenir en mayor medida los hechos de violencia de género? Seleccione máximo dos opciones. ': 'actores_mayor_ocurrencia',
                   'Desde su perspectiva, ¿en qué espacios suelen ocurrir con mayor frecuencia los hechos de violencia de género? Seleccione 3 opciones máximo': 'lugares_mayor_ocurrencia',
                   '¿Qué iniciativas institucionales para la sensibilización de la violencia de género cconoce ? (Puede elegir multiples opciones)': 'iniciativas_institucionales',
                   'De las siguientes iniciativas ¿a cuántas ha asistido? (Puede elegir multiples opciones)': 'asistencia_instancias',
                   '¿conoce la Ruta Violeta? (Marque una opción del 1 al 5, siendo 1 que no conoce nada y 5 que conoce mucho)': 'conocimiento_ruta_violeta',
                   'Si fueras víctima de violencia de género, ¿a qué dependencia recurriría para hacer la denuncia? (Puede elegir varias opciones). ': 'dependencia_atención',
                   'De los siguientes mecanismos de denuncia no institucional, ¿en cuáles ha participado? (Puede elegir varias opciones)': 'partic_mecanismos_no_insitutionales',
                   'En caso de que usted fuera víctima de violencia de género ¿considera que puede recurrir a la Universidad en busca de ayuda, aunque el hecho se haya producido por fuera de ella?': 'recurrir_universidad_ayuda',
                   '¿Considera la Universidad un entorno seguro? ': 'uni_entorno_seguro',
                   '  ¿Cómo calificaría los mecanismos institucionales para la atención de casos de violencia de género?  ': 'opinión_mecanismos',
                   ' ¿Cómo calificaría las posturas y estrategias del personal administrativo frente a las violencias basadas en género?  ': 'opinion_posturas_admon',
                   ' ¿Cómo calificaría las posturas y estrategias de los docentes frente a las violencias basadas en género?  ': 'opinion_posturas_profes',
                   'En términos generales ¿Cómo describiría al personal administrativo de la facultad?  ': 'opinion_admon_gral',
                   'En términos generales ¿Cómo describiría a los docentes de la facultad?  ': 'opinion_profes_gral',
                   '¿Considera que el trato recibido por parte de los administrativos de la facultad fomenta la confianza, propiciando ambientes idóneos para las denuncias de violencias basadas en género?': 'admon_confianza',
                   '¿Considera que el trato recibido por parte de los docentes de la facultad fomenta la confianza, propiciando ambientes idóneos para las denuncias de violencias basadas en género?' : 'profes_confianza',
                   'De los siguientes aspectos, seleccione los que considera más prioritarios para mejora la atención de los casos de violencia de género. Seleccione máximo 3 opciones  ': 'estrategias_prioritarias',
                   '  Si considera que hay otro aspecto administrativo que la universidad deba mejorar para que la atención de los casos de violencia de género sea efectiva, porfavor mencionelos aquí.   ': 'otras_sugerencias'
            }, inplace=True)

# Se ponen todas las letras en minúscula
df.columns = df.columns.str.lower()
df = df.apply(lambda col: col.map(lambda x: x.lower() if isinstance(x, str) else x))

# Función para eliminar tildes
def eliminar_tildes(texto):
    if isinstance(texto, str):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
    return texto

# Eliminar tildes en nombres de columnas
df.columns = df.columns.map(eliminar_tildes)

# Aplica la función para eliminar tildes en todas las columnas
df = df.apply(lambda col: col.apply(eliminar_tildes))

#Reemplaza los datos ausentes en la columna otras sugerencias por No sabe/No responde
def reemplazar_los_datos_ausentes (df):
    return df.fillna('ns/nr')

df=reemplazar_los_datos_ausentes(df)

# Eliminar espacios al principio y al final, y reemplazar espacios por guiones bajos en múltiples columnas
df[['pregrado', 'semestre']] = df[['pregrado', 'semestre']].apply(lambda col: col.str.strip().str.replace(' ', '_'))

# Eliminar espacios al principio y al final, y reemplazar espacios por guiones bajos en múltiples columnas
df[['pregrado', 'semestre']] = df[['pregrado', 'semestre']].apply(lambda col: col.str.strip().str.replace(' ', '_'))

#Sistematización de pregrados
df['pregrado'] = df['pregrado'].replace({'antropolgia': 'antropologia', 'derecho' : 'antropologia', 'dercho': 'antropologia', 'si': 'historia', 'lic._ciencias_sociales': 'sociologia', 'licenciatura_en_literatura__y_lengua_castellana': 'trabajo_social', 'licenciatura_en_literatura_y_lengua_castellana': 'trabajo_social'})

#sistematización de semestre
df['semestre'] = df['semestre'].replace({'primero': '1', 'sexto': '6', 'segundo': '2', 'dos':'2', 'primer_semestre':'1','tercero': '3', 'cuarto': '4', 'septimo': '7', '4_semestre': '4', 'sexto_semestre': '6', '2do': '2', 'egresado': '8'})

#sistematización genero
df['genero'] = df['genero'].replace({'no-binario':'no binario', 'no binario ': 'no binario', 'no binarie': 'no binario'})

#Se reemplaza la palabra no sabe/no responde por ns/nr
df.replace({'no sabe/no responde': 'ns/nr'}, inplace=True)

# Se crea una función para separar las variables de las preguntas que permitieran opción múltiple
def separate_column(df, column_name):
    # Separar la columna especificada por comas que están fuera de paréntesis
    df_separated = df[column_name].apply(lambda x: re.split(r',\s*(?![^()]*\))', x)).explode().reset_index(drop=True)
    
    # Repetir las filas de 'genero' y 'pregrado' según el número de respuestas separadas
    df_additional = df[['genero', 'pregrado']].loc[df.index.repeat(df[column_name].str.count(',') + 1)]
    
    # Concatenar el DataFrame separado con las columnas adicionales
    result_df = pd.concat([df_additional.reset_index(drop=True), df_separated.rename('opciones_respuesta')], axis=1)
    
    # Eliminar filas con NaN
    result_df = result_df.dropna()
    
    return result_df

#Se crean los Dataframes de las variables con múltiples opciones de respuesta
victima_facultad = separate_column(df, 'victima_facultad')
conocimiento_hecho = separate_column(df, 'conocimiento_hecho')
hechos_mayor_ocurrencia = separate_column(df, 'hechos_mayor_ocurrencia') 
actores_mayor_ocurrencia = separate_column(df, 'actores_mayor_ocurrencia') 
lugares_mayor_ocurrencia = separate_column(df, 'lugares_mayor_ocurrencia')
iniciativas_institucionales = separate_column(df, 'iniciativas_institucionales')
asistencia_instancias = separate_column(df, 'asistencia_instancias')
dependencia_atencion = separate_column(df, 'dependencia_atencion')
partic_mecanismos_no_insitutionales = separate_column(df, 'partic_mecanismos_no_insitutionales')
estrategias_prioritarias = separate_column(df, 'estrategias_prioritarias')

#se eliminan las ',' de todo el dataframe
df = df.apply(lambda col: col.map(lambda x: x.replace(',', '') if isinstance(x, str) else x))

#Se cambia la ultima variable de la columna semestre que faltaba por cambiar, para cambiar el tipo de dato
df['semestre'] = df['semestre'].replace({'5_6_y_7': '7'})
df['semestre'] = df['semestre'].astype(int)

# Se define una función que sustituye los titulos de las variables para que sean más amigable en la gráfica
def reemplazar_categorias(df, columna):
    # Crear un diccionario con las sustituciones
    reemplazos = {
        'comentarios sexistas en el ambito academico (durante clase, asesorias, proyectos de investigacion, etc)': 'comentarios sexistas academico',
        'exclusion o discriminacion en actividades academicas y/o laborales ligadas a la facultad': 'exclusion o discriminación',
        'comentarios sexistas en espacios de interaccion social o esparcimiento': 'comentarios sexistas socialmente',
        'acoso sexual (acoso fisico, verbal, visual)': 'acoso sexual',
        'difusion de contenido sexual no consentido': 'difusion contenido sexual',
        '-exposicion de material audiovisual de estudiantes udea mujeres  en redes sociales no consentido. - "chistes" sexistas en la facultad porcparte de profesores y estudiantes': 'comentarios sexistas academico'
    }
    
    # Aplicar las sustituciones a la columna específica del DataFrame
    df[columna] = df[columna].replace(reemplazos)
    
    return df

#Se aplica la función
reemplazar_categorias(victima_facultad, 'opciones_respuesta')
reemplazar_categorias(conocimiento_hecho, 'opciones_respuesta')
reemplazar_categorias(hechos_mayor_ocurrencia, 'opciones_respuesta')

#Funciones para graficar

# Crear un gráfico de barras interactivo

def gráficas_distribución(df, column_name, title, colors, xlabel, ylabel,
                           use_index_as='y', value_col_as='x', height=400, width=600,
                           size_title=15, size_x=15, size_y=15, size_tick=10):
    # Contar valores y obtener las `top_n` categorías más frecuentes
    counts_bar = df[column_name].value_counts()
    
    #Calcular porcentajes
    percentages = (counts_bar / counts_bar.sum()) * 100
    
    # Seleccionar ejes flexibles
    if use_index_as == 'y' and value_col_as == 'x':
        x_vals = counts_bar.values  # Valores absolutos
        y_vals = counts_bar.index    # Categorías
        orientation = 'h'            # Horizontal (barras horizontales)
        percentages_hover = percentages.values  # Porcentajes
    elif use_index_as == 'x' and value_col_as == 'y':
        x_vals = counts_bar.index
        y_vals = counts_bar.values
        orientation = 'v'            # Vertical (barras verticales)
        percentages_hover = percentages.values  # Porcentajes
    else:
        raise ValueError("Los valores de 'use_index_as' y 'value_col_as' deben ser 'x' o 'y'")

    # Crear el gráfico de barras
    fig = go.Figure(data=[
        go.Bar(
            x=x_vals,  
            y=y_vals,  
            orientation=orientation,
            marker=dict(color=colors[:len(y_vals)], line=dict(color='black', width=0.5)),
            customdata=list(zip(counts_bar.values, percentages_hover)),
            hovertemplate=(
                'No. estudiantes: %{customdata[0]}<br>'  # Valor absoluto
                'Porcentaje: %{customdata[1]:.2f}%<extra></extra>'
            )
        )
    ])
    # Personalización del diseño
    fig.update_layout(
        title={
            'text': title,
            'font': {
                'family': 'Roboto',
                'size': size_title,
                'color': 'black'
            },
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'b': 90}
        },
        xaxis_title={
            'text': xlabel,
            'font': {
                'family': 'Roboto',
                'size': size_x,
                'color': 'black'
            }
        },
        yaxis_title={
            'text': ylabel,
            'font': {
                'family': 'Roboto',
                'size': size_y,
                'color': 'black'
            },
            'standoff': 10
        },
        yaxis=dict(
            automargin=True,
            tickfont=dict(size=size_tick)  
            ),
        xaxis=dict(
            tickfont=dict(size=size_tick)  # Ajustar el tamaño de las etiquetas en el eje x
        ),
        template='plotly_white',  # Estilo del gráfico
        hoverlabel=dict(
            bgcolor="white",  
            font_size=16,         
            font_family="Roboto",  
            font_color='black'
        ),
        margin=dict(l=70, r=30, t=75, b=30),
        width=width,  # Ajusta el ancho de la figura
        height= height  # Ajusta la altura de la figura
    )
    
    # Mostrar el gráfico
    return fig
    

# Crear gráfico de torta
def graficas_circulares(df, column_name, title, height=400, width=600, title_size=15):
    
    counts_circulares = df[column_name].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=counts_circulares.index,
        values=counts_circulares.values,
    marker=dict(colors=['#478cba', 
                        '#ffa3c9', 
                        '#7c8ddd', 
                        '#dba74c'], 
                line=dict(color='black', width = 0.5)),
    textinfo='percent',
    )])
    fig.update_traces(textposition='inside'),
    fig.update_layout(
        uniformtext_minsize=12, 
        uniformtext_mode='hide',
        title={
            'text': title,
            'font': {
                'family': 'Roboto',
                'size': title_size,
                'color': 'black'
                },
            'x': 0.5,  # Centrar el título
            'xanchor': 'center'  # Anclar el título al centro
            },
        template='plotly_white',  # Estilo del gráfico
        hoverlabel=dict(
            bgcolor="white",  
            font_size=16,         
            font_family="Roboto",  
            font_color='black',
        ),
        margin=dict(l=70, r=95, t=80, b=15),  # Ajusta los márgenes izquierdo, derecho, superior e inferior
        height=height,  # Ajusta la altura del gráfico
        width=width,   # Ajusta el ancho del gráfico
        showlegend=True  # Asegúrate de que la leyenda esté activa
        )
    # Mostrar el gráfico
    return fig

# Distrubición de estudiantes por pregrados
estudiantes_pregrado = gráficas_distribución(df, 'pregrado', 'Distribución de Estudiantes por Pregrado',
                      ['#9b6ba9', '#cd6e96', '#ef9997', '#418eb7', '#d1aebf'], 
                      'Pregrado', 'Cantidad', use_index_as='x', value_col_as='y',
                      height=250, width=550, size_title=15, size_x=12, size_y=12, size_tick=10)

#Distribución de estudiantes por semestre
estudiantes_semestre = gráficas_distribución(df, 'semestre', 
                      'Distribución de Estudiantes por Semestre',
                      ['#d1aebf', '#9977b6', '#ea96b9','#9b6ba9', '#ef9997', '#faa67b', 
                       '#efb99e', '#418eb7', '#ffbc5c', '#57a4ba'],
                      'Semestre', 'Cantidad', use_index_as='x', value_col_as='y', height=300, width=360,
                           size_title=15, size_x=12, size_y=12, size_tick=10)

#Distribución de estudiantes por género
estudiantes_genero = graficas_circulares(df, 'genero', 'Distribución de Estudiantes por Género', 
                                         height=250, width=365, title_size=15)

#Víctimas de VBG
victimas =gráficas_distribución(victima_facultad,
                      'opciones_respuesta', 
                      'Número de Víctimas de Violencia basada en Género',
                      ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9', '#ef9997',
                       '#faa67b', '#efb99e','#418eb7', '#d1aebf' '#d1aebf'],
                       'Cantidad','Hecho', use_index_as='y', value_col_as='x', height=400, width=450,
                           size_title=15, size_x=15, size_y=15, size_tick=10)

#Conocimiento de hechos de VBG en la facultad
conocimiento_hechos = gráficas_distribución(conocimiento_hecho, 'opciones_respuesta', 
                      'Conocimiento de Hechos de Violencia Basada en Género', 
                      ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9', '#ef9997',
                       '#faa67b', '#efb99e'], 
                      'Cantidad', 'Hechos', use_index_as='y', value_col_as='x', height=400, width=450,
                           size_title=15, size_x=15, size_y=15, size_tick=10)

#Hechos de mayor ocurrencia
hechos_mayor_ocurrencia['opciones_respuesta']=hechos_mayor_ocurrencia['opciones_respuesta'].replace({' comentarios sexuales en el ambito academico (durante clase, asesorias, proyectos de investigacion, etc)':'comentarios sexistas académico',
                                                                                                     'comentarios sexuales en el ambito academico (durante clase, asesorias, proyectos de investigacion, etc)': 'comentarios sexistas académico'})
hechos_comunes = gráficas_distribución(hechos_mayor_ocurrencia, 'opciones_respuesta', 
                      'Hechos Violencia Basada en Género de Mayor Ocurrencia', 
                      ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9', '#ef9997',
                       '#faa67b', '#efb99e'], 
                       'Cantidad', 'Hecho', use_index_as='y', value_col_as='x', height=400, width=450,
                       size_title=15, size_x=15, size_y=15, size_tick=10)

#Tiempo de ocurrencia del último hecho
tiempo_ocurrencia = graficas_circulares(df, 'tiempo_ocurrencia', '¿Hace Cuanto Tiempo Ocurrió el Hecho?', 
                                        height=400, width=450, title_size=15)

#Actores mayormente implicados
actores_mayor_ocurrencia['opciones_respuesta'] = actores_mayor_ocurrencia['opciones_respuesta'].replace({'companero sexual o afectivo que tambien es estudiante':'pareja sexoafectiva estudiante', 
                                                                                                         'actores externos al rededor de la universidad': 'actores externos'})
actores_comunes = graficas_circulares(actores_mayor_ocurrencia, 'opciones_respuesta', 
                                      'Actores Más Relacionados a las Violencias Basadas en Género',
                                      height=350, width=450, title_size=15)

#Lugares donde suelen ocurrir mas casos de VBG
lugares_mayor_ocurrencia['opciones_respuesta'] = lugares_mayor_ocurrencia['opciones_respuesta'].replace({'practicas y/o salidas de campo': 'salidas de campo',
                                                                                                         'espacios de interaccion social (plazoleta, jardineras, etc)': 'lugares de ocio en la u',
                                                                                                         'alrededores de la universidad': 'alrededores de la u'})
lugares_comunes = gráficas_distribución(lugares_mayor_ocurrencia, 'opciones_respuesta', 
                      'Lugares de Mayor Incidencia de Violencias Basadas en Género',
                      ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9', '#ef9997',
                       '#faa67b', '#efb99e'], 'Cantidad', 'Lugares', use_index_as='y', value_col_as='x',
                      height=400, width=450, size_title=15, size_x=15, size_y=15, size_tick=10)

#Conocimiento iniciativas institucionales para prevenir las VBG
iniciativas_institucionales['opciones_respuesta'] = iniciativas_institucionales['opciones_respuesta'].replace({'conversatorios e iniciativas culturales y artisticas': 'conversatorios/eventos artistico-culturales',
                                                                                                               'catedra del cuidado de si (nataly palacios)': 'catedra Nataly Palacios'})
iniciativas_institucionales_graph = gráficas_distribución(iniciativas_institucionales, 'opciones_respuesta', 
                                                          'Conocimiento de Iniciativas Institucionales contra las VBG',
                                                          ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9',
                                                           '#ef9997', '#faa67b', '#efb99e'], 'Cantidad', 'Iniciativas',
                                                          use_index_as='y', value_col_as='x', height=250, width=500, 
                                                          size_title=15, size_x=15, size_y=15, size_tick=10)

#Conocimiento de la ruta violeta
ruta_violeta = gráficas_distribución(df, 'conocimiento_ruta_violeta', 
                                     'Conocimiento de la Ruta Violeta en una escala del 1 al 5', 
                                     ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9', '#ef9997',
                                      '#faa67b', '#efb99e'], 'Escala', 'Cantidad',  use_index_as='x',
                                     value_col_as='y', height=250, width=500, size_title=15, size_x=15,
                                     size_y=15, size_tick=10)

#Mecanismos de atención institucional para VBG
dependencia_atencion['opciones_respuesta'] = dependencia_atencion['opciones_respuesta'].replace({
'centro de atencion en genero y diversidad sexual': 'CAGDS', 
'unidad de asuntos disciplinarios (uad)' : 'uad',
'no haria la denuncia ': 'no denunciaria',
'colectivos feministas de la facultad': 'colectivos feministas',
'fiscalia ': 'fiscalia',
'no haria la denuncia': 'no denunciaria',
'lineas de atencion telefonica o via email': 'linea telefonica/email'
})

mecanismos_inst = gráficas_distribución(dependencia_atencion, 'opciones_respuesta', 
                      'Mecanismos Institucionales Donde las Víctimas<br> Podrían Solicitar Ayuda', 
                      ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9', '#ef9997', '#faa67b', 
                       '#ff9d50', '#efb99e', '#78aed3'], 'Cantidad', 'Dependencias', 
                      use_index_as='y', value_col_as='x', height=280, width=350, size_title=15, size_x=12,
                      size_y=12, size_tick=10)

#Participación en mecanismos de denuncia no institucional
partic_mecanismos_no_insitutionales['opciones_respuesta'] = partic_mecanismos_no_insitutionales['opciones_respuesta'].replace({
'divulgacion en medios independientes como revistas' : 'divulgación independiente',
'he ido a marchas y difusion de material por internet antes de estar en la u': 'protestas',
'espacios asamblearios motivadas por vbg': 'asambleas',
'contarle a las parceras ': 'comentar amigas/os',
'contar a las amigas' : 'comentar amigas/os'
})

mecanismos_no_inst = gráficas_distribución(partic_mecanismos_no_insitutionales, 'opciones_respuesta', 
                      'Participación en Mecanismos de<br> Denuncia no Institucionales', 
                      ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9', '#ef9997', '#faa67b', '#ff9d50'], 
                      'Dependencias', 'Cantidad', use_index_as='y', value_col_as='x', height=280, width=350, 
                      size_title=15, size_x=12, size_y=12, size_tick=10)

#Participación en iniciativas institucionales de prevención de VBG
asistencia_instancias['opciones_respuesta'] = asistencia_instancias['opciones_respuesta'].replace({'conversatorios e iniciativas culturales y artisticas': 'conversatorios/eventos artistico-culturales',
                                                                                                               'catedra del cuidado de si (nataly palacios)': 'catedra Nataly Palacios'})

par_mecanismos_inst = gráficas_distribución(asistencia_instancias, 'opciones_respuesta', 
                      'Participación en Mecanismos de<br> Denuncia Institucionales', 
                      ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9', '#ef9997', '#faa67b', '#ff9d50'], 
                      'Cantidad', 'Dependencias', use_index_as='y', value_col_as='x', height=250, width=500, 
                      size_title=15, size_x=12, size_y=12, size_tick=10)

#Niveles de confianza en la universidad para denunciar VBG
confianza_u = graficas_circulares(df, 'recurrir_universidad_ayuda',
                                  'Percepción Estudiantil:<br> ¿Confían en la U ante Casos de VBG?',
                                  height=280, width=380, title_size=15)

#Percepción de la univerisdad como un entorno seguro
u_segura = graficas_circulares(df, 'uni_entorno_seguro', 
                               '¿Es la Universidad un Entorno Seguro?<br> Opiniones de los Estudiantes',
                               height=280, width=380, title_size=15)

#Percepción de efectividad en mecanismos de atención institucional
efectividad_mecanismos = graficas_circulares(df, 'opinion_mecanismos', 
                                             'Opinión Estudiantil sobre la Efectividad de los<br> Mecanismos de Atención de VBG Institucionales',
                                             height=280, width=380, title_size=15)

#Percepción sobre las posturas de la administración frente a las VBG
posturas_admon = graficas_circulares(df, 'opinion_posturas_admon', 
                                     'Percepción de las Posturas del Personal<br> Administrativo Sobre VBG',
                                     height=280, width=350, title_size=15)

#Percepción de las posturas de los docentes frente a las VBG
posturas_profes = graficas_circulares(df, 'opinion_posturas_profes', 
                                      'Percepción de las Posturas de los<br> Docentes Sobre VBG',
                                      height=280, width=350, title_size=15)

#Percepción de los estudiantes frente al comportamiento general de los administrativos
df['opinion_admon_gral'] = df['opinion_admon_gral'].replace('colaborativo proactivo','colaborativo/proactivo')
gral_admon = graficas_circulares(df, 'opinion_admon_gral', 'Percepción General del Personal Administrativo',
                                 height=280, width=360, title_size=15)

#Percepción de los estudiantes frente al comportamiento general de los docentes
df['opinion_profes_gral'] = df['opinion_profes_gral'].replace('colaborativo proactivo', 'colaborativo/proactivo')
gral_profes = graficas_circulares(df, 'opinion_profes_gral', 'Percepción General de los Docentes',
                                  height=280, width=365, title_size=15)

#Niveles de confianza en el personal administrativo para denuncias de VBG
confianza_admon = graficas_circulares(df, 'admon_confianza', 
                                      'Percepción sobre la Confianza en los<br> Administrativos para Denunciar VBG',
                                      height=280, width=350, title_size=15)

#Niveles de confianza en el personal docente para denuncias de VBG
confianza_profes = graficas_circulares(df, 'profes_confianza', 
                                       'Percepción sobre la Confianza en los Docentes<br> para Denunciar VBG',
                                       height=280, width=350, title_size=15)

#Estrategias prioritarias para mejorar la gestión y prevención de hechos de VBG
estrategias_prioritarias['opciones_respuesta'] = estrategias_prioritarias['opciones_respuesta'].replace({
'mayor inclusion de los/las estudiantes en el diseno de los protocolos y rutas de atencion': 'inclusion estudiantes',
'aumental la confianza de los estudiantes en los mecanismos institucionales': 'aumento confianza',
'diseno de protocolos y rutas de atencion mas claras y amigables para los/las estudiantes': 'claridad protocolos',
'personal mas empatico y capacitado para atender a las victimas': 'empatia del personal',
'mayor difusion de los protocolos y rutas de atencion' : 'difusion protocolos'    
})

mejorar = gráficas_distribución(estrategias_prioritarias, 'opciones_respuesta', 
                      'Como Mejorar la Atención y Prevensión a VBG', 
                      ['#9b6ba9', '#9977b6', '#b4a6bf', '#d1aebf', '#ea96b9', '#ef9997', '#faa67b', '#ff9d50'], 
                      'Cantidad', 'Elementos a Mejorar', height=250, width=500, size_title=15, size_x=12, size_y=12, size_tick=10)

#Diseño de la app
app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'
])

# Datos de ejemplo para las gráficas
data = {
    'Inicio': 'Bienvenido al dashboard sobre Violencias de Género. Selecciona una categoría para ver los resultados.',
    'Caracterización': ['estudiantes_genero'],
    'Violencias BVG': ['victimas', 'conocimiento_hechos', 'hechos_comunes',
                       'tiempo_ocurrencia', 'actores_comunes', 'lugares_comunes'],
    'Mecanismos de Atención': ['iniciativas_institucionales_graph', 'ruta_violeta', 'mecanismos_inst', 'mecanismos_no_inst'],
    'Opiniones':['ABC']
    }

image_list = ['1.png', '2.png', '3.png', '4.png', '5.png','6.png', '7.png', '8.png', '9.png','10.png',
              '11.png','12.png', '13.png', '14.png']

# Definir el layout del dashboard
app.layout = html.Div(
    style={
        'width': '80%',
        'max-width': '1200px',
        'min-height': '80vh',  
        'margin': 'auto',  
        'padding': '20px', 
        'backgroundColor': '#33691e' 
    },
    children=[
        html.Div(
            children=[
                html.H1("Retos y Estrategias en la Lucha contra las Violencias de Género en la Facultad de Ciencias Sociales y Humanas de la Universidad de Antioquia", style={
                    'textAlign': 'center',  # Centrar el texto
                    'color': 'black',        # Color del texto
                    'fontSize': '19px'
                })
            ],
            style={
                'backgroundColor': 'white',  
                'padding': '20px',           # Espaciado interno
                'borderRadius': '5px',       # Bordes redondeados
                'height': '20px',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'fontFamily': 'Roboto, sans-serif',
                'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0.1)'  
            }
        ), html.Div(
            children=[
                html.Button(cat, id=cat, n_clicks=0, style={
                    'margin': '7px',
                    'padding': '10px',
                    'backgroundColor': '#33691e',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer'}
                ) for cat in data.keys()
            ], 
            style={
                'textAlign': 'center',
                'marginBottom': '5px'}
        ), 
        html.Div(
            id='graficas-container',  # ID para poder referenciar este Div más tarde
            style={
                'backgroundColor': 'white',  # Fondo blanco para las gráficas
                'margin': '5px',
                'height' : '100%',
                'padding': '10px',           # Espaciado interno
                'borderRadius': '5px',       # Bordes redondeados
                'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0.1)',  # Sombra sutil
                #'minHeight': '250px',
                #'minWidth': '150px',
                'display' : 'flex'
                }
        )
    ]
)

@app.callback(
    Output('mi-grafica', 'figure'),
    [Input('dropdown-graficas', 'value')]
)
def update_dropdown_graph(selected_value):
    # Dependiendo del valor seleccionado en el dropdown, mostramos una gráfica diferente
    if selected_value == 'victimas':
        return victimas  # Aquí pones la gráfica que quieras para 'Gráfica de víctimas'
    elif selected_value == 'conocimiento_hechos':
        return conocimiento_hechos  # Gráfica para 'Gráfica de delitos'
    elif selected_value == 'hechos_mayor_ocurrencia':
        return hechos_comunes  # Gráfica para 'Gráfica de denuncias'
    elif selected_value == 'tiempo_ocurrencia':
        return tiempo_ocurrencia 
    elif selected_value == 'actores_comunes':
        return actores_comunes
    elif selected_value == 'lugares_comunes':
        return lugares_comunes

@app.callback(
    Output('mi-grafica_mecanismos', 'figure'),
    [Input('dropdown-graficas_mecanismos', 'value')]
)
def update_dropdown_graph_mecanismos(selected_value):
    # Dependiendo del valor seleccionado en el dropdown, mostramos una gráfica diferente
    if selected_value == 'iniciativas_institucionales_graph':
        return iniciativas_institucionales_graph  
    elif selected_value == 'ruta_violeta':
        return ruta_violeta  
    elif selected_value == 'par_mecanismos_inst':
        return par_mecanismos_inst 
    
@app.callback(
    Output('primera-grafica', 'figure'),
    [Input('dropdown-mecanismos', 'value')]
)
def update_dropdown_mecanismos(selected_value):
    # Dependiendo del valor seleccionado en el dropdown, mostramos una gráfica diferente
    if selected_value == 'mecanismos_inst':
        return mecanismos_inst  
    elif selected_value == 'mecanismos_no_inst':
        return mecanismos_no_inst 
    
    
@app.callback(
    Output('segunda-grafica', 'figure'),
    [Input('dropdown-segunda-grafica', 'value')]
)
def update_dropdown_mecanismos(selected_value):
    # Dependiendo del valor seleccionado en el dropdown, mostramos una gráfica diferente
    if selected_value == 'efectividad_mecanismos':
        return efectividad_mecanismos  # Aquí pones la gráfica que quieras para 'Gráfica de víctimas'
    elif selected_value == 'u_segura':
        return u_segura  # Gráfica para 'Gráfica de delitos'
    elif selected_value == 'confianza_u':
        return confianza_u

@app.callback(
    Output('tercer-grafica', 'figure'),
    [Input('dropdown-tercer-grafica', 'value')]
)
def update_dropdown_mecanismos(selected_value):
    # Dependiendo del valor seleccionado en el dropdown, mostramos una gráfica diferente
    if selected_value == 'posturas_profes':
        return posturas_profes  # Aquí pones la gráfica que quieras para 'Gráfica de víctimas'
    elif selected_value == 'gral_profes':
        return gral_profes  # Gráfica para 'Gráfica de delitos'
    elif selected_value == 'confianza_profes':
        return confianza_profes
    
@app.callback(
    Output('cuarta-grafica', 'figure'),
    [Input('dropdown-cuarta-grafica', 'value')]
)
def update_dropdown_mecanismos(selected_value):
    # Dependiendo del valor seleccionado en el dropdown, mostramos una gráfica diferente
    if selected_value == 'posturas_admon':
        return posturas_admon  # Aquí pones la gráfica que quieras para 'Gráfica de víctimas'
    elif selected_value == 'gral_admon':
        return gral_admon  # Gráfica para 'Gráfica de delitos'
    elif selected_value == 'confianza_admon':
        return confianza_admon
    
# Callback para actualizar la imagen al hacer clic en los botones de navegación
@app.callback(
    Output('displayed-image', 'src'),
    [Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')],
    [State('displayed-image', 'src')]
)
def update_image(prev_clicks, next_clicks, current_image_src):
    # Encuentra el índice actual de la imagen mostrada
    current_image = current_image_src.split('/')[-1]  # Extrae el nombre de la imagen del src actual
    current_index = image_list.index(current_image)
    
    # Calcula el nuevo índice según el botón clicado
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_image_src
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'prev-button':
        new_index = (current_index - 1) % len(image_list)  # Ir hacia atrás
    elif button_id == 'next-button':
        new_index = (current_index + 1) % len(image_list)  # Ir hacia adelante
    else:
        new_index = current_index

    # Devuelve la nueva imagen para mostrar
    return f'/assets/{image_list[new_index]}'
    
@app.callback(
    Output('graficas-container', 'children'),
    [Input(cat, 'n_clicks') for cat in data.keys()]
)
def update_graphs(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'backgroundColor': 'white',
                'border': '2px solid black',
                'borderRadius': '10px',
                'padding': '5px'
            },
            children=[
                html.Div(
                    id='image-container',
                    children=[
                        # Muestra la imagen inicial
                        html.Img(id='displayed-image', src=f'/assets/{image_list[0]}',
                                 style={'width': '100%', 'height': '500px', 'objectFit': 'contain',
                                        'maxHeight': '400px', 'minWidth':'300px'}),
                    ],
                    style={'width': '80%', 'position': 'relative'}
                ),
                html.Div(
                    children=[
                        html.Button('<', id='prev-button', style={'fontSize': '24px', 'margin': '5px'}),
                        html.Button('>', id='next-button', style={'fontSize': '24px', 'margin': '5px'}),
                    ],
                    style={'display': 'flex', 'justifyContent': 'center'}
                )
            ]
        )
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id in data:
        if button_id == 'Inicio':
            return html.Div(
                style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'alignItems': 'center',
                    'backgroundColor': 'white',
                    'border': '2px solid black',
                    'borderRadius': '10px',
                    'padding': '5px'
                },
                children=[
                    html.Div(
                        id='image-container',
                        children=[
                            html.Img(id='displayed-image', src=f'/assets/{image_list[0]}', 
                                     style={'width': '100%', 'height': '500px', 'objectFit': 'contain', 
                                            'maxHeight': '400px', 'minWidth':'300px'}),
                        ],
                        style={'width': '80%', 'position': 'relative'}
                    ),
                    html.Div(
                        children=[
                            html.Button('<', id='prev-button', style={'fontSize': '24px', 'margin': '5px'}),
                            html.Button('>', id='next-button', style={'fontSize': '24px', 'margin': '5px'}),
                        ],
                        style={'display': 'flex', 'justifyContent': 'center'}
                    )
                ]
            ),
        elif button_id == 'Caracterización':
            return html.Div(
                style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'padding': '3px',  # Reduce el padding
                    'backgroundColor': 'white',
                    'borderRadius': '5px',
                    'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0)',
                    'height': '50%',
                    },
                children=[
                    html.Div(
                        style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'padding': '0px',  # Reduce el padding
                            'margin': '0px',  # Reduce el margin
                            'backgroundColor': 'white',  
                            'borderRadius': '5px',
                            'height': '100%',
                            },
                        children=[
                            dcc.Graph(
                                figure=estudiantes_pregrado,
                                config={'responsive': True},  # Hacer que la gráfica sea responsiva
                                style={'height': '100%', 
                                       'width': '80%',
                                       'marginLeft': 'auto', 
                                       'marginRight': 'auto',}
                                )
                            ]
                        ),               
                    html.Div(
                        style={
                            'display': 'flex',  # Cambiado a flex para poner gráficos uno al lado del otro
                            'padding': '2px',  # Reduce el padding
                            'backgroundColor': 'white',
                            'borderRadius': '5px',
                            'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0)',  # Mejorar la sombra
                            'height': '50%', 
                            },
                        children=[
                            html.Div(
                                style={'flex': '1', 'display': 'flex', 'justifyContent': 'center'},
                                children=[
                                    dcc.Graph(
                                        figure=estudiantes_genero,  # Reemplaza con la figura correspondiente
                                        config={'responsive': True},
                                        style={'height': '100%', 'width': '100%'}
                                        )
                                    ]
                                ),
                            html.Div(
                                style={'flex': '1', 'display': 'flex', 'justifyContent': 'center'},
                                children=[
                                    dcc.Graph(
                                        figure=estudiantes_semestre, 
                                        config={'responsive': True},
                                        style={'height': '100%', 'width': '100%'}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )  
        elif button_id == 'Violencias BVG':
            return html.Div(
                style={
                    'display': 'flex',
                    'flexDirection': 'row',  # Alinear en fila
                    'padding': '10px',
                    'backgroundColor': 'white',  # Color del fondo del contenedor principal
                    'borderRadius': '5px',
                    'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0)',
                    'height': '90%',
                    'width': '100%',  # Asegúrate de que ocupe el ancho completo
                    'minHeight': '400px'
                    },
                children=[
                    html.Div(
                        style={
                            'flex': '1',  # Ocupa un espacio razonable en el lado izquierdo
                            'padding': '15px',  # Más espacio interno (padding)
                            'backgroundColor': '#dfdac3',  # Color crema para el texto
                            'borderRadius': '5px',  # Bordes redondeados
                            'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0.1)',  # Sombra
                            'height': '100%',  # Ocupa todo el alto del contenedor
                            'minHeight': '500px',
                            'marginRight': '10px'  # Separación entre texto y gráfica
                            },
                        children=[
                            html.H1("Estrategias", style={
                                'textAlign': 'center',  # Centrar el texto
                                'color': 'black',        # Color del texto
                                'fontSize': '19px'
                                }),
                            html.P("Aunque el 42.6% de los estudiantes no ha sido víctima directa, el 94% conoce de casos que afectaron a terceros, lo que refleja la necesidad de mecanismos efectivos de prevención y atención. Se deben priorizar programas dirigidos a prevenir el acoso sexual (36.1%) y los comentarios sexistas en espacios de ocio (31.5%) y en el ámbito académico (16.1%). Asimismo, es clave involucrar tanto a estudiantes (41%) como a docentes (29.3%) en estos esfuerzos, y prestando atención a que los lugares de mayor incidencia son los espacios de ocio (22.1%) y alrededores de la universidad (19.4%).", 
                                   style={'color': 'black',
                                          'textAlign': 'justify'}), 
                            ]
                        ),
                    html.Div(
                        style={
                            'flex': '2',  # Ocupa más espacio que el texto
                            'padding': '15px',
                            'backgroundColor': 'white',  # Color blanco para la gráfica
                            'borderRadius': '5px',  # Bordes redondeados
                            'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0)',  # Sombra
                            'height': '100%',  # Ocupa todo el alto del contenedor
                            },
                        children=[
                            dcc.Dropdown(
                                id='dropdown-graficas',
                                options=[
                                    {'label': 'Víctimas de VBG', 'value': 'victimas'},
                                    {'label': 'Conocimiento de Hechos de VBG', 'value': 'conocimiento_hechos'},
                                    {'label': 'Hechos de Mayor Ocurrencia', 'value': 'hechos_mayor_ocurrencia'},
                                    {'label': 'Hace Cuánto Ocurrió el Hecho', 'value': 'tiempo_ocurrencia'},
                                    {'label': 'Actores Comunes', 'value': 'actores_comunes'},
                                    {'label': 'Lugares con Mayor Ocurrencia de VBG', 'value': 'lugares_comunes'},
                                    ],
                                value='victimas',  # Valor inicial
                                multi=False,  # Permitir seleccionar solo una gráfica a la vez
                                style={'width': '100%', 'marginBottom': '20px'}
                                ),
                            dcc.Graph(
                                id='mi-grafica',  
                                config={'responsive': True},
                                style={'height': '100%', 'width': '100%'}
                                ),
                            ]
                        ),
                    ]
                )
        elif button_id == 'Mecanismos de Atención':
            return html.Div(
                style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'padding': '3px',  # Reduce el padding
                    'backgroundColor': 'white',
                    'borderRadius': '5px',
                    'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0)',
                    'height': '50%',
                    },
                children=[
                    html.Div(
                        style={
                            #'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'padding': '0px',  # Reduce el padding
                            'margin': '0px',  # Reduce el margin
                            'backgroundColor': 'white',  
                            'borderRadius': '5px',
                            },
                        children=[
                            dcc.Dropdown(
                                id='dropdown-graficas_mecanismos',
                                options=[
                                    {'label': 'Conocimientos Iniciativas Institucionales', 'value': 'iniciativas_institucionales_graph'},
                                    {'label': 'Participación Mecanismos Inst', 'value': 'par_mecanismos_inst'},
                                    {'label': 'Conocimiento Ruta Violeta', 'value':'ruta_violeta'}
                                    ],
                                value='iniciativas_institucionales_graph',  # Valor inicial
                                multi=False,  # Permitir seleccionar solo una gráfica a la vez
                                style={'width': '70%',
                                       'height' : '80%', 
                                       'marginBottom': '1px',
                                       'marginLeft': 'auto', 
                                       'marginRight': 'auto',
                                       'padding':'1px'
                                       #'display': 'block'
                                       }      
                                ),
                            dcc.Graph(
                                id= 'mi-grafica_mecanismos',
                                config={'responsive': True},  # Hacer que la gráfica sea responsiva
                                style={'height': '70%', 
                                       'width': '80%',
                                       'marginLeft': '100px',
                                       'marginRight': '20px',
                                       'display': 'block'
                                       }
                                )
                            ]
                        ),               
                    html.Div(
            style={
                'display': 'flex',  # Usar flex para que las gráficas estén lado a lado
                'padding': '2px',  # Reduce el padding
                'backgroundColor': 'white',
                'borderRadius': '5px',
                'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0)',  # Mejorar la sombra
                'height': '50%',
            },
            children=[    
                # Primera gráfica con su Dropdown
                html.Div(
                    style={
                        'flex': '1', 
                        'display': 'flex', 
                        'flexDirection': 'column', 
                        'alignItems': 'center'
                    }, 
                    children=[
                        dcc.Dropdown(
                            id='dropdown-mecanismos',
                            options=[
                                {'label': 'Mecanismos Institucionales', 'value': 'mecanismos_inst'},
                                {'label': 'Mecanismos NO Institucionales', 'value': 'mecanismos_no_inst'}
                            ],
                            value='mecanismos_inst',  # Valor inicial
                            style={'width': '80%', 'marginBottom': '10px'},  # Ajustar el tamaño y margen
                        ),
                        dcc.Graph(
                            id='primera-grafica',  # Agrega un ID para la gráfica
                            figure=mecanismos_inst,  # Reemplaza con la figura correspondiente
                            config={'responsive': True},
                            style={'height': '100%', 'width': '100%'}
                        )
                    ]
                ), html.Div(
                    style={
                        'flex': '1', 
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center'
                    }, 
                    children=[
                        dcc.Dropdown(
                            id='dropdown-segunda-grafica',
                            options=[
                                {'label': 'Efectividad Mecanismos', 'value': 'efectividad_mecanismos'},
                                {'label': 'Confianza en la U', 'value': 'confianza_u'},
                                {'label': 'U Entorno Seguro', 'value': 'u_segura'},
                            ],
                            value='efectividad_mecanismos',  # Valor inicial
                            style={'width': '80%', 'marginBottom': '10px'},  # Ajustar el tamaño y margen
                        ),
                        dcc.Graph(
                            id='segunda-grafica',  # Agrega un ID para la gráfica
                            figure=efectividad_mecanismos,  # Reemplaza con la figura correspondiente
                            config={'responsive': True},
                            style={'height': '100%', 'width': '100%'}
                        )
                    ])
            ])
                ]),                    
        elif button_id == 'Opiniones':
            return html.Div(
                style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'padding': '3px',  # Reduce el padding
                    'backgroundColor': 'white',
                    'borderRadius': '5px',
                    'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0)',
                    'height': '50%',
                    },
                children=[
                    html.Div(
                        style={
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'padding': '0px',  # Reduce el padding
                            'margin': '0px',  # Reduce el margin
                            'backgroundColor': 'white',
                            'borderRadius': '5px',
                            },
                        children=[
                            dcc.Graph(
                                figure=mejorar,
                                config={'responsive': True},  # Hacer que la gráfica sea responsiva
                                style={
                                    'height': '70%',
                                    'width': '80%',
                                    'marginLeft': '100px',
                                    'marginRight': '20px',
                                    'display': 'block',
                                    },
                                )
                            ]), html.Div(
                                style={
                                    'display': 'flex',
                                    'padding': '2px',  # Reduce el padding
                                    'backgroundColor': 'white',
                                    'borderRadius': '5px',
                                    'boxShadow': '0px 2px 5px rgba(0, 0, 0, 0)',  # Mejorar la sombra
                                    'height': '50%',
                                    },
                                children=[
                                    html.Div(
                                        style={
                                            'flex': '1',
                                            'display': 'flex',
                                            'flexDirection': 'column',
                                            'alignItems': 'center',
                                            }, children=[
                                                dcc.Dropdown(
                                    id='dropdown-tercer-grafica',
                                    options=[
                                        {'label': 'Opinion Posturas Docentes', 'value': 'posturas_profes'},
                                        {'label': 'Opinion Gral Docentes', 'value': 'gral_profes'},
                                        {'label': 'Confianza en Docentes', 'value': 'confianza_profes'},
                                        ],
                                    value='confianza_profes',  # Valor inicial
                                    style={'width': '70%', 'marginBottom': '10px'},  # Ajustar el tamaño y margen
                                    ),
                                dcc.Graph(
                                    id='tercer-grafica',  # Agrega un ID para la gráfica
                                    figure=confianza_profes,  # Reemplaza con la figura correspondiente
                                    config={'responsive': True},
                                    style={'height': '100%', 'width': '100%'}
                                    )
                                ]), html.Div(
                                    style={
                                        'flex': '1', 
                                        'display': 'flex',
                                        'flexDirection': 'column',
                                        'alignItems': 'center'
                                        }, 
                                    children=[
                                        dcc.Dropdown(
                                            id='dropdown-cuarta-grafica',
                                            options=[
                                                {'label': 'Opinion Posturas Admon', 'value': 'posturas_admon'},
                                                {'label': 'Opinion Gral Admon', 'value': 'gral_admon'},
                                                {'label': 'Confianza en Admon', 'value': 'confianza_admon'},
                                                ],
                                            value='confianza_admon',  # Valor inicial
                                            style={'width': '70%', 'marginBottom': '10px'},  # Ajustar el tamaño y margen
                                            ),
                                        dcc.Graph(
                                            id='cuarta-grafica',  # Agrega un ID para la gráfica
                                            figure=confianza_admon,  # Reemplaza con la figura correspondiente
                                            config={'responsive': True},
                                            style={'height': '100%', 'width': '100%'}
                                        )
                                    ]) 
                                ])
                ])
                                            
                         
                                                    
                
                    
 
            
if __name__ == '__main__':
    app.run_server(debug=True)
