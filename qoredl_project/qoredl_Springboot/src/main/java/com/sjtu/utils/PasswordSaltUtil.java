package com.sjtu.utils;

import org.apache.shiro.crypto.hash.SimpleHash;
import org.apache.shiro.util.ByteSource;

import java.util.Random;

public class PasswordSaltUtil {
    private static final Random RANDOM = new Random();
    public static String md5(String password,String salt){
        String hashAlgorithmName = "MD5";
        ByteSource byteSalt = ByteSource.Util.bytes(salt);
        Object source = password;
        int hashIterations = 2;
        SimpleHash result = new SimpleHash(hashAlgorithmName,source,byteSalt,hashIterations);
        return result.toString();
    }

    //生成salt
    public static String randomAlphanumeric(int count) {
        StringBuilder strBuilder = new StringBuilder(count);
        int anLen = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ".length();
        synchronized(RANDOM) {
            for(int i = 0; i < count; ++i) {
                strBuilder.append("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ".charAt(RANDOM.nextInt(anLen)));
            }
            return strBuilder.toString();
        }
    }
}
