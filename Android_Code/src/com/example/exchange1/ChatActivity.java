package com.example.exchange1;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

public class ChatActivity extends Activity {

	Handler handler;
	private ListView talkView;
	private Button messageButton;
	private EditText messageText;
	private ArrayList<ChatMessage> list = new ArrayList<ChatMessage>();
	private String msgType;
	private String eventkey;
	private String event;
	static String toUser = "EXgood";
	String fromUser = null;
	LocationManager locationManager = null;
	String provider = null;
	Location location = null;
	double longtitude = 360;
	double latitude = 360;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		talkView = (ListView) findViewById(R.id.list);
		messageButton = (Button) findViewById(R.id.MessageButton);
		messageText = (EditText) findViewById(R.id.MessageText);
		fromUser = xml.getFromUser();
		Log.i("xiangxiyun", "chat");
		// 更新结果显示
		handler = new Handler() {
			@Override
			
			public void handleMessage(Message msg) {
				Bundle b = msg.getData();
				String re = b.getString("result");
				// he
				int RIdB = R.layout.list_say_me_item;
				String date = getDate();
				ChatMessage backMsg = new ChatMessage(date, re, RIdB);
				list.add(backMsg);
				talkView.setAdapter(new ChattingAdapter(ChatActivity.this, list));

			}
		};
		init();

		chat();
	}

	private void init() {
		Log.i("xiangxiyun", "init");
		locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
		provider = LocationManager.NETWORK_PROVIDER;
		location = locationManager.getLastKnownLocation(provider);

		latitude = location.getLatitude();
		longtitude = location.getLongitude();

		new Thread(new DownLoadLocation(longtitude, latitude)).start();

		msgType = "hint";
		// xml编码
		String xmlS = xml.encode(toUser, fromUser, msgType, null, null, null,
				null, null, null, null, null, null, null, null, null)
				.toString();
		Log.i("xiangxiyun", xmlS);
		// 启动网络访问
		new Thread(new DownLoadQuery(xmlS)).start();
	}

	private void chat() {

		messageButton.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				// me
				msgType = "text";
				String date = getDate();
				String msgText = getText();
				int RIdA = R.layout.list_say_he_item;
				ChatMessage newMsg = new ChatMessage(date, msgText, RIdA);
				messageText.setText("");
				list.add(newMsg);
				// xml编码
				String xmlS;
				xmlS = xml.encode(toUser, fromUser, msgType, msgText, null,
						null, null, null, null, null, null, null, null, null,
						null).toString();
				// 启动网络访问
				new Thread(new DownLoadThread(xmlS)).start();
			}
		});

	}

	class DownLoadLocation implements Runnable {
		private double longtitude;
		private double latitude;

		public DownLoadLocation(double lon, double lat) {
			longtitude = lon;
			latitude = lat;
			Log.i("Heidi", "initThread");
		}

		@Override
		public void run() {
			// Log.i("Heidi", "runThread");
			Bundle b = new Bundle();
			// Log.i("Heidi", "Bundle");
			Message msg = handler.obtainMessage();
			Log.i("Heidi", "msg");
			// String cityName = LacationConvert.post(latitude, longtitude);
			// TODO:City name
			String cityCode = "101280701";
			String weatherUrl = "http://www.weather.com.cn/data/cityinfo/"
					+ cityCode + ".html";
			String re = Weather.query(weatherUrl);
			re = Weather.decode(re);
			// Log.i("Heidi", re);
			b.putString("result", re);
			msg.setData(b);
			handler.sendMessage(msg);
		}
	}

	class DownLoadThread implements Runnable {
		private String con;

		@Override
		public void run() {
			Bundle b = new Bundle();
			Message msg = handler.obtainMessage();
			String xmlS = xml.post(con); // post
			String decMsg = xml.decode(xmlS);
			b.putString("result", decMsg);
			Log.i("Hint", decMsg);
			msg.setData(b);
			handler.sendMessage(msg);
		}

		public DownLoadThread(String content) {
			con = content;
		}
	}

	class DownLoadQuery implements Runnable {
		private String con;

		@Override
		public void run() {
			Bundle b = new Bundle();
			Message msg = handler.obtainMessage();
			String xmlS = xml.post(con); // post
			String decMsg = xml.decode(xmlS);
			String[] re = xml.getgoodsstate(decMsg);
			if(re[0].equals("N")){
				b.putString("result", "亲，没有新订单状态～～");
			} else{
				b.putString("result", "亲，请往个人中心查看新订单状态～～");
			}
			
			Log.i("Hint", decMsg);
			msg.setData(b);
			handler.sendMessage(msg);
		}

		public DownLoadQuery(String content) {
			con = content;
		}
	}

	private String getDate() {
		SimpleDateFormat sdf = new SimpleDateFormat("MM-dd HH:mm");
		Date d = new Date();
		return sdf.format(d);
	}

	private String getText() {
		return messageText.getText().toString();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		// getMenuInflater().inflate(R.menu.main, menu);
		menu.add(0, 0, 0, "个人空间");
		menu.add(0, 1, 1, "买买买");
		menu.add(1, 2, 2, "卖卖卖");
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		int item_id = item.getItemId();
		switch (item_id) {
		case 0:
			// 跳转界面
			Intent intent = new Intent(ChatActivity.this, userCenter.class);
			ChatActivity.this.startActivity(intent);
			break;
		case 1:
			buying();
			break;
		case 2:
			selling();
			break;
		}
		return false;
	}

	public void DisplayToast(String s) {
		Toast.makeText(this, s, Toast.LENGTH_SHORT).show();
	}

	public void buying() {
		msgType = "event";
		event = "CLICK";
		eventkey = "rselfmenu_1_0";
		String xmlS;
		xmlS = xml.encode(toUser, fromUser, msgType, null, event, eventkey,
				null, null, null, null, null, null, null, null, null)
				.toString();
		// 启动网络访问
		new Thread(new DownLoadThread(xmlS)).start();
	}

	public void selling() {
		msgType = "event";
		event = "CLICK";
		eventkey = "rselfmenu_2_0";
		String xmlS;
		xmlS = xml.encode(toUser, fromUser, msgType, null, event, eventkey,
				null, null, null, null, null, null, null, null, null)
				.toString();
		// 启动网络访问
		new Thread(new DownLoadThread(xmlS)).start();
	}
}
