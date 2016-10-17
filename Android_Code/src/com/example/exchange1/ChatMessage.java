package com.example.exchange1;

public class ChatMessage
{

	private String date;
	private String text;
	private int layoutID;

	public ChatMessage(String date, String text, int id)
	{
		this.date = date;
		this.text = text;
		this.layoutID = id;
	}

	public String getDate()
	{
		return date;
	}

	public void setDate(String date)
	{
		this.date = date;
	}

	public String getText()
	{
		return text;
	}

	public void setText(String text)
	{
		this.text = text;
	}

	public int getLayoutID()
	{
		return layoutID;
	}

	public void setLayoutID(int layoutID)
	{
		this.layoutID = layoutID;
	}

}