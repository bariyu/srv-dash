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

        var plotNames = [];

        for (var i = 0; i < series.length; i++) {
            var plot = new Plottable.Plots.Line()
                .addDataset(new Plottable.Dataset(series[i].data))
                .x(function(d) { return new Date(d.time); }, xScale)
                .y(function(d) { return d[data_key]; }, yScale)
                .attr("stroke", colorScale.scale(series[i].name))
                .attr("stroke-width", 1);

            plots.append(plot);
            plotNames.push(series[i].name);
        }

        chart.renderTo(`svg#${name}`);

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

        function pointDistance(p1, p2) {
            var xDist = p1.x - p2.x;
            var yDist = p1.y - p2.y;
            return xDist * xDist + yDist * yDist;
        }

        var pointer = new Plottable.Interactions.Pointer();
        pointer.onPointerMove(function(p) {
            // go through all components in plot group and find the closest point to draw the tooltip
            var closests = plots.components().map(function(plot, idx) {
                return plot.entityNearest(p);
            })
            var closest;
            var closestIdx;
            var closestDist = Infinity;
            for (var i = 0; i < closests.length; i++) {
                var curPoint = closests[i];
                if (!curPoint) {
                    continue;
                }
                var distance = pointDistance(p, curPoint.position);
                if (distance < closestDist) {
                    closest = closests[i];
                    closestIdx = i;
                    closestDist = distance;
                }
            }
            if (closest) {
                var closestSerieNameLabel = '';
                if (plotNames[closestIdx] !== name) { // show only if serie containes more than one series
                    closestSerieNameLabel = `(${plotNames[closestIdx]})`;
                }
                tooltipAnchor.attr({
                    cx: closest.position.x,
                    cy: closest.position.y,
                    "data-original-title": `${formatTooltipValue(closest.datum[data_key])} ${unit_name} ${closestSerieNameLabel}`
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
