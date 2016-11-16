var webpack = require('webpack');
var CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: './src/index.js',
    output: { path: '../static/js', filename: 'bundle.js' },
    module: {
        loaders: [
            {
                test: /.jsx?$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    presets: ['es2015', 'react']
                }
            },
        ]
    },
    plugins: [
        new CopyWebpackPlugin([
            {
                from: './node_modules/@blueprintjs/core/dist/blueprint.css',
                to: '../css/blueprint.css'
            },
            {
                from: './node_modules/@blueprintjs/core/dist/assets/',
                to: '../css/assets/'
            },
        ]),
    ],
    devtool: 'source-map',
};
