import os
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
from pymongo import MongoClient


COLOR_TERRACOTTA = "#743014"    
COLOR_OLIVE = "#9D9167"         
COLOR_PEROLA = "#E8D1A7"       
COLOR_BEGE_ROSE = "#84592B"     
COLOR_VERDE = "#9D9167"        
COLOR_BG_SITE = "#E8D1A7"       
COLOR_DARK = "#442D1C"          

# Connection MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = MongoClient(MONGO_URI)
db = client["allocine_db"]
collection = db["films"]

app = Dash(__name__, 
           external_stylesheets=[
               dbc.themes.BOOTSTRAP,
               "https://fonts.googleapis.com/css2?family=Oswald:wght@200..700&display=swap"
           ],
           meta_tags=[{"name": "referrer", "content": "no-referrer"}])

# clean DATA

def get_clean_data():
    cursor = collection.find().limit(500)
    df = pd.DataFrame(list(cursor))
    
    fig_note = px.bar(title="En attente de données...")
    fig_genre = px.bar(title="En attente de données...")

    if df.empty:
        empty_df = pd.DataFrame(columns=["titre", "genre_str", "duree", "note_spectateurs", "date_sortie", "url", "affiche_url"])
        return empty_df, fig_note, fig_genre

    if '_id' in df.columns: 
        df.drop(columns=['_id'], inplace=True)

    df['Note_Num'] = pd.to_numeric(df['note_spectateurs'].astype(str).str.replace(',', '.'), errors='coerce')

    note_counts = df['note_spectateurs'].value_counts().reset_index()
    note_counts.columns = ['Note', 'Nombre de films']
    note_counts = note_counts.sort_values(by='Note')
    fig_note = px.bar(note_counts, x='Note', y='Nombre de films', 
                      template="plotly_white",
                      color_discrete_sequence=[COLOR_OLIVE])
    fig_note.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Oswald")

    if 'genre' in df.columns:
        df_exploded = df.explode('genre')
        genre_counts = df_exploded['genre'].value_counts().reset_index().head(10)
        genre_counts.columns = ['Genre', 'Nombre de films']
        fig_genre = px.bar(genre_counts, x='Genre', y='Nombre de films', 
                           template="plotly_white",
                           color_discrete_sequence=[COLOR_TERRACOTTA])
        fig_genre.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Oswald")
        
        df['genre_str'] = df['genre'].apply(lambda x: ", ".join(x) if isinstance(x, list) else str(x))
        df.drop(columns=['genre'], inplace=True)
    else:
        df['genre_str'] = "N/A"

    return df, fig_note, fig_genre

def make_card(film):
    img_src = film.get('affiche_url')
    if not img_src or str(img_src).startswith('data:image') or "empty.gif" in str(img_src):
        img_src = "https://ac-p.oneline.me/img/no-poster.png"
    
    return dbc.Col(
        dbc.Card([
            dbc.CardImg(src=img_src, top=True, style={
                    "aspect-ratio": "2 / 3", 
                    "object-fit": "cover",
                    "width": "100%"
                }),
            dbc.CardBody([
                html.H6(film.get('titre', 'N/A'), className="card-title text-truncate", 
                        style={"color": COLOR_TERRACOTTA, "fontFamily": "Oswald", "fontWeight": "600"}),
                html.P(f"⭐ {film.get('note_spectateurs', 'N/A')}", 
                       style={"color": COLOR_VERDE, "fontWeight": "700", "fontFamily": "Oswald"}),
                dbc.Button("Lien", href=film.get('url', '#'), target="_blank", 
                           style={"backgroundColor": COLOR_DARK, "border": "none", "fontFamily": "Oswald", "width": "100%", "fontSize": "0.8rem"})
            ], style={"padding": "12px"}),
        ], className="mb-4 shadow-sm border-0 h-100", style={
            "backgroundColor": "white", 
            "borderRadius": "12px",
            "overflow": "hidden"
        }),
        xs=6, sm=4, md=3, lg=2,
        className="px-2 pb-2"
    )

#Chargement DATA
df_init, fig_note, fig_genre = get_clean_data()
avg_note = df_init['Note_Num'].mean() if not df_init.empty else 0

