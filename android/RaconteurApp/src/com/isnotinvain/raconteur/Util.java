// (c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

package com.isnotinvain.raconteur;

import java.io.File;
import java.io.IOException;

import android.os.Environment;

/*** 
 * Static utility functions
 * 
 * @author Alex Levenson (alex@isnotinvain.com)
 * 
 */
public final class Util {
	private static final String GPS_FILE = "gps_data.yaml";
	private static final String BOOKMARKS_FILE = "bookmarks_data.yaml";
	private static final String RACONTEUR_DIRECTORY_ERROR = "Could not make the raconteur directory on external storage device";
	
	public static final File getGPSFile() throws IOException{
		return getRaconteurFile(GPS_FILE);
	}
	
	public static final File getBookmarksFile() throws IOException{
		return getRaconteurFile(BOOKMARKS_FILE);
	}
	
	private static final File getRaconteurFile(String file) throws IOException {
		File sdRoot = Environment.getExternalStorageDirectory();
		File raconteurDir = new File(sdRoot,"raconteur");
		if(!raconteurDir.exists()) {
			if(!raconteurDir.mkdir()) {
				throw new IOException(RACONTEUR_DIRECTORY_ERROR);
			}
		}
		File f = new File(raconteurDir,file);
		if(!f.exists()) {
			f.createNewFile();
		}
		return f;	   
	}
}
