import threading

# coding:utf-8
import wx
from socket import socket,AF_INET,SOCK_STREAM
class YsjClient(wx.Frame):
    def __init__(self,client_name):
        #父类初始化方法
        #none没有父级窗口
        #id当前窗口恶一个编号
        #pos窗体的打开位置
        #size窗体的大小
        wx.Frame.__init__(self,None,id=1001,title=client_name+'的客户端界面',pos=wx.DefaultPosition,size=(400,450))
        #创建面板
        pl=wx.Panel(self)
        #在面板中放上盒子
        box=wx.BoxSizer(wx.VERTICAL)#垂直布局
        #可伸缩的网格布局
        fgz1=wx.FlexGridSizer(wx.HSCROLL)#水平方向布局

        #创建两个按钮
        conn_btn=wx.Button(pl,size=(200,40),label='连接')
        dis_conn_btn = wx.Button(pl, size=(200, 40), label='断开')

        #把两个按钮放到可伸缩的网格中
        fgz1.Add(conn_btn,1,wx.TOP | wx.LEFT)
        fgz1.Add(dis_conn_btn,1,wx.TOP | wx.RIGHT)

        #添加到box中
        box.Add(fgz1,1,wx.ALIGN_CENTRE)

        #只读文本框显示聊天内容
        self.show_text=wx.TextCtrl(pl,size=(400,210),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.show_text,1,wx.ALIGN_CENTRE)

        #创建聊天内容的文本框
        self.chat_text=wx.TextCtrl(pl,size=(400,120),style=wx.TE_MULTILINE)
        box.Add(self.chat_text,1,wx.ALIGN_CENTRE)

        #可伸缩的网格布局
        fgz2=wx.FlexGridSizer(wx.HSCROLL)#水平方向布局
        #创建两个按钮
        reset_btn=wx.Button(pl,size=(200,40),label='重置')
        send_btn = wx.Button(pl, size=(200, 40), label='发送')
        #把两个按钮放到可伸缩的网格中
        fgz2.Add(reset_btn,1,wx.TOP|wx.LEFT)
        fgz2.Add(send_btn,1,wx.TOP|wx.RIGHT)
        # 添加到box中
        box.Add(fgz2, 1, wx.ALIGN_CENTRE)

        #将盒子放到面板中
        pl.SetSizer(box)
        print('放到面板中')

        '''——————————————————————客户端界面————————————————————'''
        self.Bind(wx.EVT_BUTTON,self.connect_to_server,conn_btn)
        #实例属性设置
        self.client_name=client_name
        self.isConnected=False#客户端连接服务器的状态
        self.client_socket=None#设置客户端的socket对象为空
        #给发送按钮绑定事件
        self.Bind(wx.EVT_BUTTON, self.send_to_server, send_btn)
        #给断开按钮绑定事件
        self.Bind(wx.EVT_BUTTON, self.dis_conn_server, dis_conn_btn)
        # 给重置按钮绑定事件
        self.Bind(wx.EVT_BUTTON, self.reset, reset_btn)



    def reset(self):
        self.chat_text.Clear()#清空文本框

    def dis_conn_server(self):
        #发送端开信息
        self.client_socket.send('Y-disconnect-SJ'.encode('utf-8'))
        #改变连接状态
        self.isConnected=False

    def send_to_server(self,event):
        #判断连接状态
        if self.isConnected:
            #从可写文本框中读取数据
            input_data=self.chat_text.GetValue()
            if input_data!='':
                #向服务器发送数据
                self.client_socket.send(input_data.encode('utf-8'))
                #发完数据之后清除文本
                self.chat_text.SetValue('')
    def connect_to_server(self,event):
        #连接服务器
        print(f'客户端{self.client_name}连接服务器')
        #如果客户端没有连接服务器，则开始连接
        if not self.isConnected:
            #TCP编程
            server_host_port=('192.168.0.105',8888)
            #创建socket对象
            self.client_socket=socket(AF_INET,SOCK_STREAM)
            #发送连接请求
            self.client_socket.connect(server_host_port)
            #只要连接成功，把客户端名称发过去
            self.client_socket.send(self.client_name.encode('utf-8'))
            #启动另一个线程用来给服务器端通信
            client_thread=threading.Thread(target=self.recv_data)
            #设置为守护线程，窗口关闭，现成也结束
            client_thread.daemon=True
            #修改连接状态
            self.isConnected=True
            #启动线程
            client_thread.start()
    def recv_data(self):
        #判断是否连接
        while self.isConnected:
            #接收来自服务器的信息
            data=self.client_socket.recv(1024).decode('utf-8')
            #显示到文本框中
            self.show_text.AppendText('-'*40+'\n'+data+'\n')



if __name__ == '__main__':
    print('开始执行线程函数')
    # 初始化app()
    app = wx.App()
    client = YsjClient('窗口端口')
    client.Show()
    # 循环刷新显示
    app.MainLoop()
    print('线程函数执行结束')