#AFFICHAGE
app.layout = dbc.Container([
    html.Iframe(style={'display': 'none'}, srcDoc=f"""
        <style>
            .dash-spreadsheet tr:hover td {{
                background-color: {COLOR_PEROLA} !important;
                color: {COLOR_DARK} !important;
                cursor: pointer !important;
            }}
        </style>
    """),

    # TITRE PRINCIPAL
    dbc.Row([
        dbc.Col([
            html.H1("ALLOCINÉ DATA EXPLORER", 
                    className="text-center mt-5 mb-5", 
                    style={'fontFamily': 'Oswald', 'fontWeight': '700', 'color': COLOR_TERRACOTTA, 'letterSpacing': '5px'}),
        ], width=12)
    ]),

    # SECTION STATS
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("FILMS EN BASE", style={"color": COLOR_DARK, "fontFamily": "Oswald", "fontSize": "0.9rem", "marginBottom": "5px"}),
                html.H2(f"{len(df_init)}", style={"color": COLOR_TERRACOTTA, "fontWeight": "700", "marginBottom": "0"})
            ])
        ], className="text-center border-0 shadow-sm", style={"backgroundColor": "white", "borderRadius": "10px"}), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("NOTE MOYENNE", style={"color": COLOR_DARK, "fontFamily": "Oswald", "fontSize": "0.9rem", "marginBottom": "5px"}),
                html.H2(f"{avg_note:.1f} / 5", style={"color": COLOR_VERDE, "fontWeight": "700", "marginBottom": "0"})
            ])
        ], className="text-center border-0 shadow-sm", style={"backgroundColor": "white", "borderRadius": "10px"}), width=3),

    ], className="mb-5 justify-content-center g-4"),

    # Graphiques
    dbc.Row([
        dbc.Col([
            html.H4("TOP GENRES", className="text-center mb-3", style={"fontFamily": "Oswald", "color": COLOR_DARK}),
            dcc.Graph(figure=fig_genre, config={'displayModeBar': False})
        ], width=6),
        dbc.Col([
            html.H4("RÉPARTITION DES NOTES", className="text-center mb-3", style={"fontFamily": "Oswald", "color": COLOR_DARK}),
            dcc.Graph(figure=fig_note, config={'displayModeBar': False})
        ], width=6),
    ], className="mb-5"),

    # Galerie
    html.H3("SÉLECTION SYNCHRONISÉE", className="mb-4", 
            style={'fontFamily': 'Oswald', 'color': COLOR_TERRACOTTA, 'borderLeft': f'8px solid {COLOR_TERRACOTTA}', 'paddingLeft': '15px'}),
    dbc.Row(id='dynamic-gallery', className="mb-5 px-3"),

    # Tableau
    html.H3("BASE DE DONNÉES COMPLÈTE", className="mb-4", 
            style={'fontFamily': 'Oswald', 'color': COLOR_TERRACOTTA, 'borderLeft': f'8px solid {COLOR_OLIVE}', 'paddingLeft': '15px'}),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i.replace("_str", "").upper(), "id": i} for i in ["titre", "genre_str", "duree", "note_spectateurs", "date_sortie"]],
                data=df_init.to_dict('records'),
                sort_action="native",
                filter_action="native",
                page_action="native",
                page_current=0,
                page_size=12,
                
                style_table={
                    'borderRadius': '15px',
                    'overflow': 'hidden',
                    'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'
                },
                
                style_cell={
                    'backgroundColor': 'white',
                    'color': COLOR_DARK,
                    'padding': '12px 15px',
                    'fontFamily': 'Oswald',
                    'fontSize': '14px',
                    'borderBottom': f'1px solid {COLOR_PEROLA}',
                    'textAlign': 'left'
                },
                
                style_header={
                    'backgroundColor': COLOR_OLIVE,
                    'color': 'white',
                    'fontWeight': 'bold',
                    'textTransform': 'uppercase',
                    'border': 'none'
                },
                
                style_data_conditional=[
                    {
                        'if': {'state': 'active'},
                        'backgroundColor': COLOR_TERRACOTTA,
                        'color': 'white'
                    },
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': "#F9F4EB",
                    }
                ],
                
                style_filter={
                    'backgroundColor': 'white',
                    'color': COLOR_DARK,
                    'fontFamily': 'Oswald'
                }
            )
        ], width=12)
    ], className="pb-5")
], fluid=True, style={'backgroundColor': COLOR_BG_SITE, 'minHeight': '100vh', 'fontFamily': 'Oswald'})


@app.callback(
    Output('dynamic-gallery', 'children'),
    [Input('table', 'derived_virtual_data'),
     Input('table', 'page_current'),
     Input('table', 'page_size')]
)
def update_gallery(rows, page_current, page_size):
    if rows is None:
        return []
    
    page_current = page_current if page_current else 0
    start = page_current * page_size
    end = (page_current + 1) * page_size
    
    paged_rows = rows[start:end]
    return [make_card(row) for row in paged_rows]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)