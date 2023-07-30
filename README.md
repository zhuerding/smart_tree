# Smart Tree Fucker

---
&nbsp;&nbsp;&nbsp;&nbsp;狂躁医学生不想刷网课？一学期12门网课，**医学院我![img.png](readme_img/img.png)老X（情绪过于激动被带走）……  
&nbsp;&nbsp;&nbsp;&nbsp;~~这是一款基于[Selenium](https://github.com/SeleniumHQ/selenium)开发https://github.com/ultralytics/yolov5自动刷智慧树网课的Python脚本。~~  
&nbsp;&nbsp;&nbsp;&nbsp;这是一款基于[YOLOv5](https://github.com/ultralytics/yolov5)框架开发的针对易盾空间验证码进行识别并破解的自动验证码处理工具。因为在开发该工具过程中发现已经有大佬[@VermiIIi0n](https://github.com/VermiIIi0n)从[后端](https://github.com/VermiIIi0n/fuckZHS)（*）进入智慧树深处，所以这个自动识别智慧树上的空间推理验证码工具也没有什么用处了，所以就不再开发刷网课的脚本，只把这个工具单独上传了。  
---
😅文件树：  
```
zhuerding
   └─smart_tree  
       ├─datasets    # 里面是训练YOLOv5的数据集，内部结构不再展示
       │
       ├─img         # 里面是用来测试的验证码及其文本内容
       │
       ├─mods        # 一些开发过程中随便写的小工具
       │     ├─ output  # 某个小工具的输出文件夹
       │     ├─ tutle   # 某个小工具的基础元件文件夹
       │     │    ├─ A-Z #  某个小工具的基础元件文件夹
       │     │    ├─ Xa-z #  某个小工具的基础元件文件夹
       │     │    ├─ background.jpg  #  某个小工具所需要的背景图
       │     │    ├─ predefined_classes.txt  #  某个小工具所需要的标签文件
       │     ├─ chromedrive.exe # 某个谷歌浏览器驱动