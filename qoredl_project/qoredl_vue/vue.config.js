// 跨域配置
module.exports = {
    devServer: {                //记住，别写错了devServer//设置本地默认端口  选填
        port: 8080,
        proxy: {                 //设置代理，必须填
            '/api': {              //设置拦截器  拦截器格式   斜杠+拦截器名字，名字可以自己定 变成
                target: 'http://localhost:9091',     //代理的目标地址
                changeOrigin: true,              //是否设置同源，输入是的
                pathRewrite: {                   //路径重写
                    '/api': ''                     //选择忽略拦截器里面的单词
                }
            },
            '/flask': {              //设置拦截器  拦截器格式   斜杠+拦截器名字，名字可以自己定 变成
                target: 'http://172.16.20.190:15000',     //代理的目标地址
                changeOrigin: true,              //是否设置同源，输入是的
                pathRewrite: {                   //路径重写
                    '/flask': ''                     //选择忽略拦截器里面的单词
                }
            },
        }
    },

}


