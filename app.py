#Import libraries
import pandas as pd
import datetime as dt 
import numpy as np 
import seaborn as sb 
import scipy as sp 
import unicodedata
import matplotlib.pyplot as plt
import plotly as px
import plotly.graph_objects as go
import nbformat
import re
import dash
import psycopg2
from dash import dcc, html
from dash.dependencies import Input, Output, State
app = dash.Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'
])

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
