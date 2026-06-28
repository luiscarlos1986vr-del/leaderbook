# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 16:00:03 2026

@author: user1
"""

# -*- coding: utf-8 -*-
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any

def create_radar_chart(averages: Dict[str, float]) -> go.Figure:
    """Crea gráfico de radar con los promedios de los indicadores"""
    
    categories = {
        'analysis_score': 'Análisis',
        'flexibility_score': 'Flexibilidad',
        'delegation_score': 'Delegación',
        'communication_score': 'Comunicación',
        'development_score': 'Desarrollo',
        'serenity_score': 'Serenidad',
        'balance_score': 'Balance'
    }
    
    values = [averages.get(k, 0) for k in categories.keys()]
    labels = list(categories.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name='Tu Perfil Actual',
        line_color='#2563eb',
        fillcolor='rgba(37, 99, 235, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5]
            )
        ),
        title="📊 Resumen de tus indicadores",
        showlegend=False,
        height=450,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig


def create_trend_chart(trends: List[Dict[str, Any]]) -> go.Figure:
    """Crea gráfico de líneas con la evolución de los indicadores"""
    
    if not trends:
        return go.Figure()
    
    df = pd.DataFrame(trends)
    
    indicators = {
        'analysis': 'Análisis',
        'flexibility': 'Flexibilidad',
        'delegation': 'Delegación',
        'communication': 'Comunicación',
        'development': 'Desarrollo',
        'serenity': 'Serenidad',
        'balance': 'Balance'
    }
    
    fig = go.Figure()
    
    # Colores más cálidos y motivadores
    colors = ['#2563eb', '#7c3aed', '#0891b2', '#059669', '#d97706', '#dc2626', '#4f46e5']
    
    for i, (key, label) in enumerate(indicators.items()):
        fig.add_trace(go.Scatter(
            x=df['week'],
            y=df[key],
            name=label,
            mode='lines+markers',
            line=dict(width=2.5, color=colors[i % len(colors)]),
            marker=dict(size=6, color=colors[i % len(colors)]),
            hovertemplate=f'{label}: %{{y:.1f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title="📈 Evolución de tus indicadores",
        xaxis_title="Semana",
        yaxis_title="Puntaje (1-5)",
        yaxis=dict(range=[0.5, 5.5]),
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig


def create_improvement_bars(improvement: Dict[str, float]) -> go.Figure:
    """Crea barras de mejora vs semana anterior"""
    
    labels = {
        'analysis_score': 'Análisis',
        'flexibility_score': 'Flexibilidad',
        'delegation_score': 'Delegación',
        'communication_score': 'Comunicación',
        'development_score': 'Desarrollo',
        'serenity_score': 'Serenidad',
        'balance_score': 'Balance'
    }
    
    keys = list(labels.keys())
    values = [improvement.get(k, 0) for k in keys]
    names = list(labels.values())
    colors = ['#22c55e' if v >= 0 else '#ef4444' for v in values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=names,
        y=values,
        marker_color=colors,
        text=[f"{v:+.1f}" for v in values],
        textposition='outside',
        hovertemplate='%{x}: %{y:+.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="📊 Cambio vs semana anterior",
        yaxis=dict(title="Diferencia", range=[-2, 2]),
        height=300,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


def create_heatmap(trends: List[Dict[str, Any]]) -> go.Figure:
    """Crea un mapa de calor de los indicadores en el tiempo"""
    
    if not trends or len(trends) < 3:
        return go.Figure()
    
    df = pd.DataFrame(trends)
    indicators = ['analysis', 'flexibility', 'delegation', 'communication', 
                  'development', 'serenity', 'balance']
    
    # Tomar últimas 12 semanas máximo
    df = df.tail(12)
    
    data = df[indicators].values.T
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=[f"{r['week']}" for r in df.to_dict('records')],
        y=['Análisis', 'Flexibilidad', 'Delegación', 'Comunicación', 
           'Desarrollo', 'Serenidad', 'Balance'],
        colorscale='RdYlGn',
        zmid=3,
        text=data,
        texttemplate='%{text:.1f}',
        textfont={"size": 10},
        hoverongaps=False,
        hovertemplate='Semana %{x}<br>%{y}: %{z:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="🔥 Evolución visual (últimas semanas)",
        height=350,
        xaxis=dict(title="Semana"),
        yaxis=dict(title="Indicador"),
        margin=dict(l=60, r=20, t=40, b=30)
    )
    
    return fig