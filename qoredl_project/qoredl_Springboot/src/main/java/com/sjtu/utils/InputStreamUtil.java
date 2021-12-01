package com.sjtu.utils;

import org.springframework.core.io.InputStreamResource;

import java.io.IOException;
import java.io.InputStream;

public class InputStreamUtil extends InputStreamResource {
    private long length;
    private String fileName;

    public InputStreamUtil(InputStream inputStream, long length, String fileName) {
        super(inputStream);
        this.length = length;
        this.fileName = fileName;
    }

    @Override
    public long contentLength() throws IOException {
        long estimate = length;
        return estimate==0?1:estimate;
    }

    @Override
    public String getFilename() {
        return fileName;
    }

    public void setLength(long length) {
        this.length = length;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }
}
