package com.example.exchange1;

import java.io.InputStream;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONObject;

import android.util.Log;

public class LacationConvert{

	// 发送post请求
	// 输出：返回location的string格式
	public static String post(double latitude, double longtitude) {
		String result = "";

		String url = "http://api.map.baidu.com/geocoder/v2/?ak=soWzrkuTpplPBw6qSL5REy7w&callback=renderReverse&"
				+ "location="
				+ latitude
				+ ","
				+ longtitude
				+ "&output=json&pois=0";
		HttpClient client = new DefaultHttpClient();
		HttpGet httpGet = new HttpGet(url);
		StringBuilder sb = new StringBuilder();

		try {

			HttpResponse response = client.execute(httpGet);

			HttpEntity entity = response.getEntity();

			InputStream stream = entity.getContent();

			int len = 0;
			byte[] b = new byte[1024];
			while (-1 != (len = stream.read(b, 0, b.length))) {
				sb.append(new String(b, 0, len));
			}

			String temp = sb.toString().substring(
					"renderReverse&&renderReverse(".length(),
					sb.toString().length() - 1);

			JSONObject jsonObj = new JSONObject(temp);
			Log.d("test1", temp);
			//result = jsonObj.getJSONObject("result").getString("formatted_address");
			temp = jsonObj.getJSONObject("result").getString("addressComponent");
			jsonObj = new JSONObject(temp);
			temp = jsonObj.getString("city");
			result = temp.substring(0, temp.length()-1);
			
		} catch (Exception e) {
			e.printStackTrace();
		}
		return result;
	}
}
