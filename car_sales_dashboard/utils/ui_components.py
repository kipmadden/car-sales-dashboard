"""
UI/UX Improvements and Accessibility Module

Provides comprehensive user interface enhancements, responsive design,
and accessibility features for the Car Sales Dashboard.
"""

import reflex as rx
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class AccessibilityConfig:
    """Configuration for accessibility features"""
    
    # WCAG 2.1 AA compliant color ratios
    COLORS = {
        'primary': '#1f2937',      # Dark gray with high contrast
        'secondary': '#374151',    # Medium gray
        'accent': '#3b82f6',       # Blue with good contrast
        'success': '#10b981',      # Green
        'warning': '#f59e0b',      # Amber
        'error': '#ef4444',        # Red
        'background': '#ffffff',   # White
        'surface': '#f9fafb',      # Light gray
        'text_primary': '#111827', # Very dark gray
        'text_secondary': '#6b7280', # Medium gray
        'border': '#d1d5db'        # Light border
    }
    
    # Font sizes following accessibility guidelines
    FONT_SIZES = {
        'xs': '0.75rem',    # 12px
        'sm': '0.875rem',   # 14px  
        'base': '1rem',     # 16px (minimum for accessibility)
        'lg': '1.125rem',   # 18px
        'xl': '1.25rem',    # 20px
        'xxl': '1.5rem',    # 24px
        'title': '2rem'     # 32px
    }
    
    # Spacing for consistent layout
    SPACING = {
        'xs': '0.25rem',    # 4px
        'sm': '0.5rem',     # 8px
        'md': '1rem',       # 16px
        'lg': '1.5rem',     # 24px
        'xl': '2rem',       # 32px
        'xxl': '3rem'       # 48px
    }


class ResponsiveDesign:
    """Responsive design utilities"""
    
    BREAKPOINTS = {
        'mobile': '480px',
        'tablet': '768px',
        'desktop': '1024px',
        'large': '1200px'
    }
    
    @staticmethod
    def get_responsive_grid(
        mobile_cols: int = 1,
        tablet_cols: int = 2,
        desktop_cols: int = 3
    ) -> Dict[str, str]:
        """Get responsive grid configuration"""
        return {
            'display': 'grid',
            'grid_template_columns': f'repeat({mobile_cols}, 1fr)',
            'gap': AccessibilityConfig.SPACING['md'],
            f'@media (min-width: {ResponsiveDesign.BREAKPOINTS["tablet"]})': {
                'grid_template_columns': f'repeat({tablet_cols}, 1fr)'
            },
            f'@media (min-width: {ResponsiveDesign.BREAKPOINTS["desktop"]})': {
                'grid_template_columns': f'repeat({desktop_cols}, 1fr)'
            }
        }
    
    @staticmethod
    def get_responsive_text(
        mobile_size: str = 'base',
        desktop_size: str = 'lg'
    ) -> Dict[str, str]:
        """Get responsive text sizing"""
        return {
            'font_size': AccessibilityConfig.FONT_SIZES[mobile_size],
            f'@media (min-width: {ResponsiveDesign.BREAKPOINTS["desktop"]})': {
                'font_size': AccessibilityConfig.FONT_SIZES[desktop_size]
            }
        }


