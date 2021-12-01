import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import time
import operator
DNA_SIZE = 24
POP_SIZE = 200
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.005
N_GENERATIONS = 100

'''
实际上是没有需求需要将一个十进制数转化为一个二进制数，而在最后我们肯定要将编码后的二进制串转换为我们理解的十进制串，
所以我们需要的是y=f(x)y=f(x)的逆映射，也就是将二进制转化为十进制，
这个过程叫做解码（很重要，感觉初学者不容易理解），理解了解码编码还难吗?先看具体的解码过程如下。
'''
'''
首先我们限制二进制串的长度为10（长度自己指定即可，越长精度越高），例如我们有一个二进制串（在程序中用数组存储即可）
[0,1,0,1,1,1,0,1,0,1][0,1,0,1,1,1,0,1,0,1]
，这个二进制串如何转化为实数呢？不要忘记我们的x,y∈[−3,3]这个限制，
我们目标是求一个逆映射将这个二进制串映射到x,y∈[−3,3]即可，
为了更一般化我们将x,y的取值范围用一个变量表示，在程序中可以用python语言写到：
'''
XBOUND = [-3,3]
YBOUND = [-3,3]

def F(x,y):
    return 3*(1-x)**2*np.exp(-(x**2)-(y+1)**2)- 10*(x/5 - x**3 - y**5)*np.exp(-x**2-y**2)- 1/3**np.exp(-(x+1)**2 - y**2)

def plot_3d(ax):
    X = np.linspace(*XBOUND, 100)
    Y = np.linspace(*YBOUND, 100)
    X,Y = np.meshgrid(X, Y)
    Z = F(X, Y)
    ax.plot_surface(X,Y,Z,rstride=1,cstride=1,cmap=cm.coolwarm)
    ax.set_zlim(-10,10)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.pause(3)
    plt.show()


'''
种群和个体的概念

遗传算法启发自进化理论，而我们知道进化是由种群为单位的，种群是什么呢？维基百科上解释为：
在生物学上，是在一定空间范围内同时生活着的同种生物的全部个体。显然要想理解种群的概念，又先得理解个体的概念，
在遗传算法里，个体通常为某个问题的一个解，并且该解在计算机中被编码为一个向量表示！ 
我们的例子中要求最大值，所以该问题的解为一组可能的(x,y)
(x,y)的取值。比如(x=2.1,y=0.8),(x=−1.5,y=2.3)...(x=2.1,y=0.8),(x=−1.5,y=2.3)...就是求最大值问题的一个可能解，
也就是遗传算法里的个体，把这样的一组一组的可能解的集合就叫做种群 ，比如在这个问题中设置100个这样的x,yx,y的可能的取值对，
这100个个体就构成了种群。
————————————————
版权声明：本文为CSDN博主「重学CS」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/ha_ha_ha233/article/details/91364937

编码、解码与染色体的概念

在上面个体概念里提到个体（也就是一组可能解）在计算机程序中被编码为一个向量表示，而在我们这个问题中，个体是x,y

x,y的取值，是两个实数，所以问题就可以转化为如何将实数编码为一个向量表示，可能有些朋友有疑惑，实数在计算机里不是可以直接存储吗，为什么需要编码呢？这里编码是为了后续操作（交叉和变异）的方便。实数如何编码为向量这个问题找了很多博客，写的都是很不清楚，看了莫烦python的教学代码，终于明白了一种实数编码、解码的方式。

生物的DNA有四种碱基对，分别是ACGT，DNA的编码可以看作是DNA上碱基对的不同排列，不同的排列使得基因的表现出来的性状也不同（如单眼皮双眼皮）。在计算机中，我们可以模仿这种编码，但是碱基对的种类只有两种，分别是0，1。只要我们能够将不同的实数表示成不同的0，1二进制串表示就完成了编码，也就是说其实我们并不需要去了解一个实数对应的二进制具体是多少，我们只需要保证有一个映射
y=f(x),x is decimal system,y is binary system
能够将十进制的数编码为二进制即可，至于这个映射是什么，其实可以不必关心。将个体（可能解）编码后的二进制串叫做染色体，染色体（或者有人叫DNA）就是个体（可能解）的二进制编码表示。为什么可以不必关心映射f(x)

f(x)呢？因为其实我们在程序中操纵的都是二进制串，而二进制串生成时可以随机生成，如：

#pop表示种群矩阵，一行表示一个二进制编码表示的DNA，矩阵的行数为种群数目,DNA_SIZE为编码长度

'''
# pop = np.random.randint(2,size=(POP_SIZE,2*DNA_SIZE))
# print(pop)#matrix (POP_SIZE, DNA_SIZE*2)
# print(type(pop))
# print(pop.shape)



