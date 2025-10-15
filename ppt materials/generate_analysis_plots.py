"""
Comprehensive Placement Data Analysis
======================================
This script generates beautiful visualizations for placement data analysis
using Plotly for interactive and professional-looking plots.

Author: Data Analysis Team
Date: October 2025
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set consistent color palette
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9800',
    'info': '#17a2b8',
    'dark': '#343a40',
    'light': '#f8f9fa',
    'placed': '#2ecc71',
    'unplaced': '#e74c3c',
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

# Department full names mapping
DEPT_NAMES = {
    'AE': 'Aerospace Engineering',
    'AG': 'Agricultural Engineering',
    'BT': 'Biotechnology',
    'CE': 'Civil Engineering',
    'CH': 'Chemical Engineering',
    'CS': 'Computer Science',
    'EC': 'Electronics & Communication',
    'EE': 'Electrical Engineering',
    'IE': 'Instrumentation Engineering',
    'IM': 'Industrial Management',
    'ME': 'Mechanical Engineering',
    'MF': 'Manufacturing Engineering',
    'MI': 'Mining Engineering',
    'MT': 'Metallurgical Engineering',
    'NA': 'Naval Architecture',
    'CY': 'Chemistry',
    'EX': 'Exploration Geophysics',
    'GG': 'Geology & Geophysics',
    'HS': 'Humanities & Social Sciences',
    'MA': 'Mathematics',
    'PH': 'Physics'
}

def load_data():
    """Load and preprocess all required data files"""
    print("Loading data files...")
    
    # Load student data
    students = pd.read_csv('analysis_data.csv')
    
    # Load outcomes
    outcomes = pd.read_csv('outcomes_4_year.csv')
    
    # Load companies
    companies = pd.read_csv('companies.csv')
    
    # Extract department from roll number (e.g., 23CS10001 -> CS)
    students['department'] = students['roll_no'].str.extract(r'23([A-Z]{2})\d+')
    
    # Merge with outcomes
    students = students.merge(outcomes, on='roll_no', how='left')
    students['placed'] = students['received_offer'].fillna(False)
    students['placed'] = students['placed'].replace({'TRUE': True, 'True': True, True: True})
    
    # Map department codes to full names
    students['dept_name'] = students['department'].map(DEPT_NAMES).fillna(students['department'])
    
    print(f"Loaded {len(students)} students from {students['department'].nunique()} departments")
    print(f"Placement rate: {students['placed'].mean()*100:.2f}%")
    
    return students, companies

def plot_1_departmental_performance(students):
    """
    Plot 1: Departmental Hit Rate Analysis
    Grouped bar chart showing total students vs placed students by department
    """
    print("\nGenerating Plot 1: Departmental Performance...")
    
    # Calculate metrics by department
    dept_stats = students.groupby('dept_name').agg({
        'roll_no': 'count',
        'placed': 'sum'
    }).reset_index()
    dept_stats.columns = ['Department', 'Total Students', 'Placed Students']
    dept_stats['Placement Rate (%)'] = (dept_stats['Placed Students'] / dept_stats['Total Students'] * 100).round(2)
    dept_stats = dept_stats.sort_values('Placement Rate (%)', ascending=False)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Total Students',
        x=dept_stats['Department'],
        y=dept_stats['Total Students'],
        marker_color=COLORS['info'],
        text=dept_stats['Total Students'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Total Students: %{y}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Placed Students',
        x=dept_stats['Department'],
        y=dept_stats['Placed Students'],
        marker_color=COLORS['success'],
        text=dept_stats['Placed Students'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Placed: %{y}<br>Rate: %{customdata}%<extra></extra>',
        customdata=dept_stats['Placement Rate (%)']
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Departmental Performance: The Placement Landscape</b><br><sub>Total Students vs Placed Students by Department</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        xaxis_title='<b>Department</b>',
        yaxis_title='<b>Number of Students</b>',
        barmode='group',
        bargap=0.2,
        bargroupgap=0.1,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color=COLORS['dark']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14)
        ),
        height=600,
        width=1400
    )
    
    fig.update_xaxes(showgrid=False, tickangle=-45)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    fig.write_html('analysis_plots/plot_1_departmental_performance.html')
    fig.write_image('analysis_plots/plot_1_departmental_performance.png', width=1400, height=600)
    print("✓ Saved: plot_1_departmental_performance")
    
    return dept_stats

def plot_2_cgpa_distribution(students):
    """
    Plot 2: CGPA Distribution Analysis
    Shows overall CGPA distribution and identifies high performers by department
    """
    print("\nGenerating Plot 2: CGPA Distribution Analysis...")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '<b>Overall CGPA Distribution</b>',
            '<b>CGPA Distribution by Department (Top 10)</b>',
            '<b>Students with CGPA ≥ 9.0 by Department</b>',
            '<b>Average CGPA by Department</b>'
        ),
        specs=[[{'type': 'histogram'}, {'type': 'box'}],
               [{'type': 'bar'}, {'type': 'bar'}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # 1. Overall CGPA distribution
    fig.add_trace(
        go.Histogram(
            x=students['cgpa'],
            nbinsx=40,
            marker_color=COLORS['gradient_start'],
            opacity=0.7,
            name='CGPA Distribution',
            hovertemplate='CGPA: %{x:.2f}<br>Count: %{y}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # 2. Top 10 departments - Box plot
    top_depts = students.groupby('dept_name')['roll_no'].count().nlargest(10).index
    dept_data = students[students['dept_name'].isin(top_depts)]
    
    for dept in top_depts:
        dept_cgpa = dept_data[dept_data['dept_name'] == dept]['cgpa']
        fig.add_trace(
            go.Box(
                y=dept_cgpa,
                name=dept,
                boxmean='sd',
                showlegend=False,
                marker_color=px.colors.qualitative.Set3[list(top_depts).index(dept) % len(px.colors.qualitative.Set3)]
            ),
            row=1, col=2
        )
    
    # 3. Students with CGPA >= 9.0
    high_performers = students[students['cgpa'] >= 9.0].groupby('dept_name').size().sort_values(ascending=False).head(15)
    
    fig.add_trace(
        go.Bar(
            x=high_performers.index,
            y=high_performers.values,
            marker_color=COLORS['success'],
            text=high_performers.values,
            textposition='outside',
            name='Students with CGPA ≥ 9.0',
            showlegend=False,
            hovertemplate='<b>%{x}</b><br>Students: %{y}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 4. Average CGPA by department
    avg_cgpa = students.groupby('dept_name')['cgpa'].mean().sort_values(ascending=False).head(15)
    
    fig.add_trace(
        go.Bar(
            x=avg_cgpa.index,
            y=avg_cgpa.values,
            marker_color=COLORS['primary'],
            text=[f'{x:.2f}' for x in avg_cgpa.values],
            textposition='outside',
            name='Average CGPA',
            showlegend=False,
            hovertemplate='<b>%{x}</b><br>Avg CGPA: %{y:.2f}<extra></extra>'
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': '<b>CGPA Distribution Analysis: Academic Excellence Across Departments</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=11, color=COLORS['dark']),
        height=900,
        width=1600
    )
    
    # Update axes
    fig.update_xaxes(showgrid=False, row=2, col=1, tickangle=-45)
    fig.update_xaxes(showgrid=False, row=2, col=2, tickangle=-45)
    fig.update_xaxes(title_text='<b>CGPA</b>', row=1, col=1)
    fig.update_xaxes(title_text='<b>Department</b>', row=1, col=2)
    fig.update_yaxes(title_text='<b>Frequency</b>', row=1, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text='<b>CGPA</b>', row=1, col=2, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text='<b>Number of Students</b>', row=2, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text='<b>Average CGPA</b>', row=2, col=2, showgrid=True, gridcolor='lightgray')
    
    fig.write_html('analysis_plots/plot_2_cgpa_distribution.html')
    fig.write_image('analysis_plots/plot_2_cgpa_distribution.png', width=1600, height=900)
    print("✓ Saved: plot_2_cgpa_distribution")
    
    # Return statistics for analysis
    cgpa_stats = {
        'mean': students['cgpa'].mean(),
        'median': students['cgpa'].median(),
        'std': students['cgpa'].std(),
        'min': students['cgpa'].min(),
        'max': students['cgpa'].max(),
        'high_performers': high_performers.to_dict()
    }
    
    return cgpa_stats

def plot_3_department_domain_heatmap(students):
    """
    Plot 3: Department × Domain Heatmap
    Shows the distribution of domain preferences across departments
    """
    print("\nGenerating Plot 3: Department × Domain Heatmap...")
    
    # Create domain matrix
    # Combine domain_1 and domain_2
    domain_data = []
    for _, row in students.iterrows():
        if pd.notna(row['domain_1']):
            domain_data.append({'dept_name': row['dept_name'], 'domain': row['domain_1']})
        if pd.notna(row['domain_2']):
            domain_data.append({'dept_name': row['dept_name'], 'domain': row['domain_2']})
    
    domain_df = pd.DataFrame(domain_data)
    
    # Create pivot table
    heatmap_data = pd.crosstab(domain_df['dept_name'], domain_df['domain'])
    
    # Sort by total count
    heatmap_data = heatmap_data.loc[heatmap_data.sum(axis=1).sort_values(ascending=False).index]
    heatmap_data = heatmap_data[heatmap_data.sum(axis=0).sort_values(ascending=False).index]
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis',
        text=heatmap_data.values,
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="<b>Student<br>Count</b>"),
        hovertemplate='<b>Department:</b> %{y}<br><b>Domain:</b> %{x}<br><b>Students:</b> %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Department × Domain Matrix: Career Preference Landscape</b><br><sub>Distribution of domain choices across academic departments</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        xaxis_title='<b>Domain / Job Profile</b>',
        yaxis_title='<b>Department</b>',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color=COLORS['dark']),
        height=800,
        width=1400
    )
    
    fig.update_xaxes(tickangle=-45, showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    fig.write_html('analysis_plots/plot_3_department_domain_heatmap.html')
    fig.write_image('analysis_plots/plot_3_department_domain_heatmap.png', width=1400, height=800)
    print("✓ Saved: plot_3_department_domain_heatmap")
    
    return heatmap_data

def plot_4_companies_per_day(companies):
    """
    Plot 4: Companies Arriving Per Day
    Bar graph showing number of companies on each placement day
    """
    print("\nGenerating Plot 4: Companies Per Day...")
    
    # Count companies per day
    companies_per_day = companies.groupby('arrival_day').size().reset_index(name='count')
    companies_per_day = companies_per_day.sort_values('arrival_day')
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[f'Day {day}' for day in companies_per_day['arrival_day']],
        y=companies_per_day['count'],
        marker_color=COLORS['gradient_start'],
        marker_line_color=COLORS['gradient_end'],
        marker_line_width=2,
        text=companies_per_day['count'],
        textposition='outside',
        hovertemplate='<b>Day %{x}</b><br>Companies: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Placement Timeline: Company Arrivals by Day</b><br><sub>Distribution of recruitment activity across placement season</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        xaxis_title='<b>Placement Day</b>',
        yaxis_title='<b>Number of Companies</b>',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=14, color=COLORS['dark']),
        height=600,
        width=1200,
        showlegend=False
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    # Add trend line
    fig.add_trace(go.Scatter(
        x=[f'Day {day}' for day in companies_per_day['arrival_day']],
        y=companies_per_day['count'],
        mode='lines',
        line=dict(color=COLORS['danger'], width=2, dash='dash'),
        name='Trend',
        hovertemplate='<extra></extra>'
    ))
    
    fig.write_html('analysis_plots/plot_4_companies_per_day.html')
    fig.write_image('analysis_plots/plot_4_companies_per_day.png', width=1200, height=600)
    print("✓ Saved: plot_4_companies_per_day")
    
    return companies_per_day

def plot_5_kpi_cards(students):
    """
    Plot 5: KPI Dashboard Cards
    Key Performance Indicators - Total Placed, Placement Rate
    """
    print("\nGenerating Plot 5: KPI Dashboard...")
    
    total_students = len(students)
    total_placed = students['placed'].sum()
    placement_rate = (total_placed / total_students * 100)
    
    # Create KPI cards using plotly
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('', '', ''),
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
        horizontal_spacing=0.1
    )
    
    # Total Students
    fig.add_trace(go.Indicator(
        mode="number",
        value=total_students,
        title={'text': "<b>Total Students</b><br><span style='font-size:0.8em;color:gray'>Participating in Placement</span>"},
        number={'font': {'size': 60, 'color': COLORS['primary']}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=1)
    
    # Total Placed
    fig.add_trace(go.Indicator(
        mode="number",
        value=total_placed,
        title={'text': "<b>Students Placed</b><br><span style='font-size:0.8em;color:gray'>Received Job Offers</span>"},
        number={'font': {'size': 60, 'color': COLORS['success']}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=2)
    
    # Placement Rate
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=placement_rate,
        title={'text': "<b>Placement Rate</b><br><span style='font-size:0.8em;color:gray'>Success Percentage</span>"},
        number={'suffix': "%", 'font': {'size': 60, 'color': COLORS['warning']}},
        delta={'reference': 75, 'relative': False, 'suffix': '% vs Target'},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=3)
    
    fig.update_layout(
        title={
            'text': '<b>Placement Season 2023-24: Key Performance Indicators</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': COLORS['dark']}
        },
        paper_bgcolor='#f8f9fa',
        plot_bgcolor='white',
        height=400,
        width=1400,
        font=dict(family="Arial, sans-serif", size=14)
    )
    
    fig.write_html('analysis_plots/plot_5_kpi_cards.html')
    fig.write_image('analysis_plots/plot_5_kpi_cards.png', width=1400, height=400)
    print("✓ Saved: plot_5_kpi_cards")
    
    return {'total_students': total_students, 'total_placed': total_placed, 'placement_rate': placement_rate}

def plot_6_placement_comparison(students):
    """
    Plot 6: Horizontal Bar Chart - Placement Rate by Department
            Grouped Bar Chart - Placed vs Unplaced by Department
    """
    print("\nGenerating Plot 6: Placement Comparison Charts...")
    
    # Calculate department statistics
    dept_stats = students.groupby('dept_name').agg({
        'roll_no': 'count',
        'placed': ['sum', lambda x: (1-x).sum()]
    }).reset_index()
    dept_stats.columns = ['Department', 'Total', 'Placed', 'Unplaced']
    dept_stats['Placement Rate (%)'] = (dept_stats['Placed'] / dept_stats['Total'] * 100).round(2)
    dept_stats = dept_stats.sort_values('Placement Rate (%)', ascending=True)
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            '<b>Placement Rate by Department (%)</b>',
            '<b>Placed vs Unplaced Students</b>'
        ),
        horizontal_spacing=0.15,
        specs=[[{'type': 'bar'}, {'type': 'bar'}]]
    )
    
    # 1. Horizontal bar chart - Placement Rate
    colors = [COLORS['success'] if x >= 75 else COLORS['warning'] if x >= 50 else COLORS['danger'] 
              for x in dept_stats['Placement Rate (%)']]
    
    fig.add_trace(
        go.Bar(
            y=dept_stats['Department'],
            x=dept_stats['Placement Rate (%)'],
            orientation='h',
            marker_color=colors,
            text=[f"{x:.1f}%" for x in dept_stats['Placement Rate (%)']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Placement Rate: %{x:.2f}%<extra></extra>',
            showlegend=False
        ),
        row=1, col=1
    )
    
    # 2. Grouped bar chart - Placed vs Unplaced
    dept_stats_sorted = dept_stats.sort_values('Total', ascending=False).head(15)
    
    fig.add_trace(
        go.Bar(
            name='Placed',
            x=dept_stats_sorted['Department'],
            y=dept_stats_sorted['Placed'],
            marker_color=COLORS['placed'],
            text=dept_stats_sorted['Placed'],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Placed: %{y}<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(
            name='Unplaced',
            x=dept_stats_sorted['Department'],
            y=dept_stats_sorted['Unplaced'],
            marker_color=COLORS['unplaced'],
            text=dept_stats_sorted['Unplaced'],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Unplaced: %{y}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': '<b>Departmental Placement Analysis: Success Rates and Distribution</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=11, color=COLORS['dark']),
        height=800,
        width=1600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.75,
            font=dict(size=12)
        )
    )
    
    # Update axes
    fig.update_xaxes(title_text='<b>Placement Rate (%)</b>', row=1, col=1, showgrid=True, gridcolor='lightgray')
    fig.update_xaxes(title_text='<b>Department</b>', row=1, col=2, showgrid=False, tickangle=-45)
    fig.update_yaxes(title_text='<b>Department</b>', row=1, col=1, showgrid=False)
    fig.update_yaxes(title_text='<b>Number of Students</b>', row=1, col=2, showgrid=True, gridcolor='lightgray')
    
    fig.write_html('analysis_plots/plot_6_placement_comparison.html')
    fig.write_image('analysis_plots/plot_6_placement_comparison.png', width=1600, height=800)
    print("✓ Saved: plot_6_placement_comparison")
    
    return dept_stats

def plot_7_cgpa_boxplot(students):
    """
    Plot 7: Boxplot - CGPA Distribution Across All Departments
    """
    print("\nGenerating Plot 7: CGPA Boxplot Comparison...")
    
    # Sort departments by median CGPA
    dept_median = students.groupby('dept_name')['cgpa'].median().sort_values(ascending=False)
    
    # Create box plot
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set3
    
    for i, dept in enumerate(dept_median.index):
        dept_data = students[students['dept_name'] == dept]['cgpa']
        
        fig.add_trace(go.Box(
            y=dept_data,
            name=dept,
            marker_color=colors[i % len(colors)],
            boxmean='sd',
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Max: %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': '<b>CGPA Distribution Across Departments: Comparative Analysis</b><br><sub>Box plots showing median, quartiles, and outliers</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        xaxis_title='<b>Department</b>',
        yaxis_title='<b>CGPA</b>',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color=COLORS['dark']),
        height=700,
        width=1600,
        showlegend=False,
        hovermode='closest'
    )
    
    fig.update_xaxes(showgrid=False, tickangle=-45)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', range=[5, 10])
    
    fig.write_html('analysis_plots/plot_7_cgpa_boxplot.html')
    fig.write_image('analysis_plots/plot_7_cgpa_boxplot.png', width=1600, height=700)
    print("✓ Saved: plot_7_cgpa_boxplot")
    
    return dept_median

def main():
    """Main execution function"""
    print("="*70)
    print("  PLACEMENT DATA ANALYSIS - VISUALIZATION GENERATOR")
    print("="*70)
    
    # Load data
    students, companies = load_data()
    
    # Generate all plots
    print("\n" + "="*70)
    print("  GENERATING VISUALIZATIONS")
    print("="*70)
    
    dept_stats = plot_1_departmental_performance(students)
    cgpa_stats = plot_2_cgpa_distribution(students)
    domain_matrix = plot_3_department_domain_heatmap(students)
    companies_per_day = plot_4_companies_per_day(companies)
    kpi_data = plot_5_kpi_cards(students)
    placement_comparison = plot_6_placement_comparison(students)
    cgpa_boxplot = plot_7_cgpa_boxplot(students)
    
    print("\n" + "="*70)
    print("  ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
    print("="*70)
    print(f"\n✓ All plots saved to: analysis_plots/")
    print(f"✓ Total Students Analyzed: {len(students)}")
    print(f"✓ Placement Rate: {kpi_data['placement_rate']:.2f}%")
    print(f"✓ Departments Covered: {students['department'].nunique()}")
    print(f"✓ Companies Analyzed: {len(companies)}")
    
    return {
        'dept_stats': dept_stats,
        'cgpa_stats': cgpa_stats,
        'domain_matrix': domain_matrix,
        'companies_per_day': companies_per_day,
        'kpi_data': kpi_data,
        'placement_comparison': placement_comparison
    }

if __name__ == "__main__":
    results = main()
