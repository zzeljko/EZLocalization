package com.example.zeljko.ezclient;

import android.content.Context;
import android.os.AsyncTask;
import android.renderscript.ScriptGroup;
import android.util.Log;
import android.widget.Toast;

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
    private static boolean transmissionFinished = true;
    private IOnEZUpdate ezCallback;
    private String latitude;
    private String longitude;

    public MessageSender(IOnEZUpdate ezCallback) {
        this.ezCallback = ezCallback;
    }

    @Override
    protected String doInBackground(String... params) {

        String message = params[0];
        String messageType = params[1];
        while (!transmissionFinished);
        transmissionFinished = false;
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
            String msg = "";
            while (true) {
                int ch = bufferedReader.read();
                msg += (char)ch;
                if (ch == '\n')
                    break;
            }
            Log.d("msg", msg);
            bufferedWriter.write(message);
            bufferedWriter.flush();

            msg = "";
            while (true) {
                int ch = bufferedReader.read();
                msg += (char)ch;
                if (ch == '\n')
                    break;
            }
            Log.d("lat", msg + "");

            String latitude = "";
            while (true) {
                int ch = bufferedReader.read();
                latitude += (char)ch;
                if (ch == '\n')
                    break;
            }
            Log.d("lat", latitude + "");
            bufferedWriter.write("ACK");
            bufferedWriter.flush();

            String longitude = "";
            while (true) {
                int ch = bufferedReader.read();
                longitude += (char)ch;
                if (ch == '\n')
                    break;
            }
            Log.d("long", longitude + "");
            this.latitude = latitude;
            this.longitude = longitude;
            bufferedWriter.write("ACK");
            bufferedWriter.flush();
//            float latitude = Float.parseFloat(bufferedReader.readLine());
//            bufferedWriter.write("ACK");
//            bufferedWriter.flush();

//            float longitude = Float.parseFloat(bufferedReader.readLine());
//            bufferedWriter.write("ACK");
//            bufferedWriter.flush();
//            Log.d("lat", latitude + "");
            inputStream.close();
            dos.close();
            mySocket.close();

        } catch(IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(String s) {
        transmissionFinished = true;
        ezCallback.onEZUpdateCallback(latitude, longitude);
    }
}