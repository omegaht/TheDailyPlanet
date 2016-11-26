var path = require('path');

const PATHS = {
    app: path.join(__dirname, 'app'),
    static: path.join(__dirname, 'static')
}

module.exports = {
    entry: {
        app: PATHS.app
    },
    output: {
        path: PATHS.static,
        publicPath: "/static/",
        filename: "bundle.js"
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    module: {
        loaders: [{
                test: /\.woff|\.woff2|\.svg|.eot|\.ttf/,
                loader: 'url-loader?prefix=font/&limit=10000'
            },
            {
                test: /\.(js|jsx)?$/,
                loader: 'babel-loader',
                query: {
                    presets: ['es2015', 'react']
                },
                exclude: /node_modules/,

            },
            {
                test: /\.css$/,
                loader: 'style!css?sourceMap'
            }
        ]
    },
    plugins: []
};