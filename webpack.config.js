const path = require('path');
const webpack = require("webpack");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = [
    {
        name: 'app',
        mode: 'production',
        entry: './src/index.js',
        output: {
            filename: 'main.js',
            path: path.resolve(__dirname, 'app/clsite/static')
        },
        plugins: [
            new webpack.ProvidePlugin({
                $: 'jquery',
                jQuery: 'jquery',
                'window.jQuery': 'jquery',
                Popper: ['popper.js', 'default']
            }),
            new MiniCssExtractPlugin({
                filename: '[name].css',
                chunkFilename: '[id].css',
            }),
        ],
        module: {
            rules: [
                {
                    test: /\.(sa|sc|c)ss$/,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                        },
                        'css-loader',
                        'postcss-loader',
                        'sass-loader'
                    ],
                },
                {
                    test: /\.(png|svg|jpg|gif)$/,
                    use: [
                        {
                            loader: 'file-loader',
                            options: {
                                name: '[name].[ext]',
                                outputPath: 'img',
                                publicPath: '/static/img'
                            },
                        }
                    ]
                },
                {
                    test: require.resolve('jquery'),
                    use: [
                        {
                            loader: 'expose-loader',
                            options: 'jQuery'
                        },
                        {
                            loader: 'expose-loader',
                            options: '$'
                        }
                    ]
                }
            ]
        }
    }, {
        name: 'design',
        mode: 'development',
        entry: './src/design.js',
        output: {
            filename: 'main.js',
            path: path.resolve(__dirname, 'design/js')
        },
        module: {
            rules: [
                {
                    test: /\.css$/,
                    use: [{loader: 'style-loader'}, {loader: 'css-loader'}]
                }
            ]
        }
    }];