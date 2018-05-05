package com.example.zeljko.ezclient;

import android.os.AsyncTask;
import android.util.Log;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

public class MessageSender extends AsyncTask<String,Void,String> {
    @Override
    protected String doInBackground(String... params) {

        String message = params[0];
        try {
            Log.d("toServer", message);
            Socket mySocket = new Socket("192.168.100.15",8888);
            DataOutputStream dos = new DataOutputStream(mySocket.getOutputStream());
            dos.writeUTF(message);
            dos.close();
            mySocket.close();

        } catch(IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}