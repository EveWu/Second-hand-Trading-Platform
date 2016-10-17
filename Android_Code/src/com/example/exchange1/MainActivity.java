package com.example.exchange1;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.CompoundButton.OnCheckedChangeListener;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends Activity {

	private EditText userName, password;
	private Button btn_login, btn_reg;
	private String phoneValue, passwordValue;
	private CheckBox rem_pw;
	private CheckBox auto_login;
	public static final String DATABASE = "Login";
	private SharedPreferences sp;
	Editor editor;
	String msgType = null;
	Handler handler;

	static String toUser = "EXgood";
	String fromUser = null;

	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		setContentView(R.layout.activity_login);

		// 获得实例对象
		userName = (EditText) findViewById(R.id.et_zh);
		password = (EditText) findViewById(R.id.et_mima);
		btn_login = (Button) findViewById(R.id.btn_login);
		btn_reg = (Button) findViewById(R.id.btn_regist);
		rem_pw = (CheckBox) findViewById(R.id.cb_mima);
		auto_login = (CheckBox) findViewById(R.id.cb_auto);
		

		// 用于记住密码和自动登录状态
		sp = getSharedPreferences(DATABASE, Activity.MODE_PRIVATE);
		editor = sp.edit();

		// 判断记住密码多选框的状态
		if (sp.getBoolean("ISCHECK", false)) {
			// 设置默认是记录密码状态
			rem_pw.setChecked(true);
			userName.setText(sp.getString("USER_NAME", ""));
			password.setText(sp.getString("PASSWORD", ""));
			// 判断自动登陆多选框状态
			if (sp.getBoolean("AUTO_ISCHECK", false)) {
				// 设置默认是自动登录状态
				auto_login.setChecked(true);
				// 跳转界面
				Intent intent = new Intent(MainActivity.this,
						ChatActivity.class);
				MainActivity.this.startActivity(intent);
			}
		}

		// 登录监听事件
		btn_login.setOnClickListener(new OnClickListener() {

			public void onClick(View v) {
				phoneValue = userName.getText().toString();
				passwordValue = password.getText().toString();

				msgType = "login";
				String xmlS;
				xmlS = xml.encode(toUser, fromUser, msgType, null, null, null,
						null, null, null, passwordValue, null, phoneValue,
						null, null, null).toString();

				new Thread(new DownLoadThread(xmlS)).start();

			}
		});
		// 更新结果显示
		// 并对xml进行解析
		handler = new Handler() {
			@Override
			public void handleMessage(Message msg) {
				Bundle b = msg.getData();
				String re = b.getString("result");

				if (re.equals("N")) {
					Toast.makeText(MainActivity.this, "用户名或密码错误，请重新登录或前往注册",
							Toast.LENGTH_LONG).show();
				} else {
					Toast.makeText(MainActivity.this, "登录成功",
							Toast.LENGTH_SHORT).show();
					// 登录成功和记住密码框为选中状态才保存用户信息
					if (rem_pw.isChecked()) {
						// 记住用户名、密码、
						editor.putString("USER_NAME", phoneValue);
						editor.putString("PASSWORD", passwordValue);
						editor.commit();
					}
					// 改变openID
					xml.setFromUser(re);
					// 跳转界面
					Intent intent = new Intent(MainActivity.this,
							ChatActivity.class);
					MainActivity.this.startActivity(intent);
					finish();
				}

			}
		};

		// 监听记住密码多选框按钮事件
		rem_pw.setOnCheckedChangeListener(new OnCheckedChangeListener() {
			public void onCheckedChanged(CompoundButton buttonView,
					boolean isChecked) {
				if (rem_pw.isChecked()) {
					editor.putBoolean("ISCHECK", true).commit();

				} else {
					editor.putBoolean("ISCHECK", false).commit();

				}

			}
		});

		// 监听自动登录多选框事件
		auto_login.setOnCheckedChangeListener(new OnCheckedChangeListener() {
			public void onCheckedChanged(CompoundButton buttonView,
					boolean isChecked) {
				if (auto_login.isChecked()) {
					editor.putBoolean("AUTO_ISCHECK", true).commit();

				} else {
					editor.putBoolean("AUTO_ISCHECK", false).commit();
				}
			}
		});

		btn_reg.setOnClickListener(new OnClickListener() {
			public void onClick(View v) {
				// 跳转界面
				Intent intent = new Intent(MainActivity.this,
						RegistActivity.class);
				MainActivity.this.startActivity(intent);

			}
		});

	}
	
	

	class DownLoadThread implements Runnable {
		private String con;

		public DownLoadThread(String content) {
			con = content;
		}

		@Override
		public void run() {
			Bundle b = new Bundle();
			Message msg = handler.obtainMessage();
			String xmlS = xml.post(con); // post
			String re = xml.decode(xmlS);
			b.putString("result", re);
			msg.setData(b);
			handler.sendMessage(msg);
			// Log.i("Thread1", xmlS);
		}

	}

}
