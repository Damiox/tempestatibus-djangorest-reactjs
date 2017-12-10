const webpack = require('webpack');
const path = require('path');
const BundleTracker = require('webpack-bundle-tracker')

const config = {

    entry: {
	App: path.resolve('./client/index.js')
    },

    output: {
        path: path.resolve('./tempestatibus/static/bundles'),
        filename: 'bundle-[hash].js'
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
    ],

    module: {
        rules: [
            {
                test: /.js$/,
                loader: 'babel-loader'
            }
        ]
    },

    devServer: {
        contentBase: path.join(__dirname, "dist"),
        compress: true,
        port: 9000
    }

};

module.exports = config;
