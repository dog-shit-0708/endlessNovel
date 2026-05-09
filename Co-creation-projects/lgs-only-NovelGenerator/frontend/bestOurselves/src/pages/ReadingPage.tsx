import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ChevronLeft, ArrowRight, Share2, Heart, MessageCircle, Settings, Minus, Plus } from "lucide-react";
import { Link, useParams, useLocation } from "react-router-dom";
import ReactMarkdown from "react-markdown";

const CHAPTER_DATA: Record<string, { title: string; subtitle: string; content: string; date: string }> = {
  "1": {
    title: "第一章 耿耿",
    subtitle: "最好的我们 • No.1",
    date: "2010.09.01",
    content: `
No.1

我叫耿耿。

亲戚们都说这名字不好，劲儿劲儿的，好像憋着一口气跟谁过不去似的。

但是我喜欢。名字好不好听是其次，叫习惯了还不都是一样。真正重要的，是这个名字中倾注的心意。

我爸我妈都姓耿，估计他们起名字的时候脑子里转悠的是“强强联合”“爱情结晶”一类很美好的念头，所以我叫耿耿。

不过，后来他们离婚了。

所以，我也不确定我对自己姓名的解读，是不是一场一厢情愿。

No.2

我中考那年赶上非典，全市各行各业一片兵荒马乱，而我作为普通初中的普通学生，很不厚道地发了国难财。

中考英语取消听力部分，数学难度大幅降低，语文作文形式竟然回归了命题作文，物理、化学占总分的比例降低……这直接导致了历次模考从来就没进过班级前三的耿耿同学，竟然在初升高统考中考了全校第三名。

后来，我们班同学非拉着我在本市阿迪达斯旗舰店门口合影。

他们说，这代表着IMPOSSIBLE IS NOTHING，一切皆有可能。

然后，又让我举着振华中学大红色的录取通知书在耐克门口留影。

他们说，这张又代表了“JUST DO IT”的精神。

我问他们知不知道JUST DO IT的含义，他们说，怎么不知道？做掉他！

我最终没能做掉振华。这都是后话了。而且在我很郁闷的那段时间，听闻阿迪达斯因为某件吃瘪的事情，一怒之下将广告语改名为NOTHING IS POSSIBLE.

这才是真相。世界上唯一不变的就是变化，世界上唯一可能的就是不可能。

No.3

我们初升高是考前报志愿，我当时填报的三项是振华校本部、振华自费、振华分校。

记得当时交志愿表的时候，我是最后一个递给老师的，遮遮掩掩地，生怕别人看见。

要知道，我们班的万年第一名都没敢报振华。她纠结了很长时间，还是跟师大附中高中部签了合同，只要第一志愿报师大附中，中考录取分数线就为她降十分。

年复一年，师大附中就是用这种方式劫走了一批具有考上振华的可能却又对自己缺乏自信的优等生。

初三的时候每次考试结束，我们班同学都会在她面前起哄说，她是振华苗子。我们自然没有恶意，可是中考前最后一次模考之后，她因为这个玩笑而大发脾气。

不少人因此而觉得她无理取闹、不识抬举、矫情……所有的词语像不散的烟云在女厕所的上空飘啊飘。我站在隔板边上听着她们说三道四，却不敢说出那句“其实我理解她”。

对，我的确理解她。我们不负责任地用几句轻飘飘的赞许将人家捧得高高的，但是万一摔下来，谁也不会去接住她。

后来跟我爸说起这件事，我爸非常马后炮地评价道，耿耿啊，你那时候就具备考上振华的心理条件了。你能从振华苗子的角度来考虑问题，很好。

你他妈放屁……我突然想起他是我爸，不是我同桌，连忙把同学间的口头禅憋进肚子里。

No.4

三个志愿连着填振华的方法就是我爸爸坚持的。振华分校的分数线比校本部低了几十分，但也能分到优秀教学资源的一杯羹。我爸的目标是让我保住分校，力争自费。

说不定有可能进校本部。

我打断了他，爸，这种事情要是真的发生了，一定会付出什么代价的，比如，折寿。

后来，我竟然真的稀里糊涂地进了校本部。

振华的校本部啊！

阎王就这样强行地贷给了我高利贷，我似乎眼睁睁地看着自己人生的进度条“嗖”地一下就短了一大截。

No.5

我们班主任说，放眼整个十三中，报了振华的似乎只有三个人，一个是七班的余周周，一个是二班的沈屾，另一个就是我。

沈屾最终考试失利。那个女生是传闻中上厕所蹲坑都要带着单词本背英文固定词组的牛人，三年如一日换来这种结果，我不知道该说什么。

当我大夏天蹲在肯德基门口，舔着新出的彩豆甜筒躲避日头的时候，抬起头无意中看到路过的沈屾。她没有打遮阳伞，也没有刻意躲避毒辣的日头，依旧背着鼓鼓囊囊的大书包，脸上有油光，额上有痘痘。

她偏过头看了我一眼，没有停步，眼神很平静，就像看一个路人。

却看得我心惊。

或许是我心虚。人家可能根本不知道我是哪根葱。

但我感觉自己抢了人家的甜筒，还笑嘻嘻地蹲在墙角舔得正欢。

后来才知道她去上补课班。中考结束对我来说是心中一块石头落地，但是对很多未雨绸缪的优等生来说，新的战役刚刚打响。沈屾她们整个暑假都在提前学习高一课程，讲课的老师都是振华响当当的名师。

是的，不管甜筒在谁手里，沈屾还是沈屾。

我突然特羡慕她。

她是一个能让人记住的人。无论别人是否喜欢她，十年后回忆起来，她还是沈屾，每一个动作、每一个坚持都是沈屾。

我呢？他们会说，就是那个，那个中考时候点儿正得不行的女生。

当天晚上，我少女的惆怅让我给我妈打了一个电话。

我妈用一贯的快语速教训我：“她考试的时候心理素质差，跟你有什么关系？我看你就是吃饱了撑的！”

我妈从来不同情失败者。

所以她跟我爸离婚了。

No.6

在挂电话前，我妈说，我中考的志愿是我爸从和她结婚到离婚的十几年中办过的唯一成功的事情。

我心想，为了我爸的荣誉，我折寿就折寿了吧。

我妈总说，如果她有时间，就亲自抚养我。

因为看到我懒懒散散的样子越来越像我爸，她觉得不能容忍。

听说，当年他们结婚的时候，我奶奶强烈反对。算命的说，我爸妈八字不合，我妈命硬，克夫，老人家很信这一套。

我妈家境不好，好强争气的性格让她的一举一动都验证了算命先生的判断。传闻会亲家的饭桌上，因为奶奶不经意地显摆自己家条件好，暗示妈妈攀高枝，导致妈妈脾气爆发，现场一度失控。

我很奇怪，都到这个地步了，他们怎么最后还是结婚了？

面对我的疑问，爸妈都轻描淡写。

我妈说，他非要娶我，跟你爷爷奶奶都翻脸了。

我那时候小，还特傻缺地追问：“为啥？”

我妈眉毛都竖起来了：“怎么，你妈我不值得他娶？”

那时候，我爸傻呵呵地笑：“又漂亮又能干，当然值得。”

没出息。

我想象不出脾气超好的老爸跟长辈翻脸的样子。我妈总说他窝囊。

可是，他为她翻脸抗争。

他最帅的那一刻，她竟然没往心里去。

No.7

我妈妈凭借自己的能力，一路爬到了市分行的高层，负责中小企业贷款业务，打拼到一身亚健康慢性病。反观“金融世家”的老爸，倒是一直在市委大院的政策研究室里面混着，养养花鸟鱼，打打太极拳。

我从长相到性格、能力到智商，全都像我爸。

总而言之，我老妈的美貌与智慧，还有那份不服输的韧劲儿，一点儿都没遗传到我身上。

二选一的机会我都能选错，所以每次四选一的选择题，我都蒙不对。

她很忙，我也不想在她的电话里杀时间。

打听了几句开学前的准备，她就准备要撂电话。

都说了“过两天再聊”，在她马上要挂断的瞬间，我突然喊了起来。

“妈！”

“又什么事儿？”她的口气有种习惯性地不耐烦。如果不是我了解她就是这种急性子，可能早就膝盖一软，跪在地上对着电话磕头了。

然而此刻我只是搂紧了电话，不知道怎么说。

“到底怎么了？”她的语气终于柔和了点儿。

“我爸要结婚了，你知道吗？”
`
  },
  "2": {
    title: "最好的同桌",
    subtitle: "最好的我们 • 第一章",
    date: "2010.09.15",
    content: `
那个午后，阳光斜斜地洒在课桌上。

余淮正低头做着物理题。他的睫毛很长，在眼窝处投下一小片阴影。我偷偷看着他，手里握着的笔半天没动一下。

“耿耿，你看这道力学题，其实有个更简便的做法。”

他突然转过头，撞见了我还没来得及收回的目光。但他只是笑了笑，露出一口白牙，像是个全然不觉的英雄。

在那段长长的、灰扑扑的青春里，他是唯一的亮色。
`
  },
  "3": {
    title: "物理竞赛的秘密",
    subtitle: "最好的我们 • 第二章",
    date: "2010.10.10",
    content: `
“如果你是清风，我一定弄死心相印。”

这大概是他这辈子说过最孩子气的表白，也是我听过最动人的话。

当时我们正走在通往竞赛教室的长廊上，那里的空气总是带着一种紧绷的肃穆。但我却觉得，只要他在旁边，全世界的物理公式似乎都变得温柔了起来。

他总是说，耿耿你这么笨，离了我可怎么办。

可是那时候的我并不知道，原来在这个世界上，最难的题并不是物理，而是——离别。
`
  },
  "4": {
    title: "晚秋的高考",
    subtitle: "最好的我们 • 终章",
    date: "2011.06.07",
    content: `
那年的夏天，结束得比往年都要快一些。

考场外面的树影摇晃，家长们焦灼地等待着。而我站在人群中，却在疯狂地寻找那个熟悉的身影。

“余淮！”

他的背影还是在那片刺目的白光中显得那么倔强。如果我们的一生真的只需要一场考试来定义，那我希望，我的答卷上，写的全是他。

当时的他是最好的他，后来的我是最好的我。

可是最好的我们之间，隔了一整个青春。
`
  }
};

