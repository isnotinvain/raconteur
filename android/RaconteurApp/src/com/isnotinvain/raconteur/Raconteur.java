// (c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

package com.isnotinvain.raconteur;

import java.io.IOException;

import android.app.Activity;
import android.content.Context;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
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
	private TextView captionBox; 
	// Acquire a reference to the system Location Manager
	LocationManager locationManager;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        setupLocationListener();
        
        buildUi();
	}
    
    private void setupLocationListener() {
		locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
		LocationListener listener = new LocationListener() {

			public void onLocationChanged(Location location) {
				recordGps(location);
			}

			public void onProviderDisabled(String provider) {

			}

			public void onProviderEnabled(String provider) {
				
			}

			public void onStatusChanged(String provider, int status,
					Bundle extras) {
				
			}
			
		};
		locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, listener);
    }
    
    private void recordGps(Location location) {
    	StringBuilder msg = new StringBuilder();
    	msg.append("Recording gps location:\n")
	    	.append("\tLongitude: ")
	    	.append(location.getLongitude())
	    	.append("\n\tLatitude: ")
	    	.append(location.getLatitude())
	    	.append("\n\tAltitude: ")
	    	.append(location.getAltitude())
	    	.append("\n");
    	
    	if(location.hasAccuracy()) {
    		msg.append("\tAccuracy: ")
    			.append(location.getAccuracy())
    			.append("\n");
    	}
    	
    	Log.v("raconteur",msg.toString());
    }
    
    private void recordBookmark() {
    	Log.v("raconteur","recording bookmark...");
    	Bookmark b = new Bookmark(captionBox.getText().toString());    	
    	
		try {
			Util.writeToExternalStorage(Util.getBookmarksFile(), b.toYaml()+"\n");
		} catch (IOException e) {
			// TODO: Alert the user that there was a problem
			Log.e("raconteur","Could not write bookmark to external storage",e);
		}		
		captionBox.setText("");
    }
    
    private void buildUi() {
    	LinearLayout content = new LinearLayout(this);
		content.setOrientation(LinearLayout.VERTICAL);
        
		Button setBookmark = new Button(this);
		setBookmark.setText("Set a Bookmark!");
		setBookmark.setOnClickListener(new View.OnClickListener() {			
			public void onClick(View v) {
				recordBookmark();
			}
		});
		captionBox = new EditText(this);		
		captionBox.setHint("Enter a caption for the bookmark");
		
		content.addView(setBookmark);
		content.addView(captionBox);
		
		setContentView(content);
    }
}