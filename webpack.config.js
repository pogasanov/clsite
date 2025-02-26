const path = require('path');
const webpack = require("webpack");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MomentLocalesPlugin = require('moment-locales-webpack-plugin');

module.exports = [
    {
        name: 'app',
        mode: 'development',
        entry: './src/entry.js',
        devtool: 'eval-source-map',
        output: {
            filename: './js/main.js',
            path: path.resolve(__dirname, 'app/clsite/static')
        },
        resolve: {
            alias: {
                '@': path.resolve(__dirname, 'src/js/')
            }
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: './css/[name].css',
                chunkFilename: './css/[id].css',
            }),
            new VueLoaderPlugin(),
            new MomentLocalesPlugin(),
        ],
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    loader: 'vue-loader',
                    options: {
                        loaders: {}
                        // other vue-loader options go here
                    }
                },
                {
                    test: /\.js$/,
                    loader: 'babel-loader',
                    exclude: /node_modules/
                },
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
                                publicPath: '../img'
                            },
                        }
                    ]
                },
                {
                    test: /\.(woff|woff2|eot|ttf)$/,
                    use: [
                        {
                            loader: 'file-loader',
                            options: {
                                name: '[name].[ext]',
                                outputPath: 'fonts',
                                publicPath: '../fonts'
                            },
                        }
                    ]
                },
            ]
        }
    },
    {
        name: 'old',
        mode: 'production',
        entry: './src/entry-old.js',
        output: {
            filename: 'main.js',
            path: path.resolve(__dirname, 'app/clsite/static/old')
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
                                publicPath: '/static/old/img'
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
    }];