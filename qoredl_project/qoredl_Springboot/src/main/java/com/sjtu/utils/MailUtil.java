package com.sjtu.utils;

import com.sjtu.config.EmailConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSenderImpl;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;
import java.util.Random;


@Component
public class MailUtil {
    @Autowired
    JavaMailSenderImpl mailSender;
    @Autowired
    EmailConfig emailConfig;

    private static final Random RANDOM = new Random();

    /*简单邮件的发送*/
    public void sendSimpleMail(String sender, String title, String content) {
        SimpleMailMessage mailMessage = new SimpleMailMessage();
        mailMessage.setSubject(title);
        mailMessage.setText(content);
        mailMessage.setTo(sender);
        mailMessage.setFrom(emailConfig.getEmailFrom());
        mailSender.send(mailMessage);
    }

    /*复杂邮件的发送*/
    @Async("threadPoolTaskExecutor")
    public void sendMimeMail(String sender, String title, String content) throws MessagingException {
        MimeMessage mimeMessage = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(mimeMessage);
        helper.setFrom(emailConfig.getEmailFrom());
        helper.setSubject(title);
        helper.setText(content,true);
        helper.setTo(sender);
        mailSender.send(mimeMessage);
    }

    /*创建验证码*/
    public String create_code(int count) {
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