'''
为将二进制串映射到指定范围，首先先将二进制串按权展开，将二进制数转化为十进制数，
我们有0∗29+1∗28+0∗27+...+0∗20+1∗20=3730∗29+1∗28+0∗27+...+0∗20+1∗20=373，
然后将转换后的实数压缩到[0,1]之间的一个小数，373/（210−1）≈0.36461388074，
通过以上这些步骤所有二进制串表示都可以转换为[0,1]之间的小数，现在只需要将[0,1]
区间内的数映射到我们要的区间即可。假设区间[0,1]内的数称为num，转换在python语言中可以写成：
#X_BOUND,Y_BOUND是x，y的取值范围 X_BOUND = [-3, 3], Y_BOUND = [-3, 3],
'''
# x = num*(XBOUND[-1] - XBOUND[0])+XBOUND[0]
# y = num2*(YBOUND[-1] - YBOUND[0])+YBOUND[0]

'''
通过以上这些标记为蓝色的步骤我们完成了将一个二进制串映射到指定范围内的任务（解码）。

现在再来看看编码过程。不难看出上面我们的DNA（二进制串）长为10，10位二进制可以表示2^10种不同的状态，
可以看成是将最后要转化为的十进制区间x,y∈[−3,3]（下面讨论都时转化到这个区间）切分成2^10份，显而易见，如果我们增加二进制串的长度，
那么我们对区间的切分可以更加精细，转化后的十进制解也更加精确。例如，十位二进制全1按权展开为1023，最后映射到[-3, 3]区间时为3，
而1111111110（前面9个1）按权展开为1022，1022/(210−1)≈0.9990221022/(210−1)≈0.999022，0.999022∗(3−(−3))+(−3)≈2.994134
如果我们将实数编码为12位二进制，111111111111（12个1）最后转化为3，
而111111111110（前面11个1）按权展开为4094，4094/(212−1=4095)≈0.999756，0.999755∗(3−(−3))+(−3)≈2.998534;
而3−2.994134=0.005866；3−2.998534=0.0014663−2.998534=0.001466，可以看出用10位二进制编码划分区间后，
每个二进制状态改变对应的实数大约改变0.005866，而用12位二进制编码这个数字下降到0.001466，
所以DNA长度越长，解码为10进制的实数越精确。

以下为解码过程的python代码：

这里我设置DNA_SIZE=24（一个实数DNA长度），两个实数x,y
x,y一共用48位二进制编码，我同时将x和y编码到同一个48位的二进制串里，
每一个变量用24位表示，奇数24列为x的编码表示，偶数24列为y的编码表示。
'''
#解码函数：
def translateDNA(pop):
    print(pop.shape)
    #pop表示种群矩阵，一行表示一个二进制编码表示的DNA，矩阵的行数为种群数目：
    x_pop = pop[:,1::2]#从第1列开始，步进为2
    y_pop = pop[:,::2]#从第0列开始，步进为2
    # #pop:(POP_SIZE,DNA_SIZE)*(DNA_SIZE,1) --> (POP_SIZE,1)完成解码:二进制码求相应十进制值然后压缩到相应范围内即可完成解码
    x = x_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(XBOUND[-1] - XBOUND[0])+XBOUND[0]
    y = y_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(YBOUND[-1] - YBOUND[0])+YBOUND[0]

    return x,y

