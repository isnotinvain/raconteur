// (c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

package com.isnotinvain.raconteur;

import java.text.SimpleDateFormat;
import java.util.Date;

import org.yaml.snakeyaml.Yaml;

/*** 
 * A manually created bookmark.
 * For now it is pretty much just a time stamp with a caption,
 * more meta data may come later though
 * 
 * @author Alex Levenson (alex@isnotinvain.com)
 * 
 */
public class Bookmark {	
	private Date begin;
	private String caption;
	SimpleDateFormat iso8601Formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
	
	public String toYaml() {
		StringBuilder s = new StringBuilder();
		s.append("!!map {!!timestamp ");        
        s.append(iso8601Formatter.format(begin));
        s.append(" : !!str ");
		s.append(caption);
		s.append("}");
		return s.toString();
	}
	
	public Bookmark(String caption) {
		this(new Date(),caption);
	}
	
	public Bookmark(Date begin, String caption) {
		this.begin = begin;
		this.caption = caption;
	}
	
	public Date getBegin() {
		return begin;
	}

	public void setBegin(Date begin) {
		this.begin = begin;
	}

	public String getCaption() {
		return caption;
	}

	public void setCaption(String caption) {
		this.caption = caption;
	}
}
