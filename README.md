# EvadeHC
apply algorithm of this paper: 《Evading Classifiers by Morphing in the Dark. 》in evading PE files ML classifier. 

使用方法：
EvadeHC:
         此算法有三个超参数，q1, q2, theta. 算法以迭代的形式进行。每次迭代，维护一个集合C，集合C中包含q2个样本。初始化时，C中存储待改变的有害样本X0。每一次迭代中，对C中每一个样本，随机生成q1条改变路径。路径长暂定为10。如果某条改变路径中出现了成功规避的样本，则停止算法。否则，从路径中根据参数theta选择新的候选样本q2个加入C。
	具体算法如下：<br>
（1）对C中每个样本，产生q1条随机路径，令P为路径集合，清空C。<br>
（2）对 P 中每条路径 x, 进行<br>
        (a) 找到tester的翻转点mx, 使用二分搜索。<br>
        (b)根据公式score(mx, rx), 给定目标分数v0, 计算最大值 r’0使得score(mx,  r’0)> ＝v0。使用detector检测样本x[r’0]， 若样本检测为无害，则score一定大于等于  v0（因为翻转点必定先于r’0）。<br>
         (c)若score大于等于 v0,将 x[mx*theta] 加入C。<br>
（3）若C 中样本不足q2个，则重复（1）（2）直到C中样本数为q2。<br>
（4）通过前三个步骤，已经得到 q2个score不小于v0的样本了。此时，增大v0,再重复(1)~(3),直到v0为正，此时规避成功。<br>

公式: <br>
score(mx, rx) = mx - rx.  即tester翻转点到detector翻转点的距离。 如果score大于0，即detector的翻转点先于文件的有害性消失点，即规避成功。<br>

实验中，选择参数为： q1=20 q2=5 theta=0.5 。 v0初始值为-1, 第二轮增加到1。对每条路径，需查询testor 4次，detector 1 次。理想状态下，共需查询 testor 约280次，detector 70 次。<br>


<br>
多线程版本：<br>
      多线程主要使用在原始版本的步骤（2）中，为每一个路径分配了一个线程，即查询时，每条路径同步查询。速度大概能提升q1倍。<br>
