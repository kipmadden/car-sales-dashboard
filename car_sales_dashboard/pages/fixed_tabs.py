# This file contains the fixed tabs implementation
import reflex as rx
from car_sales_dashboard.state import DashboardState
from car_sales_dashboard.components.static_charts import create_static_chart
from car_sales_dashboard.components.tables import create_forecast_table, create_summary_table

def create_tabs():
    """Create the tabs component with correct argument ordering"""
    return rx.tabs.root(
        # All positional arguments first
        rx.tabs.list(
            rx.tabs.trigger("Sales Forecast", value="sales", color="black"),
            rx.tabs.trigger("Vehicle Analysis", value="vehicles", color="black"),
            rx.tabs.trigger("Geographic", value="geographic", color="black"),
            rx.tabs.trigger("Economic Factors", value="economic", color="black"),
        ),
        rx.tabs.content(
            rx.vstack(
                rx.box(
                    rx.heading("Sales Trend and Forecast", color="black", size="4"),
                    rx.center(
                        rx.html("""
                            <div id="sales-chart" style="width: 100%; height: 500px;"></div>
                            <script>
                                async function loadSalesChart() {
                                    try {
                                        const data = await window.pyodide.runPythonAsync(`
                                            from car_sales_dashboard.state import DashboardState
                                            import json
                                            chart_data = DashboardState.get_sales_trend_chart()
                                            json.dumps(chart_data)
                                        `);
                                        const chartData = JSON.parse(data);
                                        Plotly.newPlot('sales-chart', chartData.data, chartData.layout);
                                    } catch (e) {
                                        console.error("Failed to load sales chart:", e);
                                        document.getElementById('sales-chart').innerHTML = 
                                            "<p>Error loading chart</p>";
                                    }
                                }
                                setTimeout(loadSalesChart, 100);
                            </script>
                        """),
                        height="500px",
                        width="100%",
                    ),
                    width="100%",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
                ),
                rx.box(height="20px"),  # Add space between chart and controls
                rx.hstack(
                    rx.switch(
                        on_change=DashboardState.toggle_table,
                        is_checked=DashboardState.show_table
                    ),
                    rx.text("Show Forecast Table", color="black"),
                    margin_top="2em",
                    margin_bottom="1em",
                    padding="0.5em",
                ),
                rx.cond(
                    DashboardState.show_table,
                    create_forecast_table(DashboardState.forecast_data),
                    rx.text("")
                ),
                width="100%",
            ),
            value="sales",
        ),
        rx.tabs.content(
            rx.vstack(
                rx.hstack(
                    # Use box containers instead of fragments
                    rx.box(
                        rx.heading("Sales by Vehicle Type", color="black", size="4"),
                        rx.center(
                            rx.html("""
                                <div id="vehicle-type-chart" style="width: 100%; height: 400px;"></div>
                                <script>
                                    async function loadVehicleTypeChart() {
                                        try {
                                            const data = await window.pyodide.runPythonAsync(`
                                                from car_sales_dashboard.components import create_vehicle_type_chart
                                                from car_sales_dashboard.state import DashboardState
                                                import json
                                                df = DashboardState._filtered_df
                                                chart_data = create_vehicle_type_chart(df)
                                                json.dumps(chart_data)
                                            `);
                                            const chartData = JSON.parse(data);
                                            Plotly.newPlot('vehicle-type-chart', chartData.data, chartData.layout);
                                        } catch (e) {
                                            console.error("Failed to load vehicle type chart:", e);
                                            document.getElementById('vehicle-type-chart').innerHTML = 
                                                "<p>Error loading chart</p>";
                                        }
                                    }
                                    setTimeout(loadVehicleTypeChart, 100);
                                </script>
                            """),
                            height="400px",
                            width="100%",
                        ),
                        width="100%",
                        padding="1.5em",
                        background="white",
                        border_radius="md",
                        border="1px solid #EEE",
                        margin_top="1.5em",
                        margin_bottom="1.5em",
                    ),
                    rx.box(
                        rx.heading("Top Models by Sales", color="black", size="4"),
                        rx.center(
                            rx.html("""
                                <div id="top-models-chart" style="width: 100%; height: 400px;"></div>
                                <script>
                                    async function loadTopModelsChart() {
                                        try {
                                            const data = await window.pyodide.runPythonAsync(`
                                                from car_sales_dashboard.components import create_top_models_chart
                                                from car_sales_dashboard.state import DashboardState
                                                import json
                                                df = DashboardState._filtered_df
                                                chart_data = create_top_models_chart(df)
                                                json.dumps(chart_data)
                                            `);
                                            const chartData = JSON.parse(data);
                                            Plotly.newPlot('top-models-chart', chartData.data, chartData.layout);
                                        } catch (e) {
                                            console.error("Failed to load top models chart:", e);
                                            document.getElementById('top-models-chart').innerHTML = 
                                                "<p>Error loading chart</p>";
                                        }
                                    }
                                    setTimeout(loadTopModelsChart, 100);
                                </script>
                            """),
                            height="400px",
                            width="100%",
                        ),
                        width="100%",
                        padding="1.5em",
                        background="white",
                        border_radius="md",
                        border="1px solid #EEE",
                        margin_top="1.5em",
                        margin_bottom="1.5em",
                    ),
                    width="100%",
                ),
                rx.box(
                    rx.heading("Sales by Month and Vehicle Type", color="black", size="4"),
                    rx.center(
                        rx.html("""
                            <div id="sales-by-month-chart" style="width: 100%; height: 400px;"></div>
                            <script>
                                async function loadSalesByMonthChart() {
                                    try {
                                        const data = await window.pyodide.runPythonAsync(`
                                            from car_sales_dashboard.components import create_heatmap_chart
                                            from car_sales_dashboard.state import DashboardState
                                            import json
                                            df = DashboardState._filtered_df
                                            chart_data = create_heatmap_chart(df, x_col='month', y_col='vehicle_type')
                                            json.dumps(chart_data)
                                        `);
                                        const chartData = JSON.parse(data);
                                        Plotly.newPlot('sales-by-month-chart', chartData.data, chartData.layout);
                                    } catch (e) {
                                        console.error("Failed to load sales by month chart:", e);
                                        document.getElementById('sales-by-month-chart').innerHTML = 
                                            "<p>Error loading chart</p>";
                                    }
                                }
                                setTimeout(loadSalesByMonthChart, 100);
                            </script>
                        """),
                        height="400px",
                        width="100%",
                    ),
                    width="100%",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
                ),
                width="100%",
            ),
            value="vehicles",
        ),
        rx.tabs.content(
            rx.vstack(
                rx.box(
                    rx.heading("Sales by Region", color="black", size="4"),
                    rx.center(
                        rx.html("""
                            <div id="region-chart" style="width: 100%; height: 400px;"></div>
                            <script>
                                async function loadRegionChart() {
                                    try {
                                        const data = await window.pyodide.runPythonAsync(`
                                            from car_sales_dashboard.components import create_region_chart
                                            from car_sales_dashboard.state import DashboardState
                                            import json
                                            df = DashboardState._filtered_df
                                            chart_data = create_region_chart(df)
                                            json.dumps(chart_data)
                                        `);
                                        const chartData = JSON.parse(data);
                                        Plotly.newPlot('region-chart', chartData.data, chartData.layout);
                                    } catch (e) {
                                        console.error("Failed to load region chart:", e);
                                        document.getElementById('region-chart').innerHTML = 
                                            "<p>Error loading chart</p>";
                                    }
                                }
                                setTimeout(loadRegionChart, 100);
                            </script>
                        """),
                        height="400px",
                        width="100%",
                    ),
                    width="100%",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
                ),
                rx.box(
                    rx.heading("Sales by State", color="black", size="4"),
                    rx.center(
                        rx.html("""
                            <div id="state-map-chart" style="width: 100%; height: 500px;"></div>
                            <script>
                                async function loadStateMapChart() {
                                    try {
                                        const data = await window.pyodide.runPythonAsync(`
                                            from car_sales_dashboard.components import create_state_map_chart
                                            from car_sales_dashboard.state import DashboardState
                                            import json
                                            df = DashboardState._filtered_df
                                            chart_data = create_state_map_chart(df)
                                            json.dumps(chart_data)
                                        `);
                                        const chartData = JSON.parse(data);
                                        Plotly.newPlot('state-map-chart', chartData.data, chartData.layout);
                                    } catch (e) {
                                        console.error("Failed to load state map chart:", e);
                                        document.getElementById('state-map-chart').innerHTML = 
                                            "<p>Error loading chart</p>";
                                    }
                                }
                                setTimeout(loadStateMapChart, 100);
                            </script>
                        """),
                        height="500px",
                        width="100%",
                    ),
                    width="100%",
                    padding="1.5em",
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
                ),
                width="100%",
            ),
            value="geographic",
        ),
        rx.tabs.content(
            rx.vstack(
                rx.box(
                    rx.heading("Exogenous Variable Trends", color="black", size="4"),
                    rx.center(
                        rx.html("""
                            <div id="exogenous-impact-chart" style="width: 100%; height: 500px;"></div>
                            <script>
                                async function loadExogenousImpactChart() {
                                    try {
                                        const data = await window.pyodide.runPythonAsync(`
                                            from car_sales_dashboard.components import create_exogenous_impact_chart
                                            from car_sales_dashboard.state import DashboardState
                                            import json
                                            df = DashboardState._forecast_df
                                            chart_data = create_exogenous_impact_chart(df)
                                            json.dumps(chart_data)
                                        `);
                                        const chartData = JSON.parse(data);
                                        Plotly.newPlot('exogenous-impact-chart', chartData.data, chartData.layout);
                                    } catch (e) {
                                        console.error("Failed to load exogenous impact chart:", e);
                                        document.getElementById('exogenous-impact-chart').innerHTML = 
                                            "<p>Error loading chart</p>";
                                    }
                                }
                                setTimeout(loadExogenousImpactChart, 100);
                            </script>
                        """),
                        height="500px",
                        width="100%",
                    ),
                    width="100%",
                    padding="1.5em",
                    background="white", 
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1.5em",
                    margin_bottom="1.5em",
                ),
                rx.box(
                    create_summary_table(
                        DashboardState.filtered_data,
                        groupby_col='vehicle_type'
                    ),
                    width="100%",
                    padding="1em", 
                    background="white",
                    border_radius="md",
                    border="1px solid #EEE",
                    margin_top="1em",
                ),
                width="100%",
            ),
            value="economic",
        ),
        # Then all keyword arguments
        on_change=DashboardState.update_active_tab,
        default_value="sales",
        orientation="horizontal",
        width="100%",
        variant="enclosed",
        margin_top="1em",
    )
