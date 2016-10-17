package com.example.exchange1;

import java.util.ArrayList;

import android.content.Context;
import android.database.DataSetObserver;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;
import android.widget.TextView;

public class ChattingAdapter extends BaseAdapter {
	// private static final String TAG = ChattingAdapter.class.getSimpleName();

	private ArrayList<ChatMessage> list;
	private Context context;

	public ChattingAdapter(Context context, ArrayList<ChatMessage> list) {
		this.context = context;
		this.list = list;
	}

	public boolean areAllItemsEnabled() {
		return false;
	}

	public boolean isEnabled(int arg0) {
		return false;
	}

	@Override
	public int getCount() {
		return list.size();
	}

	@Override
	public Object getItem(int position) {
		return list.get(position);
	}

	@Override
	public long getItemId(int position) {
		return position;
	}

	public int getItemViewType(int position) {
		return position;
	}

	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		ChatMessage msg = list.get(position);
		int itemlayout = msg.getLayoutID();
		LinearLayout layout = new LinearLayout(context);
		LayoutInflater vi = (LayoutInflater) context
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		vi.inflate(itemlayout, layout, true);

		TextView tvDate = (TextView) layout
				.findViewById(R.id.messagedetail_row_date);

		tvDate.setText(msg.getDate());

		TextView tvText = (TextView) layout
				.findViewById(R.id.messagedetail_row_text);

		tvText.setText(msg.getText());
		return layout;
	}

	public int getViewTypeCount() {
		return list.size();
	}

	public boolean hasStableIds() {
		return false;
	}

	public boolean isEmpty() {
		return false;
	}

	public void registerDataSetObserver(DataSetObserver observer) {
	}

	public void unregisterDataSetObserver(DataSetObserver observer) {
	}

}