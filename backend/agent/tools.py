import sys
import subprocess
import json
import base64
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.io as pio
from langchain_core.tools import tool

# Global variable to hold the current CSV path for tool access
_csv_path = None

def set_csv_path(path: str):
    global _csv_path
    _csv_path = path

@tool
def run_python(code: str) -> str:
    """
    Executes a snippet of Python code in a sandboxed subprocess.
    The pandas library is pre-imported as `pd` and the dataset is available as `df`.
    Prints the output or any error traceback.
    Use this to explore the dataset (e.g., df.head(), df.info(), df.describe()).
    """
    if not _csv_path:
        return "Error: Dataset path is not set."

    script_content = f"""
import pandas as pd
import numpy as np
import sys
import traceback
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    df = pd.read_csv('{_csv_path}')
{chr(10).join(['    ' + line for line in code.split(chr(10))])}
except Exception as e:
    traceback.print_exc()
"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", script_content],
            capture_output=True,
            text=True,
            timeout=15
        )
        output = result.stdout
        if result.stderr:
            output += "\nErrors:\n" + result.stderr
        return output if output else "Execution completed with no output."
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 15 seconds."
    except Exception as e:
        return f"Error executing code: {str(e)}"

@tool
def generate_chart(chart_type: str, x_col: str, y_col: str, title: str) -> str:
    """
    Generates a chart and returns it as a base64 encoded image string.
    Supported chart types: 'bar', 'line', 'scatter', 'histogram', 'box'.
    For 'histogram' and 'box', only 'x_col' is required, 'y_col' can be empty.
    """
    if not _csv_path:
        return "Error: Dataset path is not set."
    
    try:
        df = pd.read_csv(_csv_path)
        colors = ['#22c55e', '#06b6d4', '#8b5cf6', '#f43f5e', '#f59e0b', '#3b82f6']
        
        if chart_type == 'bar':
            fig = px.bar(df, x=x_col, y=y_col, title=title, template='plotly_dark', color_discrete_sequence=colors)
            fig.update_traces(marker_line_width=0, opacity=0.85)
        elif chart_type == 'line':
            fig = px.line(df, x=x_col, y=y_col, title=title, template='plotly_dark', color_discrete_sequence=colors)
            fig.update_traces(line=dict(width=3, shape='spline'), marker=dict(size=6, symbol='circle'))
        elif chart_type == 'scatter':
            fig = px.scatter(df, x=x_col, y=y_col, title=title, template='plotly_dark', color_discrete_sequence=colors)
            fig.update_traces(marker=dict(size=8, opacity=0.75, line=dict(width=1, color='rgba(255,255,255,0.2)')))
        elif chart_type == 'histogram':
            fig = px.histogram(df, x=x_col, title=title, template='plotly_dark', color_discrete_sequence=colors)
            fig.update_traces(marker=dict(line=dict(width=1, color='#111111')), opacity=0.85)
        elif chart_type == 'box':
            fig = px.box(df, x=x_col, y=y_col, title=title, template='plotly_dark', color_discrete_sequence=colors)
            fig.update_traces(marker=dict(size=4), line=dict(width=1.5))
        else:
            return f"Error: Unsupported chart type '{chart_type}'."
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="JetBrains Mono, Courier New, monospace",
                size=11,
                color='#e5e5e5'
            ),
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                font=dict(
                    size=15,
                    color='#22c55e',
                    family="JetBrains Mono, Courier New, monospace"
                )
            ),
            margin=dict(l=55, r=40, t=65, b=50),
            hoverlabel=dict(
                bgcolor='#151515',
                bordercolor='#333333',
                font=dict(
                    color='#e5e5e5',
                    family="JetBrains Mono, Courier New, monospace",
                    size=11
                )
            ),
            legend=dict(
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(0,0,0,0)',
                font=dict(color='#a3a3a3')
            )
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridcolor='#222222',
            zerolinecolor='#333333',
            tickfont=dict(color='#a3a3a3'),
            title_font=dict(color='#e5e5e5'),
            linecolor='#333333'
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor='#222222',
            zerolinecolor='#333333',
            tickfont=dict(color='#a3a3a3'),
            title_font=dict(color='#e5e5e5'),
            linecolor='#333333'
        )
        
        img_bytes = pio.to_image(fig, format='png', engine='kaleido')
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
        html_div = fig.to_html(full_html=False, include_plotlyjs=False)
        return f"SUCCESS:{base64_str}|||{title}|||{html_div}"
    except Exception as e:
        return f"Error generating chart: {str(e)}"

@tool
def compute_stats(column: str) -> str:
    """
    Computes statistical metrics (mean, median, std, min, max, 25th, 75th percentiles, skewness, kurtosis) 
    for a specified numeric column.
    """
    if not _csv_path:
        return "Error: Dataset path is not set."
    
    try:
        df = pd.read_csv(_csv_path)
        if column not in df.columns:
            return f"Error: Column '{column}' not found in dataset."
            
        col_data = pd.to_numeric(df[column], errors='coerce').dropna()
        if len(col_data) == 0:
            return f"Error: Column '{column}' does not contain numeric data or is empty."
            
        stats_dict = {
            "count": len(col_data),
            "mean": float(np.mean(col_data)),
            "median": float(np.median(col_data)),
            "std": float(np.std(col_data)),
            "min": float(np.min(col_data)),
            "max": float(np.max(col_data)),
            "25%": float(np.percentile(col_data, 25)),
            "75%": float(np.percentile(col_data, 75)),
            "skewness": float(stats.skew(col_data)),
            "kurtosis": float(stats.kurtosis(col_data))
        }
        return json.dumps(stats_dict, indent=2)
    except Exception as e:
        return f"Error computing stats: {str(e)}"
