package com.sjtu.utils;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTDecodeException;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.auth0.jwt.interfaces.JWTVerifier;
import com.sjtu.common.Constant;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/*
 * JWT工具类
 *
 * 标准中注册的声明
 * iss: jwt签发者
 * sub: jwt所面向的用户
 * aud: 接收jwt的一方
 * exp: jwt的过期时间，这个过期时间必须要大于签发时间
 * nbf: 定义在什么时间之前，该jwt都是不可用的.
 * iat: jwt的签发时间
 * jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。
 */
public class JwtUtil {

	/** 服务端的私钥secret,在任何场景都不应该流露出去 */
	private static final String TOKEN_SECRET = "shushkuujn7899jji2jkkljs6gujk9";
	/*
	 * 生成签名，30分钟过期
	 * @param **User**
	 * @param **password**
	 * @return
	 */
	public static String createToken(String user_id, String currentTimeMillis) {
	    try {
	        // 设置过期时间
	        Date date = new Date(System.currentTimeMillis() + Constant.ACCESS_EXPIRE_TIME);
	        // 用户名加私钥加密
			String secret = user_id + TOKEN_SECRET;
	        Algorithm algorithm = Algorithm.HMAC256(secret);
	        // 设置头部信息
	        Map<String, Object> header = new HashMap<>(2);
	        header.put("typ", "JWT");
	        header.put("alg", "HS256");
	        // 返回token字符串
	        return JWT.create()
	                .withHeader(header)
	                .withClaim(Constant.ID, user_id)
					.withClaim(Constant.CURRENT_TIME_MILLIS,currentTimeMillis)
	                .withExpiresAt(date)
	                .sign(algorithm);
	    } catch (Exception e) {
	        e.printStackTrace();
	        return null;
	    }
	}

	/*检验token的正确性*/
	public static boolean verify(String token, String user_id){
	    try {
	    	//用户名+私钥解密
			String secret = user_id + TOKEN_SECRET;
	        Algorithm algorithm = Algorithm.HMAC256(secret);
	        JWTVerifier verifier = JWT.require(algorithm)
					.withClaim(Constant.ID, user_id)
					.build();
	        verifier.verify(token);
	        return true;
	    } catch (Exception e){
	        return false;
	    }
	}

	public static String getClaim(String token, String claim) {
		try {
			DecodedJWT jwt = JWT.decode(token);
			// 只能输出String类型，如果是其他类型返回null
			return jwt.getClaim(claim).asString();
		} catch (JWTDecodeException e) {
			throw new JWTDecodeException("解析错误");
		}
	}
}
