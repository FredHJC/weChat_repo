#!/usr/bin/env python
# coding:utf8
import sys
import imp

imp.reload(sys)

import itchat
from itchat.content import *

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
   return msg['Text']

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg['Text'])
    print(msg['Content'])

# 自动回复文本等类别消息
# isGroupChat=False表示非群聊消息
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=False)
# def text_reply(msg):
# 	#print "here we are!"
# 	itchat.send('稍后会给您回复!', msg['FromUserName'])

# # 自动回复图片等类别消息
# # isGroupChat=False表示非群聊消息
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False)
# def download_files(msg):
# 	itchat.send('稍后会给您回复！', msg['FromUserName'])

# # 自动处理添加好友申请
# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
# 	itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
# 	itchat.send_msg(u'您好', msg['RecommendInfo']['UserName'])
    
# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
	# 消息来自于哪个群聊
	chatroom_id = msg['FromUserName']
	group_name= chatrooms_rename.get(chatroom_id)
	username = msg['ActualNickName']

	print("my commend:"+chatroom_id)
	print(username)
	print(msg['Text'])

	# print("length: "+len(msg['Text']))

	if (group_name=="NYUSH 实习资讯分享") and len(msg['Text'])>50:
		for item in chatrooms:
			print(item)
		#print 3
			if not item['UserName'] == chatroom_id:
				#print 4
				itchat.send('这是一个自动转发机器人\n %s—%s 说:\n%s' % (item['NickName'],username, msg['Content']), item['UserName'])

	# if (chatroom_id=="@d3a27df357f1602aa4a3f6eaaa1aaa9d"):
	# 	cont=msg['Text']
	# 	itchat.send('这是一个测试： %s—%s 说:\n%s' % ('test','test', cont), "@@6f8053c4d4d5eaf7b69e686dd263f127aa361be82cb23ef0aa8decc266d14ae4")


	# print("chatroom_ids:"+chatroom_ids)

	# 消息并不是来自于需要同步的群
	# if not chatroom_id in chatroom_ids:
	# 	return

	#print "chatroom_id" + chatroom_id
	# 发送者的昵称
	#print "username",username
	#获取群名
	#print 11111, chatrooms_rename
	print("test get group name: "+str(group_name))

	#print group_name

	if msg['Type'] == TEXT:
		content = msg['Content']
		#print 1
	elif msg['Type'] == SHARING:
		content = msg['Text']
		#print 2

	# 根据消息类型转发至其他需要同步消息的群聊
	# if msg['Type'] == TEXT:
	# 	for item in chatrooms:
	# 		print(item)
	# 		#print 3
	# 		if not item['UserName'] == chatroom_id:
	# 			#print 4
	# 			itchat.send('%s—%s 说:\n%s' % (group_name,username, msg['Content']), item['UserName'])
	# # elif msg['Type'] == SHARING:
	# 	#print 5
	# 	for item in chatrooms:
	# 		if not item['UserName'] == chatroom_id:
	# 			itchat.send('%s-%s 分享：\n%s\n%s' % (group_name,username, msg['Text'], msg['Url']), item['UserName'])

# 自动回复图片等类别的群聊消息
# isGroupChat=True表示为群聊消息          
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)
def group_reply_media(msg):
	# 消息来自于哪个群聊
	chatroom_id = msg['FromUserName']
	# 发送者的昵称
	username = msg['ActualNickName']

	# 消息并不是来自于需要同步的群
	# if not chatroom_id in chatroom_ids:
	# 	return

	# 如果为gif图片则不转发
	if msg['FileName'][-4:] == '.gif':
		return

	# 下载图片等文件
	msg['Text'](msg['FileName'])
	# 转发至其他需要同步消息的群聊
	for item in chatrooms:
		if not item['UserName'] == chatroom_id:
			itchat.send('这是一个自动转发机器人\n @%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), item['UserName'])

# 扫二维码登录
#itchat.auto_login(hotReload=False)
itchat.auto_login(enableCmdQR=2)
# 获取所有通讯录中的群聊
# 需要在微信中将需要同步的群聊都保存至通讯录
chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
chatroom_ids = [c['UserName'] for c in chatrooms]
# chatroom_rename={}
print ('正在监测的群聊：', len(chatrooms), '个')
# print("chatroom_ids: "+ str(chatroom_ids))
#更改群名 ：  交流群+i
i=2
#for k in chatrooms.keys():
chatrooms_rename={}
for item in chatrooms:
	chatrooms_rename[str(item['UserName'])]=item['NickName']
	#print item['NickName']
	#print item['UserName']
	#print "交流群"+str(i)
	#item['Nickname']=str(i)

	i=i-1
	print (item['NickName'])
	# print (chatrooms_rename[item['UserName']])
#重新命名之后的群名
print ('chatrooms_rename'+str(chatrooms_rename))
#原始群名
# print ' '.join([item['NickName'] for item in chatrooms])
# 开始监测
itchat.run()