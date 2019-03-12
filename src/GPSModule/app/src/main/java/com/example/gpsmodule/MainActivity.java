package com.example.gpsmodule;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import com.jcraft.jsch.*;


public class MainActivity extends AppCompatActivity {

    Button button;
    TextView textv;
    EditText editt;
    LocationManager locationManager;
    LocationListener listener;
    Double lat, longt;
    String lats, longts, ip;
    String server_url = "https://192.168.43.188/update_info.php";


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);

        textv = (TextView) findViewById(R.id.textView);
        button = (Button) findViewById(R.id.button);
        editt = (EditText) findViewById(R.id.editText);


        listener = new LocationListener() {
            @Override
            public void onLocationChanged(Location location) {
                lat = location.getLatitude();
                longt = location.getLongitude();
                lats = lat.toString();
                longts = longt.toString();
                textv.append("\n " + longts + " " + lats);
                ip = editt.getText().toString();
                sen(lats, longts, ip);
            }

            @Override
            public void onStatusChanged(String s, int i, Bundle bundle) {

            }

            @Override
            public void onProviderEnabled(String s) {

            }

            @Override
            public void onProviderDisabled(String s) {

                Intent i = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
                startActivity(i);
            }
        };
        init();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        if (requestCode == 10) {
            init();
        }
    }

    public void sen(final String lat, final String longt, final String ip) {
        new AsyncTask<Integer, Void, Void>() {

            @Override
            protected Void doInBackground(Integer... integers) {
                try {
                    executeSsh(lat, longt, ip);
                } catch (Exception e0) {
                    e0.printStackTrace();
                }
                return null;
            }
        }.execute(1);
    }

    public void executeSsh(String lat, String longt, String ip) {
        try {

            String host = ip;
            String user = "hunter";
            String pass = "testpwd1234@";

            java.util.Properties config = new java.util.Properties();
            config.put("StrictHostKeyChecking", "no");

            JSch jsch = new JSch();
            Session session = jsch.getSession(user, host, 22);
            session.setPassword(pass);
            session.setConfig(config);

            session.connect(3000);

            ChannelExec channel = (ChannelExec) session.openChannel("exec");
            String str1 = "cd /home/hunter/Desktop/gps;echo " + lat + " " + longt + " > gpsdata.txt";

            channel.setCommand(str1);
            channel.connect();
            channel.disconnect();
        } catch (Exception e) {

        }

    }

    void init() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                requestPermissions(new String[]{Manifest.permission.ACCESS_COARSE_LOCATION, Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.INTERNET}
                        , 10);
            }
            return;
        }

        button.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {

                locationManager.requestLocationUpdates("gps", 1000, 0, listener);
            }
        });
    }
}