#计算适应度
'''
pred是将可能解带入函数F中得到的预测值，因为后面的选择过程需要根据个体适应度确定每个个体被保留下来的概率
，而概率不能是负值，所以减去预测中的最小值把适应度值的最小区间提升到从0开始，但是如果适应度为0，
其对应的概率也为0，表示该个体不可能在选择中保留下来，这不符合算法思想，
遗传算法不绝对否定谁也不绝对肯定谁，所以最后加上了一个很小的正数。
————————————————
版权声明：本文为CSDN博主「重学CS」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/ha_ha_ha233/article/details/91364937
'''
def get_fitness(pop):
    x,y = translateDNA(pop)
    pred = F(x,y)
    return (pred - min(pred))+1e-4 ##减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)],最后在加上一个很小的数防止出现为0的适应度

'''
相应地，计算最小适应度优先的函数如下：
'''
def get_fitness_min(pop):
    x,y = translateDNA(pop)
    pred = F(x,y)
    return (-1)*(pred - max(pred))+1e-4

    # return x,y
    # print(x.shape)

'''
有了评估的适应度函数，下面可以根据适者生存法则将优秀者保留下来了。
选择则是根据新个体的适应度进行，但同时不意味着完全以适应度高低为导向
（选择top k个适应度最高的个体，容易陷入局部最优解），因为单纯选择适应度高的个体
将可能导致算法快速收敛到局部最优解而非全局最优解，我们称之为早熟。作为折中，
遗传算法依据原则：适应度越高，被选择的机会越高，而适应度低的，被选择的机会就低。 在python中可以写做：
————————————————
'''
def select(pop,fitness):
    idx = np.random.choice(np.arange(pop.shape[0]),size=POP_SIZE,replace=True,p=fitness/fitness.sum())
#     不熟悉numpy的朋友可以查阅一下这个函数，主要是使用了choice里的最后一个参数p，参数p描述了从np.arange(POP_SIZE)里选择每一个元素的概率，
#     概率越高约有可能被选中，最后返回被选中的个体即可。
#     print(idx)
#     k = set(idx)
#     pl = dict()
#     for id in k:
#         pl[id] = 0
#     for id in idx:
#         pl[id] = pl[id]+1
#     print(len(list(k)))
#     print(pl)

    return pop[idx]

'''
交叉、变异

通过选择我们得到了当前看来“还不错的基因”，但是这并不是最好的基因，我们需要通过繁殖后代（包含有交叉+变异过程）来产生比当前更好的基因，
但是繁殖后代并不能保证每个后代个体的基因都比上一代优秀，这时需要继续通过选择过程来让试应环境的个体保留下来，
从而完成进化，不断迭代上面这个过程种群中的个体就会一步一步地进化。
具体地繁殖后代过程包括交叉和变异两步。
交叉是指每一个个体是由父亲和母亲两个个体繁殖产生，
子代个体的DNA（二进制串）获得了一半父亲的DNA，一半母亲的DNA，但是这里的一半并不是真正的一半，
这个位置叫做交配点，是随机产生的，可以是染色体的任意位置。
通过交叉子代获得了一半来自父亲一半来自母亲的DNA，
但是子代自身可能发生变异，使得其DNA即不来自父亲，也不来自母亲，
在某个位置上发生随机改变，通常就是改变DNA的一个二进制位（0变到1，或者1变到0）。
需要说明的是交叉和变异不是必然发生，而是有一定概率发生。先考虑交叉，最坏情况，
交叉产生的子代的DNA都比父代要差（这样算法有可能朝着优化的反方向进行，不收敛），
如果交叉是有一定概率不发生，那么就能保证子代有一部分基因和当前这一代基因水平一样；
而变异本质上是让算法跳出局部最优解，如果变异时常发生，或发生概率太大，
那么算法到了最优解时还会不稳定。交叉概率，
范围一般是0.6~1，突变常数（又称为变异概率），通常是0.1或者更小。
'''
def crossover_and_mutation(pop,CROSS_RATE=0.8):
    new_pop = []
    i = 0
    pop_sizes = len(pop)
    for father in pop:
        # print(father)
        #遍历种群中的每一个个体，将该个体作为父亲
        #孩子先得到父亲的全部基因（这里我把一串二进制串的那些0，1称为基因）
        child = np.array(list(father)[:])
        i = i+1
        child2 = []
        # print(child.shape)
        cross = False
        if np.random.rand() < CROSS_RATE:
            cross = True
            # 产生子代时不是必然发生交叉，而是以一定的概率发生交叉
            mother = pop[np.random.randint(POP_SIZE)]#再种群中选择另一个个体，并将该个体作为母亲
            # if i == len(pop):
            #     i = 0
            # mother = pop[i]
            child2 = np.array(list(mother)[:])
            cross_points = np.random.randint(low=0,high=DNA_SIZE*2)#随机产生交叉的点
            child[cross_points:] = mother[cross_points:]#孩子得到位于交叉点后的母亲的基因
            child2[cross_points:] = father[cross_points:]
        mutation(child)  # 每个后代有一定的机率发生变异
        if cross:
            print(child2)
            print(child2.shape)
            mutation(child2)
            new_pop.append(child2)
        new_pop.append(child)
        # new_pop.append(child2)
        # print(child)
        # print(father)
        if not operator.eq(list(child),list(father)) and not operator.eq(list(child2),list(father)):
            new_pop.append(father)
    return np.array(new_pop)