class LoadingStates:
    """Enhanced loading state components"""
    
    @staticmethod
    def create_skeleton_loader(
        height: str = "20px",
        width: str = "100%",
        border_radius: str = "4px"
    ) -> rx.Component:
        """Create a skeleton loading placeholder"""
        return rx.box(
            width=width,
            height=height,
            border_radius=border_radius,
            background="linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)",
            background_size="200% 100%",
            animation="skeleton-loading 1.5s ease-in-out infinite",
            style={
                '@keyframes skeleton-loading': {
                    '0%': {'background_position': '200% 0'},
                    '100%': {'background_position': '-200% 0'}
                }
            }
        )
    
    @staticmethod
    def create_chart_loader() -> rx.Component:
        """Create a chart-specific loading placeholder"""
        return rx.vstack(
            rx.hstack(
                LoadingStates.create_skeleton_loader("24px", "200px"),
                LoadingStates.create_skeleton_loader("16px", "100px"),
                spacing=AccessibilityConfig.SPACING['md'],
                width="100%",
                justify="between"
            ),
            LoadingStates.create_skeleton_loader("300px", "100%", "8px"),
            rx.hstack(
                LoadingStates.create_skeleton_loader("16px", "80px"),
                LoadingStates.create_skeleton_loader("16px", "80px"),
                LoadingStates.create_skeleton_loader("16px", "80px"),
                spacing=AccessibilityConfig.SPACING['lg'],
                width="100%",
                justify="center"
            ),
            spacing=AccessibilityConfig.SPACING['lg'],
            width="100%",
            padding=AccessibilityConfig.SPACING['lg'],
            border=f"1px solid {AccessibilityConfig.COLORS['border']}",
            border_radius="8px",
            background=AccessibilityConfig.COLORS['surface']
        )
    
    @staticmethod
    def create_spinner_with_text(text: str = "Loading...") -> rx.Component:
        """Create an accessible spinner with descriptive text"""
        return rx.vstack(
            rx.box(
                width="40px",
                height="40px",
                border=f"4px solid {AccessibilityConfig.COLORS['border']}",
                border_top=f"4px solid {AccessibilityConfig.COLORS['accent']}",
                border_radius="50%",
                animation="spin 1s linear infinite",
                style={
                    '@keyframes spin': {
                        '0%': {'transform': 'rotate(0deg)'},
                        '100%': {'transform': 'rotate(360deg)'}
                    }
                },
                # Accessibility attributes
                role="status",
                aria_label="Loading content"
            ),
            rx.text(
                text,
                font_size=AccessibilityConfig.FONT_SIZES['sm'],
                color=AccessibilityConfig.COLORS['text_secondary'],
                text_align="center"
            ),
            spacing=AccessibilityConfig.SPACING['md'],
            align="center",
            width="100%"
        )


