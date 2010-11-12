// (c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

package com.isnotinvain.raconteur;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import android.os.Environment;
import android.util.Log;

/*** 
 * Static utility functions
 * 
 * @author Alex Levenson (alex@isnotinvain.com)
 * 
 */
public final class Util {
	private static final String GPS_FILE = "gps_data.yaml";
	private static final String BOOKMARKS_FILE = "bookmarks_data.yaml";
	private static final String DIRECTORY_ERROR = "Could not make the directory '%s' on external storage device";
	private static final String RACONTEUR = "raconteur";
	
	/**
	 * @return the file on the external storage where gps data is stored 
	 * @throws IOException
	 */
	public static final File getGpsFile() throws IOException{
		return getExternalStorageFile(RACONTEUR,GPS_FILE);
	}
	
	/**
	 * @return the file on the external storage where bookmarks data is stored 
	 * @throws IOException
	 */
	public static final File getBookmarksFile() throws IOException{
		return getExternalStorageFile(RACONTEUR,BOOKMARKS_FILE);
	}
	
	/**
	 * Appends string s to file f	 
	 * @throws IOException
	 */
	public static final void writeToExternalStorage(File f, String s) throws IOException {
		writeToExternalStorage(f,s,true);
	}
	
	/**
	 * Writes String s to File f
	 * @param append whether to append s to f 
	 * @throws IOException
	 */
	public static final void writeToExternalStorage(File f, String s, boolean append) throws IOException {
		String state = Environment.getExternalStorageState();
		if (Environment.MEDIA_MOUNTED.equals(state)) {
			// sd card is readable and writable!
			try {
				FileWriter writer = new FileWriter(f,true);
				writer.write(s);
				writer.close();
			} catch (IOException e) {
				Log.e("raconteur", "Encountered an error while trying to write to the external storage device", e);
				throw e;
			}			
		} else {
			throw new IOException("External storage device not writeable at this time");
		}
	}
	
	/**
	 * Safely acquires a {@link File} object that points to the file
	 * /<directory>/<fileName> on the external storage device,
	 * creating directory and fileName if they do not exist
	 * 
	 * @return a File object that points to /<directory>/<fileName> on the external storage device
	 * @throws IOException if directory does not exist and cannot be created
	 */
	private static final File getExternalStorageFile(String directory, String fileName) throws IOException {
		File sdRoot = Environment.getExternalStorageDirectory();		
		File raconteurDir = new File(sdRoot,directory);
		if(!raconteurDir.exists()) {
			if(!raconteurDir.mkdir()) {
				throw new IOException(String.format(DIRECTORY_ERROR,directory));
			}
		}
		File f = new File(raconteurDir,fileName);
		if(!f.exists()) {
			f.createNewFile();
		}
		return f;
	}
}
