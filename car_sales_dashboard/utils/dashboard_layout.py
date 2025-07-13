"""
Enhanced Dashboard Layout with Accessibility and Responsive Design

Provides the main dashboard layout with improved UX, accessibility features,
and responsive design for the Car Sales Dashboard.
"""

import reflex as rx
from car_sales_dashboard.utils.ui_components import (
    AccessibilityConfig, ResponsiveDesign, LoadingStates,
    EnhancedControls, ErrorStates, LayoutComponents
)
from car_sales_dashboard.state import State
from typing import List, Optional


class DashboardLayout:
    """Enhanced dashboard layout with accessibility and responsive design"""
    
    @staticmethod
    def create_header() -> rx.Component:
        """Create accessible dashboard header"""
        return rx.box(
            rx.hstack(
                # Logo and title
                rx.hstack(
                    rx.image(
                        src="/logo.png",
                        width="40px",
                        height="40px",
                        alt="Car Sales Dashboard Logo"
                    ),
                    rx.vstack(
                        rx.heading(
                            "Car Sales Dashboard",
                            level=1,
                            font_size=AccessibilityConfig.FONT_SIZES['title'],
                            color=AccessibilityConfig.COLORS['text_primary'],
                            margin="0"
                        ),
                        rx.text(
                            "Interactive forecasting and analytics",
                            font_size=AccessibilityConfig.FONT_SIZES['sm'],
                            color=AccessibilityConfig.COLORS['text_secondary']
                        ),
                        spacing="2px",
                        align="start"
                    ),
                    spacing=AccessibilityConfig.SPACING['md'],
                    align="center"
                ),
                
                # User actions and accessibility controls
                rx.hstack(
                    DashboardLayout.create_accessibility_controls(),
                    rx.box(
                        # User menu would go here
                        width="40px",
                        height="40px",
                        border_radius="50%",
                        background=AccessibilityConfig.COLORS['surface'],
                        display="flex",
                        align_items="center",
                        justify_content="center"
                    ),
                    spacing=AccessibilityConfig.SPACING['md']
                ),
                
                justify="between",
                align="center",
                width="100%"
            ),
            padding=AccessibilityConfig.SPACING['lg'],
            border_bottom=f"1px solid {AccessibilityConfig.COLORS['border']}",
            background=AccessibilityConfig.COLORS['background'],
            # Sticky header for better UX
            position="sticky",
            top="0",
            z_index="100",
            role="banner"
        )
    
    @staticmethod
    def create_accessibility_controls() -> rx.Component:
        """Create accessibility control panel"""
        return rx.hstack(
            # Skip to main content link (screen reader accessible)
            rx.link(
                "Skip to main content",
                href="#main-content",
                style={
                    'position': 'absolute',
                    'left': '-9999px',
                    'width': '1px',
                    'height': '1px',
                    'overflow': 'hidden',
                    '&:focus': {
                        'position': 'static',
                        'width': 'auto',
                        'height': 'auto',
                        'padding': AccessibilityConfig.SPACING['sm'],
                        'background': AccessibilityConfig.COLORS['accent'],
                        'color': 'white',
                        'text_decoration': 'none',
                        'border_radius': '4px'
                    }
                }
            ),
            
            # High contrast toggle
            EnhancedControls.create_accessible_button(
                "",
                on_click=lambda: None,  # Would toggle high contrast mode
                variant="secondary",
                size="sm",
                icon="contrast",
                aria_label="Toggle high contrast mode"
            ),
            
            # Font size controls
            rx.hstack(
                EnhancedControls.create_accessible_button(
                    "A-",
                    on_click=lambda: None,  # Would decrease font size
                    variant="secondary", 
                    size="sm",
                    aria_label="Decrease text size"
                ),
                EnhancedControls.create_accessible_button(
                    "A+",
                    on_click=lambda: None,  # Would increase font size
                    variant="secondary",
                    size="sm", 
                    aria_label="Increase text size"
                ),
                spacing="2px"
            ),
            
            spacing=AccessibilityConfig.SPACING['sm']
        )
    
    @staticmethod
    def create_sidebar() -> rx.Component:
        """Create responsive sidebar with controls"""
        return rx.box(
            rx.vstack(
                LayoutComponents.create_section_header(
                    "Controls",
                    "Adjust parameters to see forecast changes"
                ),
                
                # Model selection
                DashboardLayout.create_model_selector(),
                
                # Scenario controls
                DashboardLayout.create_scenario_controls(),
                
                # Time range controls
                DashboardLayout.create_time_controls(),
                
                # Data actions
                DashboardLayout.create_data_actions(),
                
                spacing=AccessibilityConfig.SPACING['xl'],
                width="100%"
            ),
            width="100%",
            max_width="400px",
            padding=AccessibilityConfig.SPACING['lg'],
            background=AccessibilityConfig.COLORS['surface'],
            border_right=f"1px solid {AccessibilityConfig.COLORS['border']}",
            height="100vh",
            overflow_y="auto",
            role="complementary",
            aria_label="Dashboard controls"
        )
    
    @staticmethod
    def create_model_selector() -> rx.Component:
        """Create accessible model selection"""
        return LayoutComponents.create_card(
            rx.vstack(
                rx.text(
                    "Forecasting Model",
                    font_weight="600",
                    font_size=AccessibilityConfig.FONT_SIZES['base'],
                    color=AccessibilityConfig.COLORS['text_primary']
                ),
                rx.select(
                    ["Linear Regression", "Random Forest"],
                    value=State.model_type,
                    on_change=State.update_model_type,
                    aria_label="Select forecasting model",
                    style={
                        'width': '100%',
                        'padding': AccessibilityConfig.SPACING['sm'],
                        'border': f"2px solid {AccessibilityConfig.COLORS['border']}",
                        'border_radius': '6px',
                        'font_size': AccessibilityConfig.FONT_SIZES['base'],
                        '&:focus': {
                            'border_color': AccessibilityConfig.COLORS['accent'],
                            'outline': 'none'
                        }
                    }
                ),
                rx.text(
                    "Choose the machine learning model for sales forecasting",
                    font_size=AccessibilityConfig.FONT_SIZES['xs'],
                    color=AccessibilityConfig.COLORS['text_secondary']
                ),
                spacing=AccessibilityConfig.SPACING['sm'],
                align="start",
                width="100%"
            ),
            title="",
            padding="md"
        )
    
    @staticmethod
    def create_scenario_controls() -> rx.Component:
        """Create accessible scenario modification controls"""
        return LayoutComponents.create_card(
            rx.vstack(
                EnhancedControls.create_accessible_slider(
                    "Gas Price Impact",
                    State.gas_price_modifier,
                    0.1,
                    3.0,
                    0.1,
                    State.update_gas_price,
                    "Modify gas price impact on sales (0.1 = 90% decrease, 3.0 = 200% increase)",
                    "x"
                ),
                
                EnhancedControls.create_accessible_slider(
                    "Economic Conditions (CPI)",
                    State.cpi_modifier,
                    0.1,
                    3.0,
                    0.1,
                    State.update_cpi,
                    "Adjust economic conditions impact on sales",
                    "x"
                ),
                
                EnhancedControls.create_accessible_slider(
                    "Consumer Interest",
                    State.search_volume_modifier,
                    0.1,
                    3.0,
                    0.1,
                    State.update_search_volume,
                    "Modify consumer search interest impact on sales",
                    "x"
                ),
                
                rx.box(
                    rx.text(
                        "Forecast Horizon",
                        font_weight="600",
                        font_size=AccessibilityConfig.FONT_SIZES['base'],
                        color=AccessibilityConfig.COLORS['text_primary']
                    ),
                    rx.select(
                        ["6", "12", "18", "24"],
                        value=str(State.forecast_months),
                        on_change=State.update_forecast_months,
                        aria_label="Select forecast duration in months",
                        style={
                            'width': '100%',
                            'padding': AccessibilityConfig.SPACING['sm'],
                            'border': f"2px solid {AccessibilityConfig.COLORS['border']}",
                            'border_radius': '6px',
                            'margin_top': AccessibilityConfig.SPACING['sm']
                        }
                    ),
                    width="100%"
                ),
                
                spacing=AccessibilityConfig.SPACING['lg'],
                width="100%"
            ),
            title="Scenario Parameters",
            padding="md"
        )
    
    @staticmethod
    def create_time_controls() -> rx.Component:
        """Create time range filter controls"""
        return LayoutComponents.create_card(
            rx.vstack(
                rx.text(
                    "Historical Data Range",
                    font_weight="600",
                    font_size=AccessibilityConfig.FONT_SIZES['base'],
                    color=AccessibilityConfig.COLORS['text_primary']
                ),
                
                rx.hstack(
                    rx.vstack(
                        rx.text("Start Date", font_size=AccessibilityConfig.FONT_SIZES['sm']),
                        rx.input(
                            type="date",
                            value=State.start_date,
                            on_change=State.update_start_date,
                            aria_label="Select start date for data range",
                            style={'width': '100%', 'padding': AccessibilityConfig.SPACING['sm']}
                        ),
                        spacing=AccessibilityConfig.SPACING['xs'],
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("End Date", font_size=AccessibilityConfig.FONT_SIZES['sm']),
                        rx.input(
                            type="date",
                            value=State.end_date,
                            on_change=State.update_end_date,
                            aria_label="Select end date for data range",
                            style={'width': '100%', 'padding': AccessibilityConfig.SPACING['sm']}
                        ),
                        spacing=AccessibilityConfig.SPACING['xs'],
                        width="100%"
                    ),
                    spacing=AccessibilityConfig.SPACING['md'],
                    width="100%"
                ),
                
                EnhancedControls.create_accessible_button(
                    "Apply Date Filter",
                    State.filter_data,
                    variant="primary",
                    size="sm",
                    icon="filter"
                ),
                
                spacing=AccessibilityConfig.SPACING['md'],
                width="100%"
            ),
            title="",
            padding="md"
        )
    
    @staticmethod
    def create_data_actions() -> rx.Component:
        """Create data management actions"""
        return LayoutComponents.create_card(
            rx.vstack(
                rx.text(
                    "Data Management",
                    font_weight="600",
                    font_size=AccessibilityConfig.FONT_SIZES['base'],
                    color=AccessibilityConfig.COLORS['text_primary']
                ),
                
                EnhancedControls.create_accessible_button(
                    "Upload New Data",
                    lambda: None,  # Would trigger file upload
                    variant="secondary",
                    size="sm",
                    icon="upload",
                    aria_label="Upload new sales data file"
                ),
                
                EnhancedControls.create_accessible_button(
                    "Export Forecast",
                    lambda: None,  # Would trigger export
                    variant="secondary",
                    size="sm", 
                    icon="download",
                    aria_label="Export forecast data"
                ),
                
                EnhancedControls.create_accessible_button(
                    "Reset to Defaults",
                    lambda: None,  # Would reset all parameters
                    variant="danger",
                    size="sm",
                    icon="refresh-cw",
                    aria_label="Reset all parameters to default values"
                ),
                
                spacing=AccessibilityConfig.SPACING['sm'],
                width="100%"
            ),
            title="",
            padding="md"
        )
    
    @staticmethod
    def create_main_content() -> rx.Component:
        """Create main dashboard content area"""
        return rx.box(
            rx.vstack(
                # Status indicators
                DashboardLayout.create_status_bar(),
                
                # Chart grid
                DashboardLayout.create_chart_grid(),
                
                spacing=AccessibilityConfig.SPACING['lg'],
                width="100%"
            ),
            id="main-content",  # For skip navigation
            padding=AccessibilityConfig.SPACING['lg'],
            width="100%",
            role="main"
        )
    
    @staticmethod
    def create_status_bar() -> rx.Component:
        """Create status indicator bar"""
        return rx.hstack(
            rx.hstack(
                rx.icon(
                    "database",
                    size=16,
                    color=AccessibilityConfig.COLORS['success']
                ),
                rx.text(
                    f"Data: {len(State.filtered_data)} records",
                    font_size=AccessibilityConfig.FONT_SIZES['sm'],
                    color=AccessibilityConfig.COLORS['text_secondary']
                ),
                spacing=AccessibilityConfig.SPACING['xs']
            ),
            rx.hstack(
                rx.icon(
                    "trending-up",
                    size=16,
                    color=AccessibilityConfig.COLORS['accent']
                ),
                rx.text(
                    f"Model: {State.model_type}",
                    font_size=AccessibilityConfig.FONT_SIZES['sm'],
                    color=AccessibilityConfig.COLORS['text_secondary']
                ),
                spacing=AccessibilityConfig.SPACING['xs']
            ),
            rx.hstack(
                rx.icon(
                    "clock",
                    size=16,
                    color=AccessibilityConfig.COLORS['warning']
                ),
                rx.text(
                    f"Forecast: {State.forecast_months} months",
                    font_size=AccessibilityConfig.FONT_SIZES['sm'],
                    color=AccessibilityConfig.COLORS['text_secondary']
                ),
                spacing=AccessibilityConfig.SPACING['xs']
            ),
            spacing=AccessibilityConfig.SPACING['lg'],
            justify="start",
            width="100%",
            padding=AccessibilityConfig.SPACING['md'],
            background=AccessibilityConfig.COLORS['surface'],
            border_radius="8px",
            border=f"1px solid {AccessibilityConfig.COLORS['border']}"
        )
    
    @staticmethod
    def create_chart_grid() -> rx.Component:
        """Create responsive chart grid"""
        return rx.box(
            # Sales trend chart (full width)
            LayoutComponents.create_card(
                DashboardLayout.create_chart_with_loading(
                    State.get_sales_trend_chart,
                    "Sales Trend and Forecast"
                ),
                title="Sales Trend and Forecast",
                elevated=True
            ),
            
            # Chart grid for smaller charts
            rx.box(
                LayoutComponents.create_card(
                    DashboardLayout.create_chart_with_loading(
                        State.get_vehicle_type_chart,
                        "Vehicle Type Distribution"
                    ),
                    title="Vehicle Type Distribution",
                    elevated=True
                ),
                
                LayoutComponents.create_card(
                    DashboardLayout.create_chart_with_loading(
                        State.get_region_chart,
                        "Regional Sales"
                    ),
                    title="Regional Sales",
                    elevated=True
                ),
                
                LayoutComponents.create_card(
                    DashboardLayout.create_chart_with_loading(
                        State.get_exogenous_impact_chart,
                        "Market Factors Impact"
                    ),
                    title="Market Factors Impact",
                    elevated=True
                ),
                
                style=ResponsiveDesign.get_responsive_grid(1, 2, 3)
            ),
            
            spacing=AccessibilityConfig.SPACING['xl'],
            width="100%"
        )
    
    @staticmethod
    def create_chart_with_loading(chart_method, chart_name: str) -> rx.Component:
        """Create chart with loading and error states"""
        return rx.cond(
            # Check if data is loading
            State.is_loading,
            LoadingStates.create_chart_loader(),
            
            # Check if there's an error
            rx.cond(
                State.has_error,
                ErrorStates.create_error_boundary(
                    f"Failed to generate {chart_name}. Please check your data and try again.",
                    retry_action=chart_method,
                    context=chart_name.lower()
                ),
                
                # Show the actual chart
                chart_method()
            )
        )
    
    @staticmethod
    def create_complete_layout() -> rx.Component:
        """Create the complete dashboard layout"""
        return rx.vstack(
            DashboardLayout.create_header(),
            
            rx.hstack(
                # Responsive sidebar - hidden on mobile
                rx.box(
                    DashboardLayout.create_sidebar(),
                    display=["none", "none", "block"],  # Hidden on mobile/tablet
                    flex_shrink="0"
                ),
                
                # Main content area
                DashboardLayout.create_main_content(),
                
                spacing="0",
                width="100%",
                height="calc(100vh - 80px)"  # Account for header height
            ),
            
            spacing="0",
            width="100%",
            min_height="100vh"
        )
