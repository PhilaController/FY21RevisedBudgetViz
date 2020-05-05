const webpack = require("webpack");

module.exports = {
  chainWebpack: config => {
    config.module.rules.delete("eslint");
  },
  configureWebpack: {
    externals: {
      jquery: "jQuery",
      $: "jQuery"
    },
    entry: {
      main: './src/main.js',
      browserSupport: './src/browserSupport.js'
    },
    output: {
      filename: '[name].[hash:8].bundle.js'
    },
    plugins: [
      new webpack.ProvidePlugin({
        $: "jquery",
        jQuery: "jquery"
      })
    ],
    optimization: {
      splitChunks: false
    },
    module: {
      rules: [
        {
          test: /\.html$/,
          exclude: /node_modules/,
          use: ["html-loader"]
        }
      ]
    }
  },
  css: {
    extract: false
  }
};