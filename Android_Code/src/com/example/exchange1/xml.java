package com.example.exchange1;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.net.URL;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;

import android.app.Application;
import android.util.Xml;

public class xml extends Application {

	static final String urlStr = "http://1.exgood.sinaapp.com/weixin";
	private static String toUser = "EXgood";
	private static String fromUser = null;

	public static String getFromUser() {
		return fromUser;
	}

	public static void setFromUser(String n) {
		fromUser = n;
	}

	// 发送消息的url编码
	// 目前只完成了text部分的编码
	// 输入：用户名，微信公众号，消息类型，文本内容
	public static StringBuilder encode(String touser, String fromuser,
			String msgtype, String content, String event, String eventkey,
			String picurl, String mediaid, String name, String code,
			String sid, String phone, String nickname, String college,
			String sex) {
		// 公共部分
		StringBuilder xml = new StringBuilder();
		xml.append("<xml>");
		xml.append("<ToUserName><![CDATA[" + touser + "]]></ToUserName>");
		xml.append("<FromUserName><![CDATA[" + fromuser + "]]></FromUserName>");
		xml.append("<CreateTime>1348831860</CreateTime>"); // 请求建立时间，这个对我们来说没有用，所以暂时设为了固定的值。也可以获取当前系统时间，然后赋值
		xml.append("<MsgType><![CDATA[" + msgtype + "]]></MsgType>");
		// 公共部分
		// 文本编码
		if (msgtype.equals("text") || msgtype.equals("confirm") ||msgtype.equals("delete")) {
			xml.append("<Content><![CDATA[" + content + "]]></Content>");
			xml.append("<MsgId>1234567890123456</MsgId>");
		}
		// 待完善
		if (msgtype.equals("event") || msgtype.equals("delete") ) {
			xml.append("<Event><![CDATA[" + event + "]]></Event>");
			if (event.equals("CLICK")) {
				xml.append("<EventKey><![CDATA[" + eventkey + "]]></EventKey>");
			}

		} else if (msgtype.equals("image")) {
			xml.append("<PicUrl><![" + picurl + "]></PicUrl>");
			xml.append("<MediaId><![" + mediaid + "]></MediaId>");
			xml.append(" <MsgId>1234567890123456</MsgId>");
		}
		// 这个现在我们应用暂时还用不上，可以不用写
		else if (msgtype.equals("voice")) {

		} else if (msgtype.equals("video")) {

		} else if (msgtype.equals("location")) {

		} else if (msgtype.equals("link")) {

		}
		// 我写的登录与注册部分的编码 by成
		else if (msgtype.equals("login")) {
			xml.append("<Code><![CDATA[" + code + "]]></Code>");
			xml.append("<Phone><![CDATA[" + phone + "]]></Phone>");

		} else if (msgtype.equals("register")) {
			xml.append("<Name><![CDATA[" + name + "]]></Name>");
			xml.append("<Code><![CDATA[" + code + "]]></Code>");
			xml.append("<Sid><![CDATA[" + sid + "]]></Sid>");
			xml.append("<Phone><![CDATA[" + phone + "]]></Phone>");
			xml.append("<Nickname><![CDATA[" + nickname + "]]></Nickname>");
			xml.append("<College><![CDATA[" + college + "]]></College>");
			xml.append("<Sex><![CDATA[" + sex + "]]></Sex>");
		}

		xml.append("</xml>");
		return xml;
	}

	public static String[] getgoodsstate(String goodsinput) {
		String[] temp = goodsinput.split("\\\n");
		//int size = temp.length;
		return temp;
	}
	
	public static String[] getgoodsinfo(String goodsinput) {
		String[] temp = goodsinput.split("\\|");
		//int size = temp.length;
		return temp;
	}

	public static String decode(String re) {
		String myre = "";
		/*
		 * InputStream in_withcode; try { in_withcode = new
		 * ByteArrayInputStream(re.getBytes("UTF-8")); } catch
		 * (UnsupportedEncodingException e) { e.printStackTrace(); }
		 */
		XmlPullParser parser = Xml.newPullParser();
		try {
			parser.setInput(new StringReader(re));
		} catch (XmlPullParserException e) {
			e.printStackTrace();
		}
		int event = 0;
		try {
			event = parser.getEventType();
		} catch (XmlPullParserException e) {
			e.printStackTrace();
		}
		while (event != XmlPullParser.END_DOCUMENT) {
			switch (event) {
			case XmlPullParser.START_DOCUMENT:
				break;
			case XmlPullParser.START_TAG:
				if ("Content".equals(parser.getName())) {
					try {
						myre += parser.nextText();
					} catch (XmlPullParserException e) {
						e.printStackTrace();
					} catch (IOException e) {
						e.printStackTrace();
					}

				}
				break;
			case XmlPullParser.END_TAG:
				break;
			}
			try {
				event = parser.next();
			} catch (XmlPullParserException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return myre;
	}

	// 发送post请求
	// 输入：发送请求的xml的string格式
	// 输出：返回xml的string格式
	// 这部分不用改
	public static String post(String content) {
		String result = "";

		try {
			// 设置url连接
			byte[] xmlData = content.getBytes("UTF-8");
			URL url = new URL(urlStr);
			// URLConnection urlCon = url.openConnection();
			HttpURLConnection urlCon = (HttpURLConnection) url.openConnection();
			urlCon.setDoOutput(true);
			urlCon.setDoInput(true);
			urlCon.setUseCaches(false);
			urlCon.setRequestMethod("POST");
			urlCon.setRequestProperty("Connection", "Keep-Alive");
			urlCon.setRequestProperty("Charset", "UTF-8");
			urlCon.setRequestProperty("Content-Type", "text/xml;charset=UTF-8");
			urlCon.setRequestProperty("Content-lenth",
					String.valueOf(xmlData.length));
			// 发送数据
			urlCon.getOutputStream().write(xmlData);
			urlCon.getOutputStream().flush();
			urlCon.getOutputStream().close();

			if (urlCon.getResponseCode() != 200)
				throw new RuntimeException("请求url失败");
			// 获取返回数据
			InputStream is = urlCon.getInputStream();
			ByteArrayOutputStream out = new ByteArrayOutputStream();
			byte[] buf = new byte[1024];
			int len;
			while ((len = is.read(buf)) != -1) {
				out.write(buf, 0, len);
			}
			// 返回的xml的string格式
			result = out.toString("UTF-8");
			out.close();
		} catch (Exception e) {
			System.out.println(e);
		}
		return result;
	}
}