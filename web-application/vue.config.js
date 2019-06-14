const path = require('path')
function resolve(dir) {
  return path.join(__dirname, dir)
}

module.exports = {
  devServer: {
    port: 60000,
    proxy: {
      '/api': {
        target: 'http://localhost:9200',
        changeOrigin: true,
        ws: true,
        pathRewrite:{
          "^/api": ''
        }
      }
    }
  }
}