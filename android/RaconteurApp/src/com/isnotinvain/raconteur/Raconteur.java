// (c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

package com.isnotinvain.raconteur;

import java.io.IOException;

import android.app.Activity;
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
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
		
        buildUi();
	}
    
    private void recordGps() {
    	Log.v("raconteur","recording gps...");    	
    }
    
    private void recordBookmark() {
    	Log.v("raconteur","recording bookmark...");
    	Bookmark b = new Bookmark(captionBox.getText().toString());    	
    	
		try {
			Util.writeToExternalStorage(Util.getBookmarksFile(), b.toYaml()+"\n");
		} catch (IOException e) {
			Log.e("raconteur","Could not write bookmark to external storage",e);
		}
    }
    
    private void buildUi() {
    	LinearLayout content = new LinearLayout(this);
		content.setOrientation(LinearLayout.VERTICAL);
		
		Button recordGps = new Button(this);
		recordGps.setText("Record my Location!");
		recordGps.setOnClickListener(new View.OnClickListener() {			
			public void onClick(View v) {
				recordGps();
			}
		});
        
		Button setBookmark = new Button(this);
		setBookmark.setText("Set a Bookmark!");
		setBookmark.setOnClickListener(new View.OnClickListener() {			
			public void onClick(View v) {
				recordBookmark();
			}
		});
		TextView captionLabel = new TextView(this);
		captionLabel.setText("Enter a caption for the bookmark:");
		captionBox = new EditText(this);		
		
		content.addView(recordGps);
		content.addView(captionLabel);
		content.addView(captionBox);
		content.addView(setBookmark);
		
		setContentView(content);
    }
}