class EnhancedControls:
    """Enhanced UI controls with accessibility features"""
    
    @staticmethod
    def create_accessible_slider(
        label: str,
        value: float,
        min_val: float,
        max_val: float,
        step: float,
        on_change,
        help_text: str = "",
        unit: str = ""
    ) -> rx.Component:
        """Create an accessible slider with proper labeling"""
        slider_id = f"slider-{label.lower().replace(' ', '-')}"
        
        return rx.vstack(
            rx.hstack(
                rx.text(
                    label,
                    font_weight="600",
                    font_size=AccessibilityConfig.FONT_SIZES['base'],
                    color=AccessibilityConfig.COLORS['text_primary'],
                    id=f"{slider_id}-label"
                ),
                rx.text(
                    f"{value:.2f}{unit}",
                    font_size=AccessibilityConfig.FONT_SIZES['sm'],
                    color=AccessibilityConfig.COLORS['text_secondary'],
                    font_weight="500",
                    id=f"{slider_id}-value"
                ),
                justify="between",
                width="100%"
            ),
            rx.slider(
                min=min_val,
                max=max_val,
                step=step,
                value=value,
                on_change=on_change,
                # Accessibility attributes
                aria_labelledby=f"{slider_id}-label",
                aria_describedby=f"{slider_id}-help" if help_text else None,
                aria_valuemin=min_val,
                aria_valuemax=max_val,
                aria_valuenow=value,
                role="slider",
                style={
                    'width': '100%',
                    'height': '8px',
                    'background': AccessibilityConfig.COLORS['border'],
                    'border_radius': '4px',
                    'outline': 'none',
                    '&:focus': {
                        'box_shadow': f'0 0 0 2px {AccessibilityConfig.COLORS["accent"]}'
                    }
                }
            ),
            rx.cond(
                help_text != "",
                rx.text(
                    help_text,
                    font_size=AccessibilityConfig.FONT_SIZES['xs'],
                    color=AccessibilityConfig.COLORS['text_secondary'],
                    id=f"{slider_id}-help"
                )
            ),
            spacing=AccessibilityConfig.SPACING['sm'],
            width="100%"
        )
    
    @staticmethod
    def create_accessible_button(
        text: str,
        on_click,
        variant: str = "primary",
        size: str = "md",
        disabled: bool = False,
        loading: bool = False,
        icon: Optional[str] = None,
        aria_label: Optional[str] = None
    ) -> rx.Component:
        """Create an accessible button with proper states"""
        
        # Button styling based on variant
        styles = {
            'primary': {
                'background': AccessibilityConfig.COLORS['accent'],
                'color': 'white',
                'border': f"2px solid {AccessibilityConfig.COLORS['accent']}"
            },
            'secondary': {
                'background': 'transparent',
                'color': AccessibilityConfig.COLORS['accent'],
                'border': f"2px solid {AccessibilityConfig.COLORS['accent']}"
            },
            'danger': {
                'background': AccessibilityConfig.COLORS['error'],
                'color': 'white',
                'border': f"2px solid {AccessibilityConfig.COLORS['error']}"
            }
        }
        
        # Size configurations
        sizes = {
            'sm': {'padding': '8px 16px', 'font_size': AccessibilityConfig.FONT_SIZES['sm']},
            'md': {'padding': '12px 24px', 'font_size': AccessibilityConfig.FONT_SIZES['base']},
            'lg': {'padding': '16px 32px', 'font_size': AccessibilityConfig.FONT_SIZES['lg']}
        }
        
        base_style = {
            **styles.get(variant, styles['primary']),
            **sizes.get(size, sizes['md']),
            'border_radius': '6px',
            'cursor': 'pointer' if not disabled else 'not-allowed',
            'opacity': '0.6' if disabled else '1',
            'transition': 'all 0.2s ease',
            'outline': 'none',
            '&:focus': {
                'box_shadow': f'0 0 0 3px {AccessibilityConfig.COLORS["accent"]}40'
            },
            '&:hover': {
                'opacity': '0.9' if not disabled else '0.6'
            }
        }
        
        button_content = rx.hstack(
            rx.cond(
                loading,
                LoadingStates.create_spinner_with_text(""),
                rx.cond(
                    icon is not None,
                    rx.icon(icon, size=16),
                    rx.fragment()
                )
            ),
            rx.text(text),
            spacing=AccessibilityConfig.SPACING['xs'],
            align="center"
        )
        
        return rx.button(
            button_content,
            on_click=on_click if not disabled and not loading else None,
            disabled=disabled or loading,
            aria_label=aria_label or text,
            aria_disabled=disabled or loading,
            style=base_style
        )


