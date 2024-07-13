import threading
import time

import wx
from socket import  socket,AF_INET,SOCK_STREAM

class YsjServer(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,id=1002,title='服务器端界面',pos=wx.DefaultPosition,size=(400,500))
        #添加面板
        pl=wx.Panel(self)
        #添加盒子
        box=wx.BoxSizer(wx.VERTICAL)
        #添加网格布局
        fgz1=wx.FlexGridSizer(wx.HSCROLL)
        #添加按钮
        start_server_btn=wx.Button(pl,size=(133,40),label='启动服务')
        record_btn=wx.Button(pl,size=(133,40),label='保存聊天记录')
        stop_server_btn=wx.Button(pl,size=(133,40),label='停止服务')

        #把按钮放到网格布居中
        fgz1.Add(start_server_btn,1,wx.TOP)
        fgz1.Add(record_btn, 1, wx.TOP)
        fgz1.Add(stop_server_btn, 1, wx.TOP)

        #放到box中
        box.Add(fgz1,1,wx.ALIGN_CENTRE)


        #只读多行文本
        self.show_text=wx.TextCtrl(pl,size=(400,410),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.show_text,1,wx.ALIGN_CENTRE)

        #盒子放到面板中
        pl.SetSizer(box)


        '''_____________________________________________________窗口界面显示部分___________________________'''
        self.isOn=False #服务器默认启动状态
        self.host_port=('',8888)#空字符串代表本机所有ip
        #创建socket对象
        self.server_socket=socket(AF_INET,SOCK_STREAM)
        #绑定ip和端口号
        self.server_socket.bind(self.host_port)
        #监听
        self.server_socket.listen(5)
        #创建字典，存储与客户端对话的绘画线程
        self.session_thread_dict={}#用客户端名称做key，创建的线程做value

        #启动服务事件
        self.Bind(wx.EVT_BUTTON,self.start_server,start_server_btn)
        # 保存聊天记录服务事件
        self.Bind(wx.EVT_BUTTON, self.save_record, record_btn)
        # 断开服务事件
        self.Bind(wx.EVT_BUTTON, self.stop_server, stop_server_btn)

    def stop_server(self):
        #改变服务器的状态
        print('服务器已停止服务')
        self.isOn=False

    def save_record(self,event):
        #获取制度文本框中的内容
        record_data=self.show_text.GetValue()
        with open('record.log','w',encoding='utf-8') as file:
            file.write(record_data)

    #启动服务事件
    def start_server(self,event):
        print('启动服务的按钮点击成功')
        #判断服务器是否已经启动
        if not self.isOn:
            self.isOn=True
            #创建主线程
            main_thread=threading.Thread(target=self.do_work)
            #设置为守护线程，父线程执行结束，窗口界面关闭子线程也关闭
            main_thread.daemon=True
            #启动主线程
            main_thread.start()

    def do_work(self):
        #判断isOn
        while self.isOn:
            #接受客户端的连接请求
            session_socket,client_addr=self.server_socket.accept()
            #客户端发送请求之后第一条数据是客户端的名称,名称作为key
            user_name=session_socket.recv(1024).decode('utf-8')
            #创建一个会话线程对象
            sesstion_thread=SesstionThread(session_socket,user_name,self)
            #存储到字典当中
            self.session_thread_dict[user_name]=sesstion_thread
            #启动回话线程
            sesstion_thread.start()
            #当有客户端连接进来，输出服务器的提示信息
            self.show_info_and_send_client('服务器通知',f'欢迎{user_name}进入聊天室',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
        #条件不成立则关闭线程
        self.server_socket.close()

    def show_info_and_send_client(self,data_source,data,date_time):
        #字符串拼接
        send_data=f'{data_source}:{data}\n时间{date_time}'
        #只读文本框
        self.show_text.AppendText('-'*40+'\n'+send_data+'\n')
        #给每一个客户端都发送一次
        for client in self.session_thread_dict.values():
            #用每一个连接客户的对象
            if client.isOn:
                client.client_socket.send(send_data.encode('utf-8'))



class SesstionThread(threading.Thread):
    def __init__(self,client_socket,user_name,server):
        #调用父类初始化方法
        threading.Thread.__init__(self)
        self.client_socket=client_socket
        self.user_name=user_name
        self.server=server
        self.isOn=True

    def run(self)->None:
        print(f'客户端{self.user_name}和服务器连接成功')
        while self.isOn:
            #接受客户端的数据存入data
            data=self.client_socket.recv(1024).decode('utf-8')
            #如果客户端是点击断开连接，给服务器发一句话用来判断
            if data=='Y-disconnect-SJ':
                self.isOn=False
                #发送一条离开聊天室的通知
                self.show_info_and_send_client('服务器通知', f'{self.user_name}离开聊天室',
                                               time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

            else:
                #显示给所有其他客户端，包括服务器端
                self.server.show_info_and_send_client(self.user_name,data,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
        #关闭socket
        self.client_socket.close()


if __name__ == '__main__':
    app=wx.App()
    server=YsjServer()
    server.Show()

    app.MainLoop()