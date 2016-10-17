数据库中各种表的作用以及详解
括号内为希望的值（简单的就不加括号说明了），’:’后为作用。
具体字段的类型请看表结构，现在没有对数据的类型进行检查，即不符合要求的值也会被插入到项中。

表users: 存放用户个人信息、记录用户当前的操作状态等
包含字段: 
	openID(手机号或微信的openID): 唯一识别用户
	sID: 学好
	t_name: 真实姓名
	nickname: 昵称
	sex: 性别
	college: 学院
	MainState(0,1,2,3,…): 记录当前用户的主状态，在weixinInterface中用于判断用户当前输入的文本消息属于哪部分操作
		0——主界面
		1——身份绑定
		2——卖东西
		3——买东西
		目前只用到了值0,1,2,3。后续可继续添加。
	IDBindingState(0,1,2,3,…): 身份绑定状态值，记录用户已经输入了哪些信息，这样我们才能知道用户当前输入的是什么信息，从而进行相应的操作以及返回提示消息
		0——表中的默认值，在实际操作中不会出现该值。因为在identityBinding.py中每次插入一条新的用户信息后，理由update语句随后将该值置为1。
		1——用户点击身份绑定后，设为改值，身份绑定的第一个状态，即用户还没有输入任何个人信息
		2——已绑定学号
		3——已绑定学号+姓名
		4——已绑定学号+姓名＋昵称
		5——已绑定学号+姓名＋昵称＋性别
		6——已绑定学号+姓名＋昵称＋性别＋学院
		7——已绑定学号+姓名＋昵称＋性别＋学院＋手机
		8——所有信息都已经绑定
		具体使用请看identityBinding.py和updateBindingInfo.py
	GoodsSellState(0,1,2,3,…): 商品上架状态值
		0——默认值，没有商品上架，商品上架完成也会将该值置0
		1——商品上架第一个状态，没有任何物品信息
		2——已输入商品名称
		3——已输入商品名称＋价格
		具体使用请看sell.py和updateSell.py
	Goodsbuystate(0,1,2,3,…): 商品购买状态值
		0——初始状态
		1——已输入需要的物品名称
	latest_goodID:  卖家正在上架商品ID
	password: 密码
	phone: 手机号
    
表goods: 存放商品
包含字段:
	goodID: 商品ID
    sellerID: 卖家ID
    name: 商品名称
    price: 商品价格
    description: 商品描述
    startDate: 商品信息最新修改时间
    state: 商品状态，0为正在上架或交易，1为在售

表goods_done: 存放以及交易了的商品
包含字段:
	doneID: 唯一标识符
    goodID: 商品ID
    sellerID: 卖家ID
    name: 商品名称
    price: 商品价格
    description: 商品描述
    startDate: 商品交易成功时间
    
表buy: 暂时缓存符合买家购物条件的商品ID以及卖家ID，用作提示卖家符合条件的商品信息
包含字段:
	buyID: 唯一标识符
    buyerID: 卖家ID
    goodID: 商品ID
    
表orders: 存放正在进行的订单
包含字段:
	orderID: 订单ID
    goodID: 商品ID
    sellerID: 卖家ID
    buyerID: 买家ID
    startDate: 订单最新修改时间
    state: 订单状态
    	0——买家下单，等待卖家确认
        1——卖家已确认，等待买家确认收货
        
表orders_done: 存放交易成功的订单
包含字段:
	doneID: 唯一标识符
    goodID: 商品ID
    sellerID: 卖家ID
    buyerID: 买家ID
    startDate: 订单最新修改时间    














