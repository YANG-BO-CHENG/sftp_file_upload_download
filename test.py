import tkinter as tk
from tkinter import ttk
import paramiko
from tkinter import filedialog
from tkinter import messagebox
class SFTPTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SFTP文件傳輸")
        self.root.geometry('200x300')
        self.root.configure(background="pink")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.connect_page = ttk.Frame(self.notebook)
        self.notebook.add(self.connect_page,text="FTSP連線伺服器")
        self.create_connect_page()

        self.upload_page = ttk.Frame(self.notebook)
        self.notebook.add(self.upload_page,text="上傳")
        self.create_upload_page()

        self.download_page = ttk.Frame(self.notebook)
        self.notebook.add(self.download_page,text="下載")
        self.create_download_page()
        
       
    def create_connect_page(self):
        self.host_label = tk.Label(self.connect_page, text="IP:")
        self.host_label.pack()
        
        self.host_entry = tk.Entry(self.connect_page)
        self.host_entry.pack()

        self.user_label = tk.Label(self.connect_page, text="帳號:")
        self.user_label.pack()

        self.user_entry = tk.Entry(self.connect_page)
        self.user_entry.pack()

        self.password_label = tk.Label(self.connect_page, text="密碼:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.connect_page, show="*")
        self.password_entry.pack()

        self.connect_button = tk.Button(self.connect_page, text="連接", command=self.connect_sftp)
        self.connect_button.pack()
        
        self.disconnect_button = tk.Button(self.connect_page, text="取消連接", command=self.disconnect_sftp)
        self.disconnect_button.pack()

    def create_upload_page(self):
        upload_label_directory = tk.Label(self.upload_page, text="選擇要放置的目錄:")
        upload_label_directory.pack()
        self.upload_directory_entry = tk.Entry(self.upload_page)
        self.upload_directory_entry.pack()
        upload_directory_button = tk.Button(self.upload_page, text="選擇目錄", command=self.select_upload_directory)
        upload_directory_button.pack()
        upload_label_file = tk.Label(self.upload_page, text="選擇要上傳的文件:")
        upload_label_file.pack()
        self.upload_file_entry = tk.Entry(self.upload_page)
        self.upload_file_entry.pack()
        upload_file_button = tk.Button(self.upload_page, text="選擇文件", command=self.select_upload_file)
        upload_file_button.pack()
        upload_button = tk.Button(self.upload_page, text="上傳文件", command=self.upload_file)
        upload_button.pack()


    def select_upload_directory(self):
        try:
           remote_directory = self.sftp.getcwd()
        except Exception as e:
           messagebox.showerror("錯誤", f"無法獲取遠端伺服器目錄: {str(e)}")
           return
        local_directory = filedialog.askdirectory(title="選擇要放置的目錄", initialdir=remote_directory)
        if local_directory:
           self.upload_directory_entry.delete(0, tk.END)
           self.upload_directory_entry.insert(0, local_directory)

    def select_upload_file(self):
        upload_file = filedialog.askopenfilename(title="選擇要上傳的文件")
        if upload_file:
           self.upload_file_entry.delete(0, tk.END)
           self.upload_file_entry.insert(0, upload_file)

    def upload_file(self):
        remote_directory = self.upload_directory_entry.get()
        local_file = self.upload_file_entry.get()
        if remote_directory and local_file:
           try:
              self.sftp.put(local_file, f"{remote_directory}/{local_file.split('/')[-1]}")
              messagebox.showinfo("上傳成功", "文件成功上傳")
           except Exception as e:
              messagebox.showerror("上傳失敗", str(e))
    def create_download_page(self):
        download_label_directory = tk.Label(self.download_page, text="選擇要放置的目錄:")
        download_label_directory.pack()
        self.download_directory_entry = tk.Entry(self.download_page)
        self.download_directory_entry.pack()
        download_directory_button = tk.Button(self.download_page, text="選擇目錄", command=self.select_download_directory)
        download_directory_button.pack()
        download_label_file = tk.Label(self.download_page, text="選擇要下載的文件:")
        download_label_file.pack()
        self.download_file_entry = tk.Entry(self.download_page)
        self.download_file_entry.pack()
        download_file_button = tk.Button(self.download_page, text="選擇文件", command=self.select_download_file)
        download_file_button.pack()
        download_button = tk.Button(self.download_page, text="下載文件", command=self.download_file)
        download_button.pack()
    def select_download_directory(self):
        try:
           remote_directory = self.sftp.getcwd()
           print(remote_directory)
        except Exception as e:
           messagebox.showerror("錯誤", f"無法獲取遠端伺服器目錄: {str(e)}")
           return
        local_directory = filedialog.askdirectory(title="選擇要放置的目錄", initialdir=remote_directory)
        if local_directory:
           self.download_directory_entry.delete(0, tk.END)
           self.download_directory_entry.insert(0, local_directory)

    def select_download_file(self):
        download_file = filedialog.askopenfilename(title="選擇要下載的文件")
        if download_file:
           self.download_file_entry.delete(0, tk.END)
           self.download_file_entry.insert(0, download_file)

    def download_file(self):
        remote_file = self.download_file_entry.get()
        local_directory = self.download_directory_entry.get()
        if remote_file and local_directory:
           try:
              self.sftp.get(remote_file, f"{local_directory}/{remote_file.split('/')[-1]}")
              messagebox.showinfo("下載成功", "文件成功下載")
           except Exception as e:
              messagebox.showerror("下載失敗", str(e))

    def connect_sftp(self):
        host     = self.host_entry.get()
        username = self.user_entry.get()
        password = self.password_entry.get()
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # transport = paramiko.Transport((host, 22))
            ssh.connect(host,username=username, password=password,allow_agent=False,look_for_keys=False)
            self.sftp = ssh.open_sftp()
            messagebox.showinfo("連接成功", "成功連接FSTP")
        except Exception as e:
            messagebox.showerror("連線失敗", str(e))
    def disconnect_sftp(self):
        self.sftp.close()
if __name__ == "__main__":
    root = tk.Tk()
    app = SFTPTransferApp(root)
    root.mainloop()
