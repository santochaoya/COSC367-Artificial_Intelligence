# Learn Prolog Now! 随笔

# 第一章 - 事实、规则和查询

1. 基本规则

Prolog基本结构：**事实**（facts）， **规则**（rules），**查询**（queries）

**知识库**（knowledge base）：事实、规则。kb1.pl



**事实**：无条件为真的一些事物、状态或关系。happy(mia).



**规则**：有条件为真的一些事物、状态或关系。listen2music(mia) :- happy(mia).

	理解为：mia听音乐，如果mia高兴。

:- 理解为 做什么 :- 如果 或 以什么为前提

规则 ： head :- body，body部分为真，那么prolog就能推导head为真。

 推导的基础步骤 ：假言推理（modus ponens）

（only false：body false，head true）

==总结==： 一个假言推理的任何事实可以作为其他推理的输入，判断其他head的真假，通过链接的方式，得出所有推理结果。



**查询**：在?-后的输入



Prolog：

**?-** ：待输入符号

**.**：结束符

**，**：逻辑与

；：逻辑或（提高处理效率，但是会使可读性变差，也可以使用两个相同head的规则来表达		逻辑或）

空格：没有意义



**子句**（clauses）：在知识库中的事实和规则都称为子句。

**谓词**（predicates）：相当于知识库中的属性。

```perl
happy(yolanda).
listen2Music(mia).
listen2Music(yolanda) :- happy(yolanda).
playsAirGuitar(mia) :- listen2Music(mia).
playsAirGuitar(yolanda) :- listen2Music(yolanda).
```

示例中有三个谓词：happy、listen2Music、playsAirGuitar。

谓词happy是一个独立的子句：事实。

谓词listen2Music是两个子句：事实、规则。

谓词playsAirGuitar是两个子句：两个规则。



**变量的使用**

**变量**：大写字母开头的单词

查询时输入带有变量的事实或者规则，prolog会返回变量所代表的值，再输入；，prolog会输出第二个变量代表的值，依次往下知道输出所有值后，prolog会返回false。



事实、规则和查询又是由语句（term）构成：原子（Atoms）、数字（numbers)、变量（Variables）、复杂语句（Complex Terms）



**原子（Atoms）** ：

* 字符串 : 

  大写字母、小写字母、数字、下划线

  * 头字符：必须是小写字母

* 单引号封装的字符序列：'Vincent'，'The Gimp'，' '（空格符）
* 特殊字符组成的字符串：@==，：-，，等

**变量（Variables）**：

* 头字符必须是大写字母或者下划线

* 下划线 _ 可以单独作为一个变量，**匿名变量**， 可以代指任意值。


**复杂语句（Complex Terms）**：

* 函子(Factor) + 参数序列：loves(vincent, mia)，

  * **函子**：loves
  * 必须是原子。
  * **参数序列**：vincent，mia

  - 必须放在小括号内，有英文逗号分隔，紧跟在函子后，不应有空格。参数序列可以是变量、复杂语句等任意类型的语句。

* **元数**（arity）：参数的个数

  loves/2

  **注意**：Prolog允许定义函子相同的复杂语句，但是元数必须不同。loves(vincent, mia)和loves(aby, kobe, wasabi)是两个不同的函子，分别是loves/2和loves/3。



第一章习题：

1.1 原子、变量、原子、变量、原子、原子、都不是、原子、变量、原子

1.2 

1. 复杂语句，函子：loves，元数：2
2. 原子
3. 都不是
4. 复杂语句，函子：boxer，元数：1
5. 复杂语句，函子：and，元数：2
6. 复杂语句，函子：and，元数：2
7. 都不是
8. 都不是
9. 都不是
10. 都不是

1.3 

1. 事实：3

2. 规则：4

3. 子句：7

4. 谓词：5 ==**谓词有7个：每个动词都是谓词，即使出现在规则的body部分**==

5. 规则的头部：person(X)，loves(X, Y)，father(Y, Z)，father(Y, Z)==（**重复的头部依然要列出来**）==

6. 规则的目标：man(X); woman(X)，father(X, Y)，man(Y), son(Z, Y)和man(Y), daughter(Z, Y).


1.4

1. killer(Butch).
2. married(Mia, Marsellus).
3. dead(Zed).
4. kills(Marsellus, X) :- gives_a_footmassage(Mia, X).
5. loves(Mia, X):-good_dancer(X).
6. eats(Jules, X):-nutritious(X), tasty(X).

1.5

1. ture

2. false ==(ERROR: Undefined procedure: witch/1 (DWIM could not correct goal)==

3. false

4. false==(ERROR)==

5. true

6. Y=ron;

   Y=harry.

7. false==(ERROR)==



## 第二章 合一和证明搜索

### 1.合一（Unification）

* 语句类型：

  * **常量**：==原子==和==数字==

  * **变量**

  * **复杂语句**


* 能够合一的两个语句**必须**：

  * 是==相同==语句：

    mia和mia，可以合一

    mia和vinecnt，不可以合一

  * 如果语句中有变量，可以通过变量初始化后变相同的语句：

    mia和X，可以合一

    loves（X，mia）和loves（vincent，X）不可以合一，无法通过对X初始化是的两个复杂语句相同。



**定义**：term1和term2能否Unification？

1. 都是常量：具有相同原子或数字
2. term1是变量，term2是任意语句：term1能初始化成term2

3. 都是复杂语句：
   * 具有相同函子和元数，且
   * 所有对应参数能合一，且
   * 变量初始化后能匹配。



Prolog 语句：=/2，测试两个参数是否合一

*Examples*

```perl
?- =(mia, mia).
true.
#same atoms

?- =(mia, vincent).
false.
#different atoms

?- =('mia', mia).
true.
#in Prolog, all the 'symbols' is known as symbols.

?- '2' = 2.
false.
#in Prolog, '2' is a atom, 2 is a number.

?- mia = X.
X = mia
#variable initilise

?- X = Y.
X = _2435;
Y = _2435;
true.
#_2435 is a variable, prolog means X and Y share the same value.

?- X = mia, X = vincent.
false.

?- k(s(g), Y) = k(X, t(k)).
X = s(g);
Y = t(k).

?- lovse(X, X) = loves(mia, vincent).
false.

?- father(X) = X.
X = father(X).
#recursion
"""
   in standard unification algorithm, it can no be unification:
	 as initilise, X = father(X), 
	 meanwhile,  on the leftside X = father(X),
	 but 		on the rightside, X = father(father(X)).
	 X can not be initilised to the same, can not be unification.
   in the ancient Prolog, it will be exhaust the memory:
     as initilise, X = father(X),
     meanwhile,  on the leftside X = father(X),
    			on the rightside X = father(father(X)),
     then prolog will force the leftside X = father(father(X)),
     then				on the rightside X = father(father(father(X))),
     Prolog will give: Not enough memory to complete query!
   in the modern Prolog, it will be simplified:
     X = father(X).
"""
```



最后一个例子不同的原因：

* 标准合一算法进行一个==触发检验（the occurs check）==：

  * 如果一个变量和一个语句进行合一：首先检验变量是否在语句中， 如果在，则不能合一；

  * **优点**：不会出现死锁现象，因为检验在前；
  * **缺点**：每次执行语句之前进行触发检验会降低速度，因为大部分不会死锁。

* Prolog合一算法为了提高速度，每次开始前不会进行触发检验，但是可以通过语句：

  ?- unify_with_occur_check(father(X), X). 来执行这一步。

