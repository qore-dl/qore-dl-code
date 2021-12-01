package com.sjtu.common;

import lombok.Data;

@Data
public class Response {
    private String code;
    private String msg;
    private Object data;

    public Response() {
    }

    public Response(String code, String msg, Object data) {
        this.code = code;
        this.msg = msg;
        this.data = data;
    }

    public Response(String code, String msg) {
        this.code = code;
        this.msg = msg;
    }
}
