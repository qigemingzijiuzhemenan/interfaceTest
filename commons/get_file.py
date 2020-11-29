import os


#判断文件夹是否存在，若不存在则创建一个
def create_path(path):
    a=os.path.isdir(path)
    if a is False:
        os.makedirs(path)
        
#获取文件夹内所有文件的名称
def get_filename(pach_1):
    filenames=[]
    filename = pach_1
    for pach,dirs,files in os.walk(filename):
        file = files
        for b in file:
            c=b
            # filenames.append(pach_1+"\\"+c)#绝对路径
            filenames.append(c)#仅仅为名称
            # print(c)
    return filenames
# 获取文件夹内所有文件夹的名称
def get_filepach(pach_1):
    fd_pachs=[]
    filename = pach_1
    for pach,dirs,files in os.walk(filename):
        file1 = dirs
        # print(pach)
        # print(dirs)
        for b in file1:
            fd_pachs.append(b)
    return fd_pachs

#读取文件内容
def get_filedata(filepath):
    file=open(filepath,'rb')
    return file.read()


# filepath='C:\\Users\\admin\\Desktop\\测试信息\\浓烟明火\\mh001'
# a=get_filename(filepath)
# c=1
# for i in a:
#     oldpath=filepath+"\\"+i
#     newpath=filepath+"\\"+"mh%s.jpg"%str(c)
#     os.rename(oldpath,newpath)
#     c+=1

# path='D:\\铜陵\\AI\\海康AI效果评估\\渣土车未加盖'
# filepath='D:\\铜陵\\AI\\海康AI效果评估\\渣土车未加盖\\744344373_date_2019-04-25 03_39_30.jpg'
# filepath2=get_filename(path)
# print(filepath2)
# print(len(filepath2))
# num=1
# for i in filepath2:
#     a,b=get_filedata(filepath),get_filedata(i)
#     if a==b and i !=filepath:
#         print(i)
#         print("图片相同")
#         os.remove(i)#删除此图片
    # else:
    #     print("图片不同")