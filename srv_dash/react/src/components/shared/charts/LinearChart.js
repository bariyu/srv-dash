import React from 'react';

import BaseChart from './BaseChart';

export default class LinearChart extends BaseChart {
    componentDidMount() {
        const { chartData } = this.props;
        const { name, series, data_key, metric_title, unit_name } = chartData;

        var xScale = new Plottable.Scales.Time();
        var yScale = new Plottable.Scales.Linear();
        var colorScale = new Plottable.Scales.Color();

        var xAxis = new Plottable.Axes.Time(xScale, "bottom");
        var yAxis = new Plottable.Axes.Numeric(yScale, "left");

        var legend = new Plottable.Components.Legend(colorScale).maxEntriesPerRow(series.length);

        var plots = new Plottable.Components.Group();
        var panZoom = new Plottable.Interactions.PanZoom(xScale, null);
        panZoom.attachTo(plots);

        var chartLabel = new Plottable.Components.AxisLabel(metric_title);

        var chart = new Plottable.Components.Table([
            [null, chartLabel],
            [null, legend],
            [yAxis, plots],
            [null, xAxis]
        ]);

        for (var i = 0; i < series.length; i++) {
            var plot = new Plottable.Plots.Line()
                .addDataset(new Plottable.Dataset(series[i].data))
                .x(function(d) { return new Date(d.time); }, xScale)
                .y(function(d) { return d[data_key]; }, yScale)
                .attr("stroke", colorScale.scale(series[i].name))
                .attr("stroke-width", 1);

            plots.append(plot);
        }


        chart.renderTo(`svg#${name}`);

        var tooltipAnchorSelection = plots.foreground().append("circle").attr({
            r: 3,
            opacity: 0
        });

        var tooltipAnchor = $(tooltipAnchorSelection.node());
        tooltipAnchor.tooltip({
            animation: false,
            container: "body",
            placement: "auto",
            title: "text",
            trigger: "manual"
        });

        // tooltip value formatter
        function formatTooltipValue(val) {
            if (Number(val) === val) {
                if (val % 1 === 0) {
                    return val;
                }
                return val.toFixed(2);
            }
            return val;
        }

        // Setup Interaction.Pointer
        var pointer = new Plottable.Interactions.Pointer();
        pointer.onPointerMove(function(p) {
            var closest = plot.entityNearest(p);
            if (closest) {
                tooltipAnchor.attr({
                    cx: closest.position.x,
                    cy: closest.position.y,
                    "data-original-title": `${formatTooltipValue(closest.datum[data_key])} ${unit_name}`
                });
                tooltipAnchor.tooltip("show");
            }
        });

        pointer.onPointerExit(function() {
            tooltipAnchor.tooltip("hide");
        });

        pointer.attachTo(plots);
    }

    render() {
        const { chartData } = this.props;
        const { name } = chartData;
        return (
            <svg id={name} />
        )
    }
}
