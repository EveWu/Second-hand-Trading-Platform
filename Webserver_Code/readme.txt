Table current_state is used to store the state of our weixin's current state.
When users enter our weixin, the value of current is set to be 0. Means that users are at the main menu.
More values are to be filled later...


Now we have

Main Menu:
0............weixinInterface.py

Subfuction:

1............identitifyBinding.py     (by eve and Xiang)
2............identityBinding.py       (by eve and Xiang)
3............search.py                (by Chen zehao)
4............sqlInterface.py          
5............postUserIdentity.py      (by Xiangxiyun)
6............getAccessToken.py        (by Xiangxiyun)
7............updateBingdingInfo.py    (by Xiangxiyun)
8............postUserIdentify.py      (by Xiangxiyun)
9............updatebuyv1.py           (by Chen zehao)
10...........buyv1.py                 (by Chen zehao)
11...........Delete.py                (by eve)
12...........Hint.py                  (by eve)
13...........UpdateDatabase.py        (by eve)
14...........getGood.py               (by eve)
15...........getGoodText.py           (by eve)
16...........getOrder.py              (by eve)
17...........getOrderText.py          (by eve)
18...........hintText.py              (by eve)
19...........orderConfirm.py          (by eve)
20...........sell.py                  (by eve)
21...........updateSell.py            (by eve)

XML file:
1............return_text              (from wechat development document)
2............return_article           (from wechat development document)



//2014-11-28
//by Xiang xiyun

Adding file:   

(.py):
1.postUserIdentity.py
2.getAccessToken.py

(.xml)
1.return_article.xml


Detail :

If you need the access_token please 
1. Make sure the memcache service is opened in SAE.
2. Check whether your file bas import the file "getAccessToken.py".
3. get the token with the sentence:
          token = getAccessToken.token


//2014-11-30
//by Xiang xiyun

Adding file:
(.py)
1.updateBingdingInfo.py
2.postUserIdentify.py

Detail :
1. solve the problem of encoding utf-8
2. encapsulate the function binding identity and unbindng identity