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
                loaders: ['style', 'css'],
                include: PATHS.app
            }
        ]
    },
    plugins: []
};