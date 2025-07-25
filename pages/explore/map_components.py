"""
Map components and utilities for the explore page.
"""

import pandas as pd
import plotly.express as px
from utils.data_processing import load_countries_data

# Load the data
df = load_countries_data()

def create_map(sort_order='none', selected_country=None):
    """Create choropleth map with optional GDP sorting and country highlighting."""
    df_sorted = df.copy()
    
    # Filter out countries with zero or no GDP data for better ranking
    df_with_gdp = df_sorted[df_sorted['gdp_numeric'] > 0].copy()
    df_no_gdp = df_sorted[df_sorted['gdp_numeric'] <= 0].copy()
    
    if sort_order == 'ascending':
        # For Low to High: Use actual GDP values (so low GDP = dark, high GDP = bright)
        df_with_gdp = df_with_gdp.sort_values('gdp_numeric', ascending=True)
        # Use actual GDP values for coloring
        df_with_gdp['display_value'] = df_with_gdp['gdp_numeric']
        df_with_gdp['gdp_rank'] = range(1, len(df_with_gdp) + 1)
        # Countries with no GDP get value 0
        df_no_gdp['display_value'] = 0
        df_no_gdp['gdp_rank'] = 0
        # Combine dataframes
        df_sorted = pd.concat([df_no_gdp, df_with_gdp], ignore_index=True)
        color_col = 'display_value'
        color_scale = px.colors.sequential.Reds
        
    elif sort_order == 'descending':
        # For High to Low: Use actual GDP values (same as ascending for consistency)
        df_with_gdp = df_with_gdp.sort_values('gdp_numeric', ascending=False)
        # Use actual GDP values for coloring (same as ascending for consistency)
        df_with_gdp['display_value'] = df_with_gdp['gdp_numeric']
        df_with_gdp['gdp_rank'] = range(1, len(df_with_gdp) + 1)
        # Countries with no GDP get value 0
        df_no_gdp['display_value'] = 0
        df_no_gdp['gdp_rank'] = 0
        # Combine dataframes
        df_sorted = pd.concat([df_no_gdp, df_with_gdp], ignore_index=True)
        color_col = 'display_value'
        color_scale = px.colors.sequential.Blues
        
    else:
        # No sorting - use original GDP values
        df_sorted['gdp_rank'] = 0
        color_col = 'gdp_numeric'
        color_scale = px.colors.sequential.Cividis
    
    # Create custom hover data
    hover_data_dict = {
        "capital": True,
        "currency": True,
        "gdp": True,
        "country_iso_alpha": True
    }
    
    # Display gdp rank if sorted
    if sort_order != 'none':
        hover_data_dict["gdp_rank"] = True
        hover_data_dict["display_value"] = False
    else:
        # Explicitly exclude gdp_numeric from hover when not sorted
        hover_data_dict["gdp_numeric"] = False
    
    fig = px.choropleth(
        df_sorted,
        locations="country_iso_alpha",
        color=color_col,
        hover_name="country",
        hover_data=hover_data_dict,
        color_continuous_scale=color_scale
    )
    # Align the title to the center
    fig.update_layout(title_x=0.5)
    
    # Update color bar title and range
    if sort_order == 'ascending':
        # For Low to High: Using actual GDP values
        fig.update_coloraxes(colorbar_title="GDP in Billions")
        min_val = df_sorted[df_sorted['display_value'] > 0]['display_value'].min()
        max_val = df_sorted['display_value'].max()
        fig.update_coloraxes(cmin=min_val, cmax=max_val)
        fig.update_traces(zmin=min_val, zmax=max_val)
    elif sort_order == 'descending':
        # For High to Low: Using actual GDP values (same as ascending for consistency)
        fig.update_coloraxes(colorbar_title="GDP in Billions")
        min_val = df_sorted[df_sorted['display_value'] > 0]['display_value'].min()
        max_val = df_sorted['display_value'].max()
        fig.update_coloraxes(cmin=min_val, cmax=max_val)
        fig.update_traces(zmin=min_val, zmax=max_val)
    else:
        fig.update_coloraxes(colorbar_title="GDP in Billions")
        # For non-sorted view, ensure proper range for GDP values
        min_gdp = df_sorted['gdp_numeric'].min()
        max_gdp = df_sorted['gdp_numeric'].max()
        fig.update_coloraxes(cmin=min_gdp, cmax=max_gdp)
    
    # Add highlighting for selected country
    if selected_country:
        # Find the country from the sorted dataframe to ensure it has all necessary columns
        country_row = df_sorted[df_sorted['country'] == selected_country]
        if not country_row.empty:
            iso_code = country_row.iloc[0]['country_iso_alpha']
            # Choose color based on sort order
            if sort_order == 'ascending':
                highlight_color = '#22AA22'  # Green for low to high
            elif sort_order == 'descending':
                highlight_color = '#4444FF'  # Blue for high to low
            else:
                highlight_color = '#FF4444'  # Red for no sorting (default)
            
            # Add a highlighted trace for the selected country with full hover data
            highlight_fig = px.choropleth(
                country_row,
                locations="country_iso_alpha",
                color_discrete_sequence=[highlight_color],
                 hover_name="country",
                 hover_data=hover_data_dict
            )
            
            fig.add_trace(highlight_fig.data[0])
            
            # Update the highlighted trace properties
            fig.data[-1].update(
                name=f"Selected: {selected_country}",
                showlegend=True,
                marker_line_color='#000000',
                marker_line_width=3
            )
            
            # Add zoom and center functionality for better visibility of small countries
            # Define regional centers and zoom levels for better country visibility
            country_coords = {
                'Albania': {'lat': 41.1533, 'lon': 20.1683, 'zoom': 6},
                'Andorra': {'lat': 42.5063, 'lon': 1.5218, 'zoom': 8},
                'Malta': {'lat': 35.9375, 'lon': 14.3754, 'zoom': 9},
                'Monaco': {'lat': 43.7384, 'lon': 7.4246, 'zoom': 10},
                'San Marino': {'lat': 43.9424, 'lon': 12.4578, 'zoom': 9},
                'Liechtenstein': {'lat': 47.166, 'lon': 9.5554, 'zoom': 9},
                'Luxembourg': {'lat': 49.8153, 'lon': 6.1296, 'zoom': 8},
                'Cyprus': {'lat': 35.1264, 'lon': 33.4299, 'zoom': 7},
                'Iceland': {'lat': 64.9631, 'lon': -19.0208, 'zoom': 5},
                'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'zoom': 10},
                'Brunei': {'lat': 4.5353, 'lon': 114.7277, 'zoom': 8},
                'Bahrain': {'lat': 26.0667, 'lon': 50.5577, 'zoom': 9},
                'Qatar': {'lat': 25.3548, 'lon': 51.1839, 'zoom': 8},
                'Kuwait': {'lat': 29.3117, 'lon': 47.4818, 'zoom': 8},
                'Maldives': {'lat': 3.2028, 'lon': 73.2207, 'zoom': 6},
                'Seychelles': {'lat': -4.6796, 'lon': 55.492, 'zoom': 8},
                'Mauritius': {'lat': -20.348404, 'lon': 57.552152, 'zoom': 9},
            }
            
            if selected_country in country_coords:
                coords = country_coords[selected_country]
                fig.update_geos(
                    center_lat=coords['lat'],
                    center_lon=coords['lon'],
                    projection_scale=coords['zoom']
                )
            else:
                # For larger countries, use default view but slightly zoomed
                fig.update_geos(
                    projection_scale=1.2
                )
    
    fig.update_layout(
        margin={"r":0, "t":60, "l":0, "b":0},  # Increased top margin for legend space
        geo=dict(
            showframe=False, 
            showcoastlines=False, 
            projection_type='equirectangular'
        ),
        legend=dict(
            x=0.02,  # Position legend on the left side
            y=0.98,  # Position near the top
            bgcolor="rgba(255,255,255,0.8)",  # Semi-transparent white background
            bordercolor="Black",
            borderwidth=1
        ),
        height=600,  # Increased height for better visibility of small countries
        width=1200
    )
    return fig
