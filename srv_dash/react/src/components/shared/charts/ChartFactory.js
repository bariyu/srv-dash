import React from 'react';

import LinearChart from './LinearChart';

export default function renderChart(chartData) {
    switch (chartData.chart_type) {
        case 'linear':
            return <LinearChart chartData={chartData} key={chartData.name} />
        default:
            console.log(`failed to render unknown chart: ${chartData.chart_type}`)
            return null;

    }
}
