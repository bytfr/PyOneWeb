// 登录
// 获取元素
var Inputs = document.getElementById("LoginPage");
// 获取输入内容
var InputList = Inputs.getElementsByTagName("input");

// 用户名
var UserName = InputList[0];
// 密码
var Pwd = InputList[1];

// 绑定事件
// 用户名输入事件
UserName.onkeydown = function(e){
    console.log(e.keyCode);
    // 方向键
    if(e.keyCode == 37 || e.keyCode == 38 || e.keyCode == 39 || e.keyCode == 40){
        console.log("移动光标");
        return;
    }
	// 不能输入特殊字符
	if(!( (e.keyCode >= 65 && e.keyCode <= 90) || (e.keyCode >= 48 && e.keyCode <= 57) || e.key == '_' || e.keyCode == 16 || e.keyCode == 8) ){
		// 回车
		if(e.keyCode == 13){
			// 失去焦点
			UserName.blur();
			// 获得焦点
			Pwd.focus();
			return;
		}
		return false;
	}
}

// 密码输入事件
Pwd.onkeydown = function(e){
    // 方向键
    if(e.keyCode == 37 || e.keyCode == 38 || e.keyCode == 39 || e.keyCode == 40){
        console.log("移动光标");
        return;
    }
	// 不输入特殊字符
	if(!((e.keyCode >= 65 && e.keyCode <= 90) || (e.keyCode >= 48 && e.keyCode <= 57) || e.key == '_' || e.keyCode == 16 || e.keyCode == 8)){
		// 回车
		if(e.keyCode == 13){
			// 失去焦点
			pwd.blur();
			return;
		}
		return false;
	}
}

// 判断
function CheckLogin(){
	// 不为空
	if(Pwd.value && UserName.value){
		return true;
	}
	return false;
}