nbChatServer
============
/*DB 数据结构*/
tb_user {
    user_name,
    user_nick,
    user_pwd,
    user_id,
    user_logo,
}

tb_friends {
    user_id_a,
    user_id_b,
}

tb_msg {
    id,
    msg,
    send_user_id,
    receive_user_id,
    time,
    flag, /* 0 = 未读 1＝已读*/
}


--------
/*协议规则说明*/
成功：直接返回数据
失败：返回error 字段

/*登录*/
{
    cmd: 'login'
    user_name: 'admin'
    user_pwd: 'admin'
}

{
    cmd: 'login',
    user_name: 'admin'
    user_id: 'xxx'
    user_nick: 'xxx'
    user_logo: 'xxx'
}
{
    cmd: 'login',
    error: 'not found'
}

/*好友操作*/
{
    cmd: 'friend'
    op: 'add' | 'remove'
    user_id: 'xxx'
}
{
    cmd: 'addfriend'
    op: 'add' | 'remove'
    friend_info {
        user_id: 'xxx',
        user_nick: 'xxx',
        user_logo: 'xxx',
        online: 0,
    }
}

/*搜索*/
{
    cmd: 'query'
    key: 'user'  | 'friend'
    value: 'xxx' 
}
{
    cmd: 'query'
    users: [
        {user_id:'xxx', user_nick:'xxx', user_logo:'xxx', online: '1'},
        {user_id:'xxx', user_nick:'xxx', user_logo:'xxx', online: '0'},
    ]
}

/*消息发送*/
{
    cmd: 'msg'
    id: 'xxx'   /*可为空*/
    msg: 'hello‘
    send_user_id: 'xxx'
    receiver_user_id: 'xxx'
}
{
    cmd: 'msg'
    id: 'xxx'
}