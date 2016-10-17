package com.example.exchange1;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.AlertDialog.Builder;
import android.app.PendingIntent;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.Matrix;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.support.v4.view.ViewPager.OnPageChangeListener;
import android.telephony.SmsManager;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.TranslateAnimation;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.AdapterView.OnItemLongClickListener;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Toast;

public class userCenter extends Activity {
	private ViewPager viewPager;
	private ImageView imageView;
	private TextView textView1, textView2, textView3;
	private List<View> views;
	private int offset = 0;
	private int currIndex = 0;
	private int bmpW;
	private View view1, view2, view3;
	private String msgType, event, eventKey;
	String toUser = "EXgood";
	String fromUser = null;
	ListView buyView1, buyView2, buyView3;
	Handler handler, handler2, handler3, handler4, handler5;
	TextView tv;
	SmsManager smsManager;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.user_inf);
		Log.i("Heidi_layout1", "onCreate");
		// 设置openID
		fromUser = xml.getFromUser().toString();
		// 获取短信管理器
		smsManager = SmsManager.getDefault();

		// 初始化更新我的订单和我的卖单的listview
		handler = new Handler() {
			@Override
			public void handleMessage(Message msg) {
				Bundle b = msg.getData();
				String re = b.getString("result");
				// Log.i("showList", re);
				setView2(re);
				setView3(re);
			}
		};

		// 判断订单确认是否成功
		handler2 = new Handler() {
			@Override
			public void handleMessage(Message msg) {
				Bundle b = msg.getData();
				String re = b.getString("result");
				Log.i("longClick", re + '\n');
				if (re.equals("Y")) {
					Toast.makeText(userCenter.this, "确认成功", Toast.LENGTH_LONG)
							.show();

				} else {
					Toast.makeText(userCenter.this, re, Toast.LENGTH_LONG)
							.show();
				}
				Log.i("longClick", "end");

			}
		};
		// listView2and3判断删除是否成功
		handler3 = new Handler() {
			@Override
			public void handleMessage(Message msg) {
				Bundle b = msg.getData();
				String re = b.getString("result");
				Log.i("longClick", re + '\n');
				if (re.equals("Y\n")) {
					Toast.makeText(userCenter.this, "删除成功", Toast.LENGTH_LONG)
							.show();
					//setView2(re);
					//setView3(re);
					//TODO:更新列表

				} else {
					Toast.makeText(userCenter.this, re, Toast.LENGTH_LONG)
							.show();
				}
				Log.i("longClick", "end");
			}
		};

		// listView1判断删除是否成功
		handler5 = new Handler() {
			@Override
			public void handleMessage(Message msg) {
				Bundle b = msg.getData();
				String re = b.getString("result");
				Log.i("longClick1", "re:\n" + re + '\n');
				if (re.equals("Y\n")) {
					Toast.makeText(userCenter.this, "删除成功", Toast.LENGTH_LONG)
							.show();
					//TODO:更新列表
					//setView1(re);
				} else {
					Toast.makeText(userCenter.this, re, Toast.LENGTH_LONG)
							.show();
				}
			}
		};

		// 初始化我的物品的listView
		handler4 = new Handler() {
			@Override
			public void handleMessage(Message msg) {
				Bundle b = msg.getData();
				String re = b.getString("result");
				Log.i("handler4", re);
				setView1(re);
			}
		};

		InitImageView();
		InitTextView();
		InitViewPager();
		msgType = "event";
		event = "CLICK";
		eventKey = "queryorders";
		// xml编码
		String xmlS;
		xmlS = xml.encode(toUser, fromUser, msgType, null, event, eventKey,
				null, null, null, null, null, null, null, null, null)
				.toString();
		Log.i("showList", "layout");
		// 显示订单和卖单listView
		new Thread(new DownLoadThread(xmlS, 1)).start();

		msgType = "event";
		event = "CLICK";
		eventKey = "querygoods";
		xmlS = xml.encode(toUser, fromUser, msgType, null, event, eventKey,
				null, null, null, null, null, null, null, null, null)
				.toString();

		new Thread(new DownLoadThread(xmlS, 4)).start();

	}

	private void setView1(String info) {
		Log.i("longClick1", "info:" + info);
		List<Map<String, String>> buyList = new ArrayList<Map<String, String>>();

		if (info.equals("")) {
			Log.i("longClick1", "here:\n");
			;
		} else {
			String[] orders = xml.getgoodsstate(info);
			int size = orders.length;

			Log.i("longClick1", "size:\n" + size);

			Map<String, String> map;

			for (int i = 0; i < size; i++) {
				String[] gInfo = xml.getgoodsinfo(orders[i]);
				map = new HashMap<String, String>();
				map.put("ID", gInfo[1]);
				map.put("goodID", "货物编号: " + gInfo[1]);
				map.put("ordersState", gInfo[2]);
				map.put("goodInfo", gInfo[3] + "  price:" + gInfo[4]);
				map.put("intro", gInfo[5]);
				map.put("date", gInfo[6]);
				String a = map.get("intro");
				buyList.add(map);
			}
		}
		SimpleAdapter listItemAdapter = new SimpleAdapter(this, buyList,
				R.layout.buy_item, new String[] { "goodInfo", "date", "intro",
						"goodID" }, new int[] { R.id.goodInfo, R.id.date,
						R.id.intro, R.id.owner, });

		buyView1 = (ListView) view1.findViewById(R.id.myListView);
		buyView1.setAdapter(listItemAdapter);

		// 长按删除
		OnItemLongClickListener mItemLongCLick = deletBuyItemLong(1);
		buyView1.setOnItemLongClickListener(mItemLongCLick);

	}

	private void setView2(String info) {
		Log.i("showList", "info:" + info);
		List<Map<String, String>> buyList = new ArrayList<Map<String, String>>();

		if (info.equals("")) {
			;
		} else {
			String[] orders = xml.getgoodsstate(info);
			int size = orders.length;

			Map<String, String> map;

			for (int i = 0; i < size; i++) {
				String[] gInfo = xml.getgoodsinfo(orders[i]);
				if (gInfo[3].equals(xml.getFromUser())) {
					map = new HashMap<String, String>();
					map.put("goodID", gInfo[1]);
					map.put("owner", "卖家:" + gInfo[9] + "   电话:" + gInfo[11]);
					map.put("date", gInfo[4]);
					map.put("ordersState", gInfo[5]);
					map.put("goodInfo", gInfo[6] + "  price:" + gInfo[7]);
					map.put("intro", gInfo[8]);
					map.put("phone", gInfo[11]);

					if (gInfo[5].equals("0"))
						map.put("remind", "等待卖家确认");
					if (gInfo[5].equals("1"))
						map.put("remind", "等待买家收货");
					if (gInfo[5].equals("2"))
						map.put("remind", "订单已完成");
					buyList.add(map);
				}
			}
		}
		SimpleAdapter listItemAdapter = new SimpleAdapter(this, buyList,
				R.layout.buy_item, new String[] { "goodInfo", "date", "intro",
						"owner", "remind" }, new int[] { R.id.goodInfo,
						R.id.date, R.id.intro, R.id.owner, R.id.remind });

		buyView2 = (ListView) view2.findViewById(R.id.buyListView);
		buyView2.setAdapter(listItemAdapter);

		OnItemClickListener mItemClickListener = buyItem();
		buyView2.setOnItemClickListener(mItemClickListener);
		// 长按删除
		OnItemLongClickListener mItemLongCLick = deletBuyItemLong(2);
		buyView2.setOnItemLongClickListener(mItemLongCLick);

	}

	private void setView3(String info) {
		List<Map<String, String>> buyList = new ArrayList<Map<String, String>>();
		if (info.equals("")) {
			;
		} else {
			String[] orders = xml.getgoodsstate(info);
			int size = orders.length;
			Log.i("Thread1", "size:" + size);

			Map<String, String> map;

			for (int i = 0; i < size; i++) {
				String[] gInfo = xml.getgoodsinfo(orders[i]);
				if (gInfo[2].equals(xml.getFromUser())) {
					map = new HashMap<String, String>();
					map.put("goodID", gInfo[1]);
					map.put("owner", "买家:" + gInfo[10] + "   电话:" + gInfo[12]);
					map.put("date", gInfo[4]);
					map.put("ordersState", gInfo[5]);
					map.put("goodInfo", gInfo[6] + "  price:" + gInfo[7]);
					map.put("intro", gInfo[8]);
					map.put("phone", gInfo[12]);

					if (gInfo[5].equals("0"))
						map.put("remind", "等待卖家确认");
					if (gInfo[5].equals("1"))
						map.put("remind", "等待买家收货");
					if (gInfo[5].equals("2"))
						map.put("remind", "订单已完成");
					buyList.add(map);
				}
			}
		}
		SimpleAdapter listItemAdapter = new SimpleAdapter(this, buyList,
				R.layout.buy_item, new String[] { "goodInfo", "date", "intro",
						"remind" }, new int[] { R.id.goodInfo, R.id.date,
						R.id.intro, R.id.remind });
		buyView3 = (ListView) view3.findViewById(R.id.sellListView);
		buyView3.setAdapter(listItemAdapter);
		// 短按确认
		OnItemClickListener mItemClickListener = sellItem();
		buyView3.setOnItemClickListener(mItemClickListener);
		// 长按删除
		OnItemLongClickListener mItemLongCLick = deletBuyItemLong(3);
		buyView3.setOnItemLongClickListener(mItemLongCLick);

	}

	/*************************** 短按 ****************************/

	// 我的订单
	private OnItemClickListener buyItem() {
		OnItemClickListener mItemClickListener = new OnItemClickListener() {
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				HashMap<String, String> item = (HashMap<String, String>) parent
						.getItemAtPosition(position);
				if (item.get("ordersState").equals("1")) {
					String goodID = item.get("goodID");
					String buyPhone = item.get("phone");
					String info = item.get("owner");
					String good = item.get("goodInfo");
					checkOrder("确认收货？！", goodID, buyPhone, info, good, 1);
				}
			}

		};
		return mItemClickListener;
	}

	// 我的卖单
	private OnItemClickListener sellItem() {
		OnItemClickListener mItemClickListener = new OnItemClickListener() {
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				HashMap<String, String> item = (HashMap<String, String>) parent
						.getItemAtPosition(position);
				if (item.get("ordersState").equals("0")) {
					String goodID = item.get("goodID");
					String sellPhone = item.get("phone");
					String info = item.get("owner");
					String good = item.get("goodInfo");
					checkOrder("确认订单？！", goodID, sellPhone, info, good, 2);
				}
			}
		};
		return mItemClickListener;
	}

	// 生成对话框
	void checkOrder(String title, final String goodID, final String phone,
			final String info, final String good, final int type) {
		Builder builder = new AlertDialog.Builder(userCenter.this);
		builder.setTitle(title);

		String msgType = "confirm";

		Log.i("Thread1", goodID);

		final String xmlS = xml.encode(toUser, fromUser, msgType, goodID, null,
				null, null, null, null, null, null, null, null, null, null)
				.toString();
		builder.setIcon(android.R.drawable.ic_dialog_info);
		builder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialog, int which) {
				Log.i("Thread1", "post\n" + xmlS);
				new Thread(new DownLoadThread(xmlS, 2)).start();
				if (type == 1) {
					sendMessage(phone, info + "\n买家已经确认收货\n货物号为:" + goodID
							+ "\n------------Exchange");
				} else if (type == 2) {
					sendMessage(phone, info + "\n卖家已经确认您的订单:\n" + good
							+ "\n-------------Exchange");
				}

			}
		});
		builder.setNegativeButton("取消", new DialogInterface.OnClickListener() {

			@Override
			public void onClick(DialogInterface dialog, int which) {
			}
		}).show();
	}

	/************************ 长按 ****************************/

	// 删除订单
	private OnItemLongClickListener deletBuyItemLong(final int flag) {
		OnItemLongClickListener mItemLong = new OnItemLongClickListener() {
			@Override
			public boolean onItemLongClick(AdapterView<?> parent, View view,
					int position, long id) {
				HashMap<String, String> item = (HashMap<String, String>) parent
						.getItemAtPosition(position);
				String goodID = item.get("ID");
				String goodState = item.get("ordersState");
				String opt = "*";
				if (flag == 1) {
					opt = "0";
				} else {
					if (goodState.equals("2")) {
						opt = "2";
					} else if (goodState.equals("1") || goodState.equals("0")) {
						opt = "1";
					}
				}
				String xmlS = xml.encode(toUser, fromUser, "delete", goodID,
						opt, null, null, null, null, null, null, null, null,
						null, null).toString();
				Log.i("longClick1", "thread 5:\n" + xmlS);
				deleteDialog(xmlS, flag);
				return true;
			}
		};
		return mItemLong;
	}


	// 生成对话框
	private void deleteDialog(String a, final int i) {
		Builder builder = new AlertDialog.Builder(userCenter.this);
		if (i == 1) {
			builder.setTitle("删除我的物品");
		} else if (i == 2) {
			builder.setTitle("删除订单");
		} else if (i == 3) {
			builder.setTitle("删除卖单");
		}
		builder.setIcon(android.R.drawable.ic_dialog_info);
		final String xmlS = a;
		builder.setPositiveButton("是", new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialog, int which) {
				if (i == 1) {
					Log.i("longClick1", "thread 5");
					new Thread(new DownLoadThread(xmlS, 5)).start();
				} else {
					new Thread(new DownLoadThread(xmlS, 3)).start();
				}
			}
		});
		builder.setNegativeButton("否", new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialog, int which) {
			}
		}).show();
	}

	/********************** 发送短信 ************************/

	private void sendMessage(String phone, String message) {

		if (message.length() > 70) {
			List<String> contents = smsManager.divideMessage(message);
			for (String sms : contents) {
				smsManager.sendTextMessage(phone, null, sms, null, null);
			}
		} else {
			smsManager.sendTextMessage(phone, null, message, null, null);
		}
	}

	/*********************** 进程 *************************/

	class DownLoadThread implements Runnable {
		private String con;
		int flag;

		public DownLoadThread(String content, int f) {
			con = content;
			flag = f;
		}

		@Override
		public void run() {
			Bundle b = new Bundle();
			Message msg = handler.obtainMessage();
			String xmlS = xml.post(con); // post
			Log.i("view1", "click return:\n" + xmlS);
			xmlS = xml.decode(xmlS);
			Log.i("view1", "click decode:\n" + xmlS);
			b.putString("result", xmlS);
			msg.setData(b);
			if (flag == 1) {
				handler.sendMessage(msg);
			} else if (flag == 2) {
				handler2.sendMessage(msg);
			} else if (flag == 3) {
				handler3.sendMessage(msg);
			} else if (flag == 4) {
				Log.i("view1", "thread begin");
				handler4.sendMessage(msg);
			} else if (flag == 5) {
				Log.i("longClick1", "hanlder5:\n" + msg);
				handler5.sendMessage(msg);
			}
			Log.i("Thread1", "decode\n");
		}
	}

	public void setColor(int i) {
		if (i == 0) {
			textView1.setBackgroundColor(Color.parseColor("#FFFFFF"));
			textView2.setBackgroundColor(Color.parseColor("#999999"));
			textView3.setBackgroundColor(Color.parseColor("#999999"));
		} else if (i == 1) {
			textView1.setBackgroundColor(Color.parseColor("#999999"));
			textView2.setBackgroundColor(Color.parseColor("#FFFFFF"));
			textView3.setBackgroundColor(Color.parseColor("#999999"));
		} else if (i == 2) {
			textView1.setBackgroundColor(Color.parseColor("#999999"));
			textView2.setBackgroundColor(Color.parseColor("#999999"));
			textView3.setBackgroundColor(Color.parseColor("#FFFFFF"));
		}
	}

	private void InitViewPager() {
		viewPager = (ViewPager) findViewById(R.id.vPager);
		views = new ArrayList<View>();
		LayoutInflater inflater = getLayoutInflater();
		view1 = inflater.inflate(R.layout.lay1, null);
		view2 = inflater.inflate(R.layout.lay2, null);
		view3 = inflater.inflate(R.layout.lay3, null);
		views.add(view1);
		views.add(view2);
		views.add(view3);
		viewPager.setAdapter(new MyViewPagerAdapter(views));
		viewPager.setCurrentItem(0);
		setColor(0);
		viewPager.setOnPageChangeListener(new MyOnPageChangeListener());
	}

	private void InitTextView() {
		textView1 = (TextView) findViewById(R.id.text1);
		textView2 = (TextView) findViewById(R.id.text2);
		textView3 = (TextView) findViewById(R.id.text3);

		textView1.setOnClickListener(new MyOnClickListener(0));
		textView2.setOnClickListener(new MyOnClickListener(1));
		textView3.setOnClickListener(new MyOnClickListener(2));
	}

	/**
	 * 2 * 初始化动画，这个就是页卡滑动时，下面的横线也滑动的效果，在这里需要计算一些数据 3
	 */

	private void InitImageView() {
		imageView = (ImageView) findViewById(R.id.cursor);
		bmpW = BitmapFactory.decodeResource(getResources(), R.drawable.bar2)
				.getWidth();// 获取图片宽度
		DisplayMetrics dm = new DisplayMetrics();
		getWindowManager().getDefaultDisplay().getMetrics(dm);
		int screenW = dm.widthPixels;// 获取分辨率宽度
		offset = (screenW / 3 - bmpW) / 2;// 计算偏移量
		Matrix matrix = new Matrix();
		matrix.postTranslate(offset, 0);
		imageView.setImageMatrix(matrix);// 设置动画初始位置
	}

	/**
	 * 头标点击监听 3
	 */
	private class MyOnClickListener implements OnClickListener {
		private int index = 0;

		public MyOnClickListener(int i) {
			index = i;
		}

		public void onClick(View v) {
			viewPager.setCurrentItem(index);
		}

	}

	public class MyViewPagerAdapter extends PagerAdapter {
		private List<View> mListViews;

		public MyViewPagerAdapter(List<View> mListViews) {
			this.mListViews = mListViews;
		}

		@Override
		public void destroyItem(ViewGroup container, int position, Object object) {
			container.removeView(mListViews.get(position));
		}

		@Override
		public Object instantiateItem(ViewGroup container, int position) {
			container.addView(mListViews.get(position), 0);
			return mListViews.get(position);
		}

		@Override
		public int getCount() {
			return mListViews.size();
		}

		@Override
		public boolean isViewFromObject(View arg0, Object arg1) {
			return arg0 == arg1;
		}
	}

	public class MyOnPageChangeListener implements OnPageChangeListener {

		int one = offset * 2 + bmpW;// 页卡1 -> 页卡2 偏移量
		int two = one * 2;// 页卡1 -> 页卡3 偏移量

		public void onPageScrollStateChanged(int arg0) {

		}

		public void onPageScrolled(int arg0, float arg1, int arg2) {

		}

		public void onPageSelected(int arg0) {
			Animation animation = new TranslateAnimation(one * currIndex, one
					* arg0, 0, 0);// 显然这个比较简洁，只有一行代码。
			currIndex = arg0;
			animation.setFillAfter(true);// True:图片停在动画结束位置
			animation.setDuration(300);
			imageView.startAnimation(animation);
			setColor(viewPager.getCurrentItem());

		}
	}
}