export default function ReadingPage() {
  const { id } = useParams();
  const location = useLocation();
  const state = location.state || {};
  
  // Settings State
  const [fontSize, setFontSize] = useState(1.1); // rem
  const [lineHeight, setLineHeight] = useState(2.2);
  const [showSettings, setShowSettings] = useState(false);
  
  const fromCatalog = state.from === 'catalog';
  const isDerivative = state.isDerivative;
  const DEFAULT_CHAPTER_LIST = [
    { id: "1", title: "第一章 耿耿（No.1）" },
    { id: "2", title: "第二章 耿耿余淮" },
    { id: "3", title: "第三章 另一只脚" },
    { id: "4", title: "第四章 喂，所以我们是..." },
    { id: "5", title: "第五章 最好莫过陌生人" },
    { id: "6", title: "第六章 新生活（No.2）" },
    { id: "7", title: "第七章 我们的生活" },
    { id: "8", title: "第八章 形式主义大好" },
    { id: "9", title: "第九章 摸底（No.3）" },
    { id: "10", title: "第十章 对不起，我不..." },
    { id: "11", title: "第十一章 寂寞的季节" },
    { id: "12", title: "第十二章 别人的生活" },
    { id: "13", title: "第十三章 校庆（上）" },
    { id: "14", title: "第十四章 校庆（中）" },
    { id: "15", title: "第十五章 校庆（下）" },
  ];
  const chapters = state.chapters || (isDerivative ? [] : DEFAULT_CHAPTER_LIST);
  
  // Find current chapter index if chapters list is available
  const currentIndex = chapters.findIndex((c: any) => c.id.toString() === id?.toString());
  const prevChapter = currentIndex > 0 ? chapters[currentIndex - 1] : null;
  const nextChapter = currentIndex >= 0 && currentIndex < chapters.length - 1 ? chapters[currentIndex + 1] : null;

  // Custom metadata from state
  const novelTitle = state.title || "最好的我们";
  const authorName = state.author || "八月长安";
  const chapterTitle = state.chapterTitle || (CHAPTER_DATA[id || "1"]?.title || "第一章：当时的他是最好的他");
  const chapterSubtitle = isDerivative ? `${novelTitle} • 社区衍生` : (CHAPTER_DATA[id || "1"]?.subtitle || "最好的我们 • 序章");
  const chapterContent = state.chapterContent || (CHAPTER_DATA[id || "1"]?.content || CHAPTER_DATA["1"].content);
  const chapterDate = isDerivative ? "2024.03.20" : (CHAPTER_DATA[id || "1"]?.date || "2010.09.01");

  const backPath = fromCatalog ? '/catalog' : '/';
  const backText = fromCatalog ? '返回目录' : '返回主页';

  // Navigation handlers
  const getNavState = (targetChapter: any) => ({
    ...state,
    chapterTitle: targetChapter.title,
    chapterContent: targetChapter.content,
  });

  return (
    <div className="min-h-screen bg-white selection:bg-summer-green-200">
      {/* Background with delicate overlay */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
        <img 
          src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/%E4%B8%8B%E8%BD%BD%20%281%29.jpg" 
          alt="Atmospheric Background"
          className="w-full h-full object-cover transform scale-105 opacity-60 grayscale-[0.1]"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-white/90 via-white/30 to-white/90" />
      </div>

      {/* Elegant Header Navigation */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/10 backdrop-blur-md border-b border-white/20 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <Link to={backPath} state={state} className="flex items-center gap-2 text-summer-green-900 group hover:text-summer-green-600 transition-all">
            <ChevronLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            <span className="font-serif font-medium">{backText}</span>
          </Link>
          
          <div className="hidden md:flex flex-col items-center">
            <span className="text-[10px] tracking-[0.4em] text-summer-green-800/40 uppercase font-bold">{chapterSubtitle}</span>
            <h1 className="text-sm font-serif font-bold text-summer-green-950 uppercase tracking-widest">{chapterTitle}</h1>
          </div>

          <div className="flex items-center gap-4">
            <button 
              onClick={() => setShowSettings(!showSettings)}
              className={`p-2 transition-colors ${showSettings ? 'text-summer-green-600' : 'text-summer-green-900/60 hover:text-summer-green-600'}`}
            >
              <Settings className="w-4 h-4" />
            </button>
            <button className="p-2 text-summer-green-900/60 hover:text-summer-green-600 transition-colors">
              <Share2 className="w-4 h-4" />
            </button>
            <button className="p-2 text-summer-green-900/60 hover:text-pink-500 transition-colors">
              <Heart className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* Settings Panel */}
      <AnimatePresence>
        {showSettings && (
          <>
            {/* Backdrop for closing */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowSettings(false)}
              className="fixed inset-0 z-[55] bg-transparent"
            />
            
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              className="fixed top-20 right-6 z-[60] bg-white/80 backdrop-blur-xl border border-white/40 shadow-2xl rounded-3xl p-6 w-72 origin-top-right"
            >
              <div className="space-y-8">
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-serif font-bold text-summer-green-950 uppercase tracking-widest">字体大小</span>
                    <span className="text-xs text-summer-green-600 font-mono">{(fontSize * 16).toFixed(0)}px</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <button 
                      onClick={() => setFontSize(Math.max(0.8, fontSize - 0.1))}
                      className="p-2 bg-stone-50 rounded-xl text-stone-900 hover:bg-stone-100 transition-colors"
                    >
                      <Minus className="w-3 h-3" />
                    </button>
                    <div className="flex-1 h-1 bg-stone-100 rounded-full relative">
                      <div 
                        className="absolute inset-y-0 left-0 bg-summer-green-600 rounded-full" 
                        style={{ width: `${((fontSize - 0.8) / (2 - 0.8)) * 100}%` }}
                      />
                    </div>
                    <button 
                      onClick={() => setFontSize(Math.min(2, fontSize + 0.1))}
                      className="p-2 bg-stone-50 rounded-xl text-stone-900 hover:bg-stone-100 transition-colors"
                    >
                      <Plus className="w-3 h-3" />
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-serif font-bold text-summer-green-950 uppercase tracking-widest">行间距</span>
                    <span className="text-xs text-summer-green-600 font-mono">{lineHeight.toFixed(1)}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <button 
                      onClick={() => setLineHeight(Math.max(1.0, lineHeight - 0.2))}
                      className="p-2 bg-stone-50 rounded-xl text-stone-900 hover:bg-stone-100 transition-colors"
                    >
                      <Minus className="w-3 h-3" />
                    </button>
                    <div className="flex-1 h-1 bg-stone-100 rounded-full relative">
                      <div 
                        className="absolute inset-y-0 left-0 bg-summer-green-600 rounded-full" 
                        style={{ width: `${((lineHeight - 1.0) / (3.5 - 1.0)) * 100}%` }}
                      />
                    </div>
                    <button 
                      onClick={() => setLineHeight(Math.min(3.5, lineHeight + 0.2))}
                      className="p-2 bg-stone-50 rounded-xl text-stone-900 hover:bg-stone-100 transition-colors"
                    >
                      <Plus className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Reading Progress Indicator */}
      <motion.div 
        className="fixed top-0 left-0 h-1 bg-summer-green-600 z-[60]"
        style={{ width: "30%" }} // Simple static progress for visual effect
      />

      {/* Main Content Area */}
      <main className="relative z-10 pt-32 pb-40 px-6">
        <article className="max-w-3xl mx-auto">
          {/* Chapter Opening Header */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-24"
          >
            <span className="inline-block px-4 py-1 rounded-full bg-summer-green-50 text-summer-green-600 text-[10px] font-bold tracking-[0.2em] mb-6 uppercase">
              {isDerivative ? "Community Entry" : `Chapter ${id || "01"}`}
            </span>
            <h2 className="text-5xl md:text-6xl font-serif font-bold text-summer-green-950 mb-6 tracking-tight">
              {chapterTitle}
            </h2>
            <div className="w-12 h-[2px] bg-summer-green-200 mx-auto mb-8" />
            <p className="text-summer-green-800/60 font-serif italic text-lg">{chapterDate} • 时光印记</p>
          </motion.div>

          {/* Reading Content */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 1 }}
            className="reading-content font-serif text-summer-green-950 px-4 md:px-0"
            style={{ 
              ['--reading-font-size' as any]: `${fontSize}rem`,
              ['--reading-line-height' as any]: lineHeight
            }}
          >
            <div className="markdown-body">
              <ReactMarkdown>{chapterContent}</ReactMarkdown>
            </div>
          </motion.div>

          {/* Elegant Footer / Navigation */}
          <footer className="mt-40 pt-20 border-t border-summer-green-100/50">
            <div className="flex flex-col items-center">
              <div className="flex items-center gap-3 mb-10">
                <MessageCircle className="w-5 h-5 text-summer-green-600" />
                <span className="text-summer-green-800/60 font-serif">记录你的感悟...</span>
              </div>
              
              <div className="flex justify-between w-full items-center">
                 {prevChapter ? (
                   <Link 
                     to={`/read/${prevChapter.id}`} 
                     state={getNavState(prevChapter)}
                     className="text-summer-green-900/60 hover:text-summer-green-600 transition-colors flex items-center gap-2"
                   >
                      <ChevronLeft className="w-4 h-4" />
                      <span className="text-xs font-serif italic">上一章</span>
                   </Link>
                 ) : (
                   <div className="text-summer-green-900/10 flex items-center gap-2 cursor-not-allowed">
                      <ChevronLeft className="w-4 h-4" />
                      <span className="text-xs font-serif italic text-stone-300">已是序章</span>
                   </div>
                 )}
 
                 {nextChapter ? (
                   <Link 
                      to={`/read/${nextChapter.id}`} 
                      state={getNavState(nextChapter)}
                      className="group flex items-center gap-6 px-10 py-4 rounded-full bg-summer-green-950/95 text-white hover:bg-summer-green-900 transition-all shadow-xl hover:shadow-2xl active:scale-95 cursor-pointer"
                    >
                      <span className="font-serif font-bold tracking-widest">下一章</span>
                      <ArrowRight className="w-4 h-4 group-hover:translate-x-2 transition-transform" />
                   </Link>
                 ) : (
                   <div 
                      className="group flex items-center gap-6 px-10 py-4 rounded-full bg-stone-100 text-stone-300 cursor-not-allowed pointer-events-none"
                    >
                      <span className="font-serif font-bold tracking-widest">已读完</span>
                      <ArrowRight className="w-4 h-4" />
                   </div>
                 )}
 
                 <span className="text-summer-green-900/40 text-xs font-serif italic">
                   {currentIndex + 1} / {chapters.length || (isDerivative ? 1 : 15)}
                 </span>
              </div>
            </div>
          </footer>
        </article>
      </main>

      {/* Atmospheric Floating Elements */}
      <div className="fixed bottom-10 right-10 z-[5] opacity-10 pointer-events-none">
        <span className="font-serif text-[20vw] font-bold text-summer-green-900 select-none">
          {id?.toString().padStart(2, '0') || "01"}
        </span>
      </div>
    </div>
  );
}
