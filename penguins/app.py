import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
from shinywidgets import output_widget, render_widget, render_plotly
import seaborn as sns
from shiny import render
import palmerpenguins
from shiny import reactive


penguins_df = load_penguins()

ui.page_opts(title="Mahesh Bashyal's Penguin Data", fillable=True)

# Sidebar for User Interaction
with ui.sidebar(open="open"):
        ui.h2("Sidebar")
        ui.input_selectize(
            "selected_attribute",
            "Select Attributes",
            ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
            )
        ui.input_numeric(
            "plotly_bin_count",
            "Plotly Number of Bins",
            10,
            min=1,
            max=20,
            )
        ui.input_slider(
            "seaborn_bin_count",
            "Seaborn Number of Bins",
            min= 0,
            max= 100,
            value= 20
            )
        ui.input_checkbox_group(
            "selected_species_list",
            "Choose Species",
            ["Adelie","Gentoo","Chinstrap"],
            selected=["Adelie","Gentoo","Chinstrap"],
            inline=False
            )
        ui.hr()

# Use ui.a() to add a hyperlink to the sidebar
ui.a("GitHub",href="https://github.com/Mahesh1416/cintel-02-data/tree/main",target= "_blank") #to add a hyperlink to the sidebar

with ui.layout_columns():

    # New data table Using Filtered Data    
    with ui.card():
        "Penguins Data Table"
        @render.data_frame
        def data_table():
            return render.DataTable(filtered_data())

    # Display data Grid Using Filtered Data    
    with ui.card():
        "Penguins Data Grid"
        @render.data_frame
        def data_grid():
            return render.DataGrid(filtered_data())

with ui.layout_columns():
    
    # Plotly Histogram    
    with ui.card():
        ui.card_header("Plotly Histogram")
        @render_plotly
        def plotlyhistogram():
            return px.histogram(
                filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species"
            ).update_layout(
                xaxis_title="Bill length (mm)",
                yaxis_title="Counts"
            )
            
    # Seaborn Histogram    
    with ui.card():
        ui.card_header("Seaborn Histogram")
       
        @render.plot
        def seabornhistogram():
            ax=sns.histplot(
                data=filtered_data(), 
                x=input.selected_attribute(), 
                bins=input.seaborn_bin_count(),
               )
            ax.set_title("Palmer Penguins")
            ax.set_xlabel(input.selected_attribute())
            ax.set_ylabel("Number")
            return ax
           
    # Plotly Scatterplot
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                 labels={
                        "bill_length_mm": "Bill Length (mm)",
                        "body_mass_g": "Body Mass (g)",
                    },
                    size_max=8, # set the maximum marker size
                )


@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    if selected_species:
        return penguins_df[penguins_df['species'].isin(selected_species)]
    return penguins_df
       
       
