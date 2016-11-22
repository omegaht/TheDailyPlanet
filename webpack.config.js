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
        filename: "bundle.js"
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    module: {
        loaders: [{
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
            }, {
                test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,
                loader: "url?limit=10000&mimetype=application/font-woff"
            }, {
                test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,
                loader: "url?limit=10000&mimetype=application/font-woff"
            }, {
                test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
                loader: "url?limit=10000&mimetype=application/octet-stream"
            }, {
                test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
                loader: "file"
            }, {
                test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
                loader: "url?limit=10000&mimetype=image/svg+xml"
            }, {
                test: /\.png$/,
                loader: 'url-loader?limit=100000'
            },
            {
                test: /\.jpg$/,
                loader: 'file-loader'
            }


            // {
            //     test: /\.css$/,
            //     loaders: ['style', 'css'],
            //     include: PATHS.app
            // },
            // {
            //     test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,
            //     loader: "url?limit=10000&mimetype=application/font-woff"
            // }, {
            //     test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,
            //     loader: "url?limit=10000&mimetype=application/font-woff"
            // }, {
            //     test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
            //     loader: "url?limit=10000&mimetype=application/octet-stream"
            // }, {
            //     test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
            //     loader: "file"
            // }, {
            //     test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
            //     loader: "url?limit=10000&mimetype=image/svg+xml"
            // }
        ]
    },
    plugins: []
};