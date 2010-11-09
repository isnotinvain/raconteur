// (c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

package com.isnotinvain.raconteur;

import java.io.FileWriter;
import java.io.IOException;

import android.app.Activity;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.widget.TextView;

/***
 * The main Raconteur {@link Activity}
 * This is for now acting as both the service and the user interface
 * Soon it should be seperated into a background Service and 
 * a UI {@link Activity}
 * 
 * The Raconteur Android App records your GPS location data over a period of time and
 * saves it to your external storage device, for import into Raconteur, a lifecasting and
 * self documentation automation tool. Find out more at: http://isnotinvain.com/captainslog/category/raconteur/ 
 * 
 * @author Alex Levenson (alex@isnotinvain.com)
 * 
 */
public class Raconteur extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
		TextView tv = new TextView(this);
		tv.setText("Hello, Android");
		setContentView(tv);
		String state = Environment.getExternalStorageState();

		if (Environment.MEDIA_MOUNTED.equals(state)) {
			try {
				FileWriter writer = new FileWriter(Util.getGPSFile(),true);
				writer.write("Hello, this is a test\n");
				writer.close();
			} catch (IOException e) {
				Log.e("raconteur", "Encountered an error while trying to write to the external storage device", e);
			}
			
		} else {
			Log.e("raconteur", "External storage device not writeable at this time");
		}
	}
}