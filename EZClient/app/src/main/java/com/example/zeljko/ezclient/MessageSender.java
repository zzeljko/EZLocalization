package com.example.zeljko.ezclient;

import android.os.AsyncTask;
import android.renderscript.ScriptGroup;
import android.util.Log;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;

public class MessageSender extends AsyncTask<String,Void,String> {

    private static final String host = "192.168.100.15";

    @Override
    protected String doInBackground(String... params) {

        String message = params[0];
        String messageType = params[1];
        try {
            Socket mySocket = new Socket(host,8888);

            InputStream inputStream = mySocket.getInputStream();
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);

            OutputStream dos = mySocket.getOutputStream();
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(dos);
            BufferedWriter bufferedWriter = new BufferedWriter(outputStreamWriter);

            Log.d("messageType", messageType);
            bufferedWriter.write(messageType);
            bufferedWriter.flush();
            bufferedReader.read();
            bufferedWriter.write(message);
            bufferedWriter.flush();

            inputStream.close();
            dos.close();
            mySocket.close();

        } catch(IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}