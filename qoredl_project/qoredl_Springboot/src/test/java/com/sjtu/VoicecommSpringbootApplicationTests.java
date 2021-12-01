package com.sjtu;

import org.jasypt.encryption.StringEncryptor;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;
import org.springframework.core.env.Environment;

@SpringBootTest
class VoicecommSpringbootApplicationTests {


    @Autowired
    private ApplicationContext appCtx;
    @Autowired
    private StringEncryptor PwdEncryptorBean;
    @Test
    public void run() throws Exception {

        Environment environment = appCtx.getBean(Environment.class);

        // 首先获取配置文件里的原始明文信息
        String mysqlOriginPswd = environment.getProperty("spring.mail.username");

        // 加密
        String mysqlEncryptedPswd = encrypt( mysqlOriginPswd );

        // 打印加密前后的结果对比
        System.out.println( "MySQL原始明文密码为：" + mysqlOriginPswd );
        System.out.println( "====================================" );
        System.out.println( "MySQL原始明文密码加密后的结果为：" + mysqlEncryptedPswd );
    }

    private String encrypt( String originPassord ) {
        String encryptStr = PwdEncryptorBean.encrypt( originPassord );
        return encryptStr;
    }

    private String decrypt( String encryptedPassword ) {
        String decryptStr = PwdEncryptorBean.decrypt( encryptedPassword );
        return decryptStr;
    }
}
