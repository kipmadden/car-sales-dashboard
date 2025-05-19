"""
Client-side JavaScript for updating charts in the dashboard.

This module provides JavaScript functions that will be injected into the page
to update Plotly charts using window.setCustomValue.
"""

def get_chart_scripts():
    """
    Get JavaScript scripts to update charts on the client side.
    
    Returns:
        str: JavaScript code to update charts on client side
    """
    return """
<script>
// Function to update charts when data changes
function updateCharts() {
    // Get chart data from app state
    var state = window.__dashboard_state || {};
    
    // Check if sales_trend_chart exists
    var salesTrendChart = document.getElementById('sales-trend-chart');
    if (salesTrendChart) {
        console.log("Updating sales trend chart");
        try {
            // Use Plotly to render chart (This is just a placeholder)
            var data = [{
                x: [1, 2, 3, 4],
                y: [10, 15, 13, 17],
                type: 'scatter'
            }];
            var layout = {
                title: 'Sales Trend Chart',
                height: 500
            };
            Plotly.newPlot('sales-trend-chart', data, layout);
        } catch (e) {
            console.error("Error updating sales trend chart:", e);
        }
    }
    
    // Do similar for other charts
}

// Update charts on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log("Page loaded, updating charts");
    setTimeout(updateCharts, 500); // Small delay to ensure elements are ready
});

// Update charts when state changes
window.addEventListener('state_change', function() {
    console.log("State changed, updating charts");
    updateCharts();
});
</script>
"""
