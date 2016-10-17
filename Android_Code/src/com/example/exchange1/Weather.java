package com.example.exchange1;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;
import org.json.JSONException;
import org.json.JSONObject;

public class Weather {

	public static String query(String url) {
		HttpGet request = new HttpGet(url);

		String result = null;
		try {
			HttpResponse response = new DefaultHttpClient().execute(request);
			if (response.getStatusLine().getStatusCode() == 200) {
				result = EntityUtils.toString(response.getEntity(), HTTP.UTF_8);
				return result;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return result;
	}

	public static String decode(String weatherJson) {
		String result = "";
		JSONObject jsonObject;
		try {
			jsonObject = new JSONObject(weatherJson);
			JSONObject weatherObject = jsonObject.getJSONObject("weatherinfo");
			result ="你好～今天"+ weatherObject.getString("city")+"的气温是"
					+ weatherObject.getString("temp2")+"--"
					+ weatherObject.getString("temp1")+"\n天气"
					+ weatherObject.getString("weather");
		} catch (JSONException e) {
			e.printStackTrace();
		}
		return result;

	}
}
