package com.sjtu.shiro;

import org.apache.shiro.authc.AuthenticationToken;

/*
 * Description
 */
public class JwtToken implements AuthenticationToken {

    private String token;
    JwtToken(String token) {
        this.token = token;
    }

    @Override
    public Object getPrincipal() {
        return token;
    }

    @Override
    public Object getCredentials() {
        return token;
    }
}
