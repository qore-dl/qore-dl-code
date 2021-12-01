package com.sjtu.config;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Data
@Component
public class EmailConfig {
    @Value("${spring.mail.username}")
    private String EmailFrom;
}
