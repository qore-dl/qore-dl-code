package com.sjtu.shiro;

import com.alibaba.fastjson.JSONObject;
import com.sjtu.common.StatusCode;
import com.sjtu.entity.User;
import com.sjtu.exception.ServiceException;
import com.sjtu.service.UserService;
import org.apache.shiro.authc.*;
import org.apache.shiro.authc.credential.HashedCredentialsMatcher;
import org.apache.shiro.authz.AuthorizationInfo;
import org.apache.shiro.authz.SimpleAuthorizationInfo;
import org.apache.shiro.realm.AuthorizingRealm;
import org.apache.shiro.subject.PrincipalCollection;
import org.apache.shiro.util.ByteSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;

public class LoginRealm extends AuthorizingRealm {

    @Lazy
    @Autowired
    UserService userService;

    public LoginRealm() {
        this.setCredentialsMatcher(hashedCredentialsMatcher());
    }

    @Override
    public boolean supports(AuthenticationToken token){
        return token instanceof UsernamePasswordToken;
    }

    /*认证*/
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken authenticationToken) throws AuthenticationException {
        UsernamePasswordToken userToken = (UsernamePasswordToken) authenticationToken;
        //判断登录名为邮箱还是用户名
        String LoginName = userToken.getUsername();
        if(LoginName==null){
            throw new ServiceException(StatusCode.NULL_POINTER,"用户名为空");
        }
        User user = new User();
        if(LoginName.contains("@")){
            user = userService.getUserByEmail(LoginName);
        }else {
            user = userService.getUserByName(LoginName);
        }
        if(user==null){
            throw new AuthenticationException("用户不存在");
        }
        if(user.getActivation()==0){
            throw new AuthenticationException("该用户未激活");
        }
        return new SimpleAuthenticationInfo(user,user.getPassword(), ByteSource.Util.bytes(user.getSalt()),getName());
    }

    /*登录验证的匹配方式*/
    public HashedCredentialsMatcher hashedCredentialsMatcher(){
        HashedCredentialsMatcher hashedCredentialsMatcher = new HashedCredentialsMatcher();
        hashedCredentialsMatcher.setHashAlgorithmName("MD5");//散列算法
        hashedCredentialsMatcher.setHashIterations(2);//散列的次数
        return hashedCredentialsMatcher;
    }

    /*授权*/
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principalCollection) {
        SimpleAuthorizationInfo info = new SimpleAuthorizationInfo();
        User user = (User) principalCollection.getPrimaryPrincipal();
        JSONObject auth = user.getAuthority();
        for(String keys : auth.keySet()){
            if((Boolean) auth.get(keys)){
                info.addStringPermission(user.getRole() + ":" + keys);
            }
        }
        return info;
    }
}
