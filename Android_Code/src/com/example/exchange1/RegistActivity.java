package com.example.exchange1;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class RegistActivity extends Activity {

	private EditText userName, userID, nickName, phone, password;
	private Button btn_reg;
	private String userNameValue, userIDValue, nickNameValue, phoneValue,
			passwordValue;

	static String toUser = "EXgood";
	String fromUser = null;
	private String msgType;
	Handler handler;

	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_regist);

		// 获得实例对象
		userName = (EditText) findViewById(R.id.Edit_name);
		userID = (EditText) findViewById(R.id.Edit_Id);
		nickName = (EditText) findViewById(R.id.Edit_nickname);
		phone = (EditText) findViewById(R.id.Edit_phone);
		password = (EditText) findViewById(R.id.Edit_key);

		btn_reg = (Button) findViewById(R.id.btn_reg);

		btn_reg.setOnClickListener(new OnClickListener() {
			public void onClick(View v) {
				msgType = "register";
				userNameValue = userName.getText().toString();
				userIDValue = userID.getText().toString();
				nickNameValue = nickName.getText().toString();
				phoneValue = phone.getText().toString();
				passwordValue = password.getText().toString();

				// xml编码
				String xmlS;
				xmlS = xml.encode(toUser, phoneValue, msgType, null, null, null,
						null, null, userNameValue, passwordValue, userIDValue,
						phoneValue, nickNameValue, null, null).toString();
				// 启动网络访问
				new Thread(new DownLoadThread(xmlS)).start();

			}
		});
		// 并对xml进行解析
		handler = new Handler() {
			@Override
			public void handleMessage(Message msg) {
				Bundle b = msg.getData();
				String re = b.getString("result");
				String decMsg = xml.decode(re);
				
				
				if (decMsg.equals("Y")) {
					Toast.makeText(RegistActivity.this, "注册成功",
							Toast.LENGTH_LONG).show();
					//设置openID
					xml.setFromUser(phoneValue);
					// 跳转界面
					Intent intent = new Intent(RegistActivity.this,
							ChatActivity.class);
					RegistActivity.this.startActivity(intent);
					finish();
				}else if(decMsg.equals("N")){
					Toast.makeText(RegistActivity.this, "注册失败",
							Toast.LENGTH_LONG).show();
				}
			}
		};

	}

	class DownLoadThread implements Runnable {
		private String con;

		@Override
		public void run() {
			// Log.d("Thread","enter run");
			Bundle b = new Bundle();
			Message msg = handler.obtainMessage();
			String xmlS = xml.post(con); // post
			b.putString("result", xmlS);
			msg.setData(b);
			handler.sendMessage(msg);
		}

		public DownLoadThread(String content) {
			con = content;
		}
	}

}