def mutation(child, MUTATION_RATE=0.003):
    if np.random.rand() < MUTATION_RATE: 				#以MUTATION_RATE的概率进行变异
        mutate_point = np.random.randint(0, 2*DNA_SIZE-1)	#随机产生一个实数，代表要变异基因的位置
        child[mutate_point] = child[mutate_point]^1 	#将变异点的二进制为反转

def print_info(pop):
    fitness = get_fitness(pop)
    max_fitness_index = np.argmax(fitness)
    print("max_fitness:", fitness[max_fitness_index])
    x,y = translateDNA(pop)
    print("最优的基因型：", pop[max_fitness_index])
    print("(x, y):", (x[max_fitness_index], y[max_fitness_index]))

'''
上面这些步骤即为遗传算法的核心模块，将这些模块在主函数中迭代起来，让种群去进化
'''
if __name__ == '__main__':
    # #pop表示种群矩阵，一行表示一个二进制编码表示的DNA，矩阵的行数为种群数目,DNA_SIZE为编码长度
    # #生成种群 matrix (POP_SIZE, DNA_SIZE)
    fig = plt.figure()
    ax = Axes3D(fig)
    plt.ion()  # 将画图模式改为交互模式，程序遇到plt.show不会暂停，而是继续执行
    plot_3d(ax)
    pop = np.random.randint(2, size=(POP_SIZE, 2 * DNA_SIZE))#matrix (POP_SIZE, DNA_SIZE)
    print(pop)  # matrix (POP_SIZE, DNA_SIZE*2)
    print(type(pop))
    print(pop.shape)
    time1 = time.time()
    for _ in range(N_GENERATIONS+10):
        # 种群迭代进化N_GENERATIONS代
        # crossover_and_mutation(pop,CROSSOVER_RATE)
        x, y = translateDNA(pop)
        if 'sca' in locals():
            sca.remove()
        sca = ax.scatter(x, y, F(x, y), c='black', marker='o');
        plt.show();
        plt.pause(0.1)
        pop = crossover_and_mutation(pop, CROSSOVER_RATE)
        pop = np.array(pop)
        print(pop.shape)
        print("before selection: %d" % pop.shape[0])
        # F_values = F(translateDNA(pop)[0], translateDNA(pop)[1])#x, y --> Z matrix
        fitness = get_fitness(pop)
        pop = select(pop, fitness)  # 选择生成新的种群
        print("after selection: %d" % pop.shape[0])
    time2 = time.time()
    print(time2 - time1)
    print_info(pop)
    plt.ioff()
    plot_3d(ax)

    # x,y = get_fitness(pop)
    # print(x.shape)