class ErrorStates:
    """Enhanced error state components"""
    
    @staticmethod
    def create_error_boundary(
        error_message: str,
        retry_action = None,
        context: str = "chart"
    ) -> rx.Component:
        """Create a comprehensive error boundary component"""
        return rx.vstack(
            rx.box(
                rx.hstack(
                    rx.icon(
                        "alert-triangle",
                        size=24,
                        color=AccessibilityConfig.COLORS['error']
                    ),
                    rx.vstack(
                        rx.text(
                            f"Unable to load {context}",
                            font_weight="600",
                            font_size=AccessibilityConfig.FONT_SIZES['lg'],
                            color=AccessibilityConfig.COLORS['text_primary']
                        ),
                        rx.text(
                            error_message,
                            font_size=AccessibilityConfig.FONT_SIZES['sm'],
                            color=AccessibilityConfig.COLORS['text_secondary']
                        ),
                        spacing=AccessibilityConfig.SPACING['xs'],
                        align="start"
                    ),
                    spacing=AccessibilityConfig.SPACING['md'],
                    align="start"
                ),
                rx.cond(
                    retry_action is not None,
                    EnhancedControls.create_accessible_button(
                        "Try Again",
                        retry_action,
                        variant="secondary",
                        size="sm",
                        icon="refresh-cw"
                    )
                ),
                spacing=AccessibilityConfig.SPACING['lg'],
                align="center"
            ),
            padding=AccessibilityConfig.SPACING['xl'],
            border=f"1px solid {AccessibilityConfig.COLORS['error']}",
            border_radius="8px",
            background=f"{AccessibilityConfig.COLORS['error']}08",
            width="100%",
            role="alert",
            aria_live="polite"
        )
    
    @staticmethod
    def create_validation_message(
        message: str,
        type: str = "error"
    ) -> rx.Component:
        """Create inline validation messages"""
        colors = {
            'error': AccessibilityConfig.COLORS['error'],
            'warning': AccessibilityConfig.COLORS['warning'],
            'success': AccessibilityConfig.COLORS['success']
        }
        
        icons = {
            'error': 'x-circle',
            'warning': 'alert-triangle', 
            'success': 'check-circle'
        }
        
        return rx.hstack(
            rx.icon(
                icons.get(type, 'alert-triangle'),
                size=16,
                color=colors.get(type, AccessibilityConfig.COLORS['error'])
            ),
            rx.text(
                message,
                font_size=AccessibilityConfig.FONT_SIZES['sm'],
                color=colors.get(type, AccessibilityConfig.COLORS['error'])
            ),
            spacing=AccessibilityConfig.SPACING['xs'],
            align="center",
            role="alert" if type == "error" else "status",
            aria_live="polite"
        )


class LayoutComponents:
    """Enhanced layout components"""
    
    @staticmethod
    def create_section_header(
        title: str,
        subtitle: str = "",
        actions: List[rx.Component] = None
    ) -> rx.Component:
        """Create a semantic section header"""
        return rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        title,
                        level=2,
                        font_size=AccessibilityConfig.FONT_SIZES['title'],
                        color=AccessibilityConfig.COLORS['text_primary'],
                        font_weight="700"
                    ),
                    rx.cond(
                        subtitle != "",
                        rx.text(
                            subtitle,
                            font_size=AccessibilityConfig.FONT_SIZES['base'],
                            color=AccessibilityConfig.COLORS['text_secondary']
                        )
                    ),
                    spacing=AccessibilityConfig.SPACING['xs'],
                    align="start"
                ),
                rx.cond(
                    actions is not None and len(actions) > 0,
                    rx.hstack(
                        *actions,
                        spacing=AccessibilityConfig.SPACING['sm']
                    )
                ),
                justify="between",
                align="start",
                width="100%"
            ),
            spacing=AccessibilityConfig.SPACING['md'],
            width="100%",
            padding_bottom=AccessibilityConfig.SPACING['lg'],
            border_bottom=f"1px solid {AccessibilityConfig.COLORS['border']}"
        )
    
    @staticmethod
    def create_card(
        content: rx.Component,
        title: str = "",
        padding: str = "lg",
        elevated: bool = True
    ) -> rx.Component:
        """Create a semantic card component"""
        card_style = {
            'border_radius': '12px',
            'border': f"1px solid {AccessibilityConfig.COLORS['border']}",
            'background': AccessibilityConfig.COLORS['background'],
            'width': '100%'
        }
        
        if elevated:
            card_style['box_shadow'] = '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
        
        return rx.box(
            rx.vstack(
                rx.cond(
                    title != "",
                    rx.text(
                        title,
                        font_weight="600",
                        font_size=AccessibilityConfig.FONT_SIZES['lg'],
                        color=AccessibilityConfig.COLORS['text_primary'],
                        padding_bottom=AccessibilityConfig.SPACING['md'],
                        border_bottom=f"1px solid {AccessibilityConfig.COLORS['border']}"
                    )
                ),
                content,
                spacing=AccessibilityConfig.SPACING['md'],
                width="100%"
            ),
            padding=AccessibilityConfig.SPACING[padding],
            style=card_style
        )
