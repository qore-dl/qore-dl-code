import axios from 'axios'
import router from "@/router";
import { Message } from 'element-ui';


const request = axios.create({
	baseURL:"",
    timeout: 5000
})


// request 拦截器
// 可以自请求发送前对请求做一些处理
// 比如统一加token，对请求参数统一加密
request.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/json;charset=utf-8';

	if (localStorage.getItem('Token')) {
		config.headers.Token= localStorage.getItem('Token');

	}

    return config
}, error => {
    return Promise.reject(error)
});


// response 拦截器
// 可以在接口响应后统一处理结果
request.interceptors.response.use(
    response => {
		
        let res = response.data;

		if(res.code=="403"){
            Message.error("登录过期");
            localStorage.removeItem('Token');
			window.location.href="/login";
		}

		const token=response.headers.token;
		if(token){
            localStorage.setItem('Token', token);
        }

        // 如果是返回的文件
        if (response.config.responseType === 'blob') {
            return res
        }
        // 兼容服务端返回的字符串数据
        if (typeof res === 'string') {
            res = res ? JSON.parse(res) : res
        }
        return res;
    },
    error => {
        console.log('err' + error) // for debug
        return Promise.reject(error)
    }
)


export default request

