import { motion, AnimatePresence } from "motion/react";
import { ChevronLeft, Plus, Heart, MessageCircle, PenTool, Loader2, BookOpen, Clock, Check, Globe } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";

const FAN_FICTION = [
  {
    id: 1,
    title: "晚秋回忆录",
    author: "余小淮",
    excerpt: "高三那一年的秋天，窗外的落叶铺满了操场。余淮坐在我旁边，笔尖划过纸面的声音在安静的课间显得格外清晰...",
    likes: 1240,
    comments: 82,
    date: "2024.03.20",
    tags: ["治愈", "耿耿余淮"],
    chapters: [
      { id: "f1-1", title: "第一章：旧操场的落叶", content: "那是我们最后一次在操场漫步，风卷起地上的枯叶，也带走了我们的青春。余淮看着远方，沉默了太久太久。" },
      { id: "f1-2", title: "第二章：没送出的信", content: "抽屉里的信封已经泛黄。我始终不明白，为什么最好的我们，注定要错过。是不是遗憾，才是青春的底色？" }
    ]
  },
  {
    id: 3,
    title: "如果我是清风",
    author: "余小淮",
    excerpt: "如果我是清风，我一定弄死心相印。这句玩笑话后来成了我们之间最隐秘的默契。多年后的重逢，谁也没提当年的豪言壮语...",
    likes: 2103,
    comments: 156,
    date: "2024.02.15",
    tags: ["经典", "虐心"],
    chapters: [
      { id: "f3-1", title: "序章：清风依旧", content: "如果我是清风，我会选择吹向你的窗台。哪怕只是停留片刻，也胜过这漫长的思念。" }
    ]
  },
  {
    id: 5,
    title: "耿耿星河的温柔",
    author: "路星河的信",
    excerpt: "如果你是耿耿，那我永远是那个在墙上画满星河的路星河。我并不后悔那些疯狂的举动，因为那就是我的青春...",
    likes: 1850,
    comments: 120,
    date: "2024.04.10",
    tags: ["路星河", "守护"],
    chapters: [
      { id: "f5-1", title: "重临：我的星河", content: "五十多次的求婚，终究是一场梦。但我宁愿沉浸在梦里，在那片为你而画的星河里。" }
    ]
  }
];

export default function FanWorksPage() {
  const location = useLocation();
  const [activeTab, setActiveTab] = useState<'community' | 'mine'>(() => {
    return location.state?.activeTab || 'community';
  });

  const [myWorks, setMyWorks] = useState<any[]>([]);
  const [showPublishToast, setShowPublishToast] = useState(false);
  const [showPublishText, setShowPublishText] = useState("");

  const handlePublish = (workId: number) => {
    const nextWorks = myWorks.map((work) => {
      if (work.id === workId) {
        return { ...work, published: true };
      }
      return work;
    });
    setMyWorks(nextWorks);
    localStorage.setItem("my_derivative_works", JSON.stringify(nextWorks));
    
    const publishedWork = nextWorks.find(w => w.id === workId);
    if (publishedWork) {
      setShowPublishText(`《${publishedWork.title}》已成功发布至文库广场！`);
    } else {
      setShowPublishText("创作已成功发布至文库广场！");
    }
    setShowPublishToast(true);
    setTimeout(() => {
      setShowPublishToast(false);
    }, 3000);
  };

  // Load custom works from localStorage on mount & when tab changes
  useEffect(() => {
    const loaded = JSON.parse(localStorage.getItem("my_derivative_works") || "[]");
    setMyWorks(loaded);
  }, [activeTab]);

  // Real-time ticking simulation for Rendering stories!
  useEffect(() => {
    if (activeTab !== 'mine') return;

    const hasRendering = myWorks.some((w) => w.status === 'rendering');
    if (!hasRendering) return;

    const timer = setInterval(() => {
      let updated = false;
      const nextWorks = myWorks.map((work) => {
        if (work.status === 'rendering') {
          updated = true;
          // Progress speed: 10% to 25% per tick for rapid responsive feedback
          const nextProgress = (work.progress || 0) + Math.floor(Math.random() * 15) + 12;
          
          if (nextProgress >= 100) {
            return {
              ...work,
              progress: 100,
              status: 'completed',
              chapters: [
                {
                  id: `${work.id}-ch1`,
                  title: "重置·那场迟到的狂奔",
                  content: `### 🌌 时光传送门已成功连接平行宇宙\n\n夏夜的风，吹散了高考最后一科的严肃与沉重。\n\n在原本的那个世界里，余淮突兀地缺席了聚会，像一颗划过夜空后陨落的彗星，在耿耿的生命里留下了一段长达十年的空白。\n\n然而，这并不是故事的唯一终局。因为此刻，属于我们的平行时空悄然开启。\n\n在人群散去的校园门口，夜樱摇曳。\n那个熟悉的身影并没有转身步入阴影，他在路灯橘黄的光晕下停住了脚步。\n他突然转过头，眼睛里带着从未有过的坚毅。\n\n“耿耿！”\n\n在风中，他大声喊着我的名字。然后，他没有逃避，而是大步向我跑来。\n他伸出手，一把抓住了我温热的手心。指尖传来的温度如此真实、滚烫，仿佛要将十年的遗憾在一瞬间融化。\n\n他说：“耿耿，这次，我不走了。我们一起去北京，好不好？”\n\n---\n\n### 📝 你的脑洞与创意融合点：\n\n> **创意：** ${work.prompt}\n\n---\n\n这一幕，在无数个平行宇宙里温柔定格。\n那块被风吹响的老黑板，那套写满了两人名字的模拟试卷，都在这一刻，拥有了最温存的圆满交代。`
                },
                {
                  id: `${work.id}-ch2`,
                  title: "落笔·更好的我们",
                  content: `### 🍁 更好的我们在未来重聚\n\n在北京秋天温存的阳光下，落叶金黄铺地。\n\n余淮重新拿出那本铺满数字的物理笔记本递给我，有些笨拙地笑起来：“耿耿，你还是这么笨。但我会永远给你解世界上最难的题。”\n\n我看着他，眼底铺满了晶莹而温热的泪水。岁月的沙漏在落笔一刻定格，我们的爱在浩瀚星河里留下了永恒的痕迹。\n\n---\n\n#### ✍️ 创意制作者寄语：\n\n本作品是时光机AI协助扩写版本。由你投递的灵感火花被永远镌刻在此。每一个温柔的遗憾，都终有回音。`
                }
              ]
            };
          } else {
            return { ...work, progress: nextProgress };
          }
        }
        return work;
      });

      if (updated) {
        setMyWorks(nextWorks);
        localStorage.setItem("my_derivative_works", JSON.stringify(nextWorks));
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [myWorks, activeTab]);

  return (
    <div className="min-h-screen selection:bg-summer-green-200 relative">
      {/* Fixed Background Image */}
      <div className="fixed inset-0 z-0">
        <img 
          src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/%E8%83%8C%E6%99%AF%E5%9B%BE/%E4%B8%8B%E8%BD%BD%20%283%29.jpg" 
          alt="Background"
          className="w-full h-full object-cover"
        />
      </div>

      <header className="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-md border-b border-stone-100 px-8 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Link to="/" className="text-stone-500 hover:text-summer-green-800 transition-colors flex items-center gap-2 group">
            <ChevronLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            <span className="text-sm font-medium">返回主页</span>
          </Link>
          
          <h1 className="text-xl font-serif font-bold text-summer-green-950 tracking-[0.2em]">二创社区 DERIVATIVE</h1>

          <Link to="/derivative/create" className="flex items-center gap-2 bg-summer-green-800 text-white px-5 py-2 rounded-full text-sm font-bold shadow-lg shadow-summer-green-800/20 hover:bg-summer-green-700 transition-all active:scale-95">
            <Plus className="w-4 h-4" />
            <span>写新创意</span>
          </Link>
        </div>
      </header>

      <main className="relative z-10 pt-32 pb-24 px-6 text-stone-900">
        <div className="max-w-6xl mx-auto">
          {/* Tab Selection */}
          <div className="flex justify-center mb-16 px-4">
            <div className="bg-stone-100/50 p-1.5 rounded-full flex items-center gap-2 border border-stone-200/50">
              <button 
                onClick={() => setActiveTab('community')}
                className={`px-10 py-3 rounded-full text-xs font-bold tracking-[0.2em] transition-all ${
                  activeTab === 'community' 
                  ? 'bg-summer-green-800 text-white shadow-xl shadow-summer-green-800/20' 
                  : 'text-stone-500 hover:text-stone-700'
                }`}
              >
                文库广场
              </button>
              <button 
                onClick={() => setActiveTab('mine')}
                className={`px-10 py-3 rounded-full text-xs font-bold tracking-[0.2em] transition-all ${
                  activeTab === 'mine' 
                  ? 'bg-summer-green-800 text-white shadow-xl shadow-summer-green-800/20' 
                  : 'text-stone-500 hover:text-stone-700'
                }`}
              >
                我的创作
              </button>
            </div>
          </div>

          <AnimatePresence mode="wait">
            {activeTab === 'community' ? (
              <motion.div
                key="community"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="grid grid-cols-1 lg:grid-cols-2 gap-12"
              >
                {/* 1. Left Feature: Quick Write Entry */}
                <div className="space-y-8">
                  <div className="bg-white border border-stone-100 rounded-[40px] p-12 shadow-sm hover:shadow-xl transition-all">
                    <div className="mb-8">
                      <div className="w-12 h-12 bg-summer-green-100 rounded-2xl flex items-center justify-center mb-4">
                         <PenTool className="w-6 h-6 text-summer-green-800" />
                      </div>
                      <h2 className="text-3xl font-serif font-bold text-stone-900">撰写时光</h2>
                      <p className="text-stone-600 text-sm italic mt-2">在这里，你可以为那个没能圆满的夏天写下一个结局。</p>
                    </div>
                    <Link to="/derivative/create" className="inline-flex items-center gap-4 bg-summer-green-950 text-white px-8 py-4 rounded-full font-serif font-bold tracking-widest hover:bg-summer-green-900 transition-all shadow-xl shadow-summer-green-900/20 group">
                      <span>开始书写</span>
                      <Plus className="w-4 h-4 group-hover:rotate-90 transition-transform" />
                    </Link>
                  </div>
                  
                  {/* Decorative Quote */}
                  <div className="p-12 text-center opacity-40">
                    <p className="font-serif text-xl italic text-stone-500 leading-relaxed">
                      "当时的他是最好的他，后来的我是最好的我。可是最好的我们之间，隔了一整个青春。"
                    </p>
                  </div>
                </div>

                {/* 2. List of Stories (Community) */}
                <div className="space-y-8">
                  <div className="flex items-center gap-4 mb-6">
                    <span className="text-[10px] font-bold text-stone-300 tracking-[0.4em] uppercase">Community Plaza</span>
                    <div className="h-[1px] flex-1 bg-stone-100"></div>
                  </div>
                  
                  {[
                    ...myWorks.filter((w) => w.status === 'completed' && w.published).map(w => ({
                      id: w.id,
                      title: w.title,
                      author: "我 (AI 协创)",
                      excerpt: w.excerpt,
                      likes: w.likes || 18,
                      comments: w.comments || 2,
                      date: w.date,
                      tags: w.tags || ["平行宇宙", "独家创意"],
                      chapters: w.chapters
                    })),
                    ...FAN_FICTION
                  ].map((work, index) => (
                    <motion.div
                      key={work.id}
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-white p-10 rounded-[40px] shadow-sm hover:shadow-2xl hover:shadow-stone-200/40 transition-all border border-stone-50 group cursor-pointer"
                    >
                      <Link 
                        to="/catalog" 
                        state={{ 
                          title: work.title, 
                          author: work.author, 
                          chapters: work.chapters, 
                          isDerivative: true 
                        }}
                      >
                        <div className="flex justify-between items-start mb-6">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-summer-green-100 flex items-center justify-center overflow-hidden">
                              <span className="text-[10px] font-bold text-summer-green-800 italic">WR</span>
                            </div>
                            <span className="text-xs font-bold text-stone-700">{work.author}</span>
                          </div>
                          <span className="text-[10px] text-stone-300 font-mono tracking-widest">{work.date}</span>
                        </div>
                        
                        <h3 className="text-2xl font-serif font-bold text-stone-900 mb-4 group-hover:text-summer-green-700 transition-colors leading-tight">
                          {work.title}
                        </h3>
                        
                        <p className="text-stone-500 text-base line-clamp-3 leading-relaxed mb-8 font-serif italic border-l-2 border-stone-50 pl-6">
                          "{work.excerpt}"
                        </p>

                        <div className="flex items-center justify-between">
                          <div className="flex gap-2">
                            {work.tags.map(tag => (
                              <span key={tag} className="text-[10px] bg-stone-50 text-stone-400 px-3 py-1 rounded-full uppercase tracking-widest">#{tag}</span>
                            ))}
                          </div>
                          <div className="flex items-center gap-6 text-stone-300">
                            <div className="flex items-center gap-1.5 hover:text-red-400 transition-colors">
                              <Heart className="w-4 h-4" />
                              <span className="text-xs font-bold">{work.likes}</span>
                            </div>
                            <div className="flex items-center gap-1.5 hover:text-blue-400 transition-colors">
                              <MessageCircle className="w-4 h-4" />
                              <span className="text-xs font-bold">{work.comments}</span>
                            </div>
                          </div>
                        </div>
                      </Link>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="mine"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="max-w-4xl mx-auto"
              >
                {myWorks.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-20 text-center">
                    <div className="w-32 h-32 bg-stone-50/80 border border-stone-200/50 rounded-[40px] flex items-center justify-center mb-8 shadow-inner">
                      <PenTool className="w-10 h-10 text-stone-300" />
                    </div>
                    <h3 className="text-2xl font-serif font-bold text-stone-900 mb-4">暂无创作作品</h3>
                    <p className="text-stone-500 text-sm max-w-[340px] mb-12 italic leading-relaxed">
                      你的感悟与奇想是时光隧道的燃料。快写下第一篇创意，意念编织机将为它重现平行世界。
                    </p>
                    <Link to="/derivative/create" className="px-10 py-4 bg-summer-green-800 text-white rounded-full font-serif font-bold tracking-widest shadow-2xl shadow-summer-green-800/20 hover:scale-105 transition-transform">
                      写下第一个同人创意
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-10">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-stone-200/50">
                      <div>
                        <h3 className="text-2xl font-serif font-bold text-stone-900">我的时光档案</h3>
                        <p className="text-xs text-stone-500 italic mt-1 font-serif">
                          这里存放着那些由时光机AI协创、为你重新续写的耿耿余淮回忆
                        </p>
                      </div>
                      <Link to="/derivative/create" className="inline-flex items-center gap-2 bg-summer-green-800 text-white px-5 py-2.5 rounded-full text-xs font-bold shadow-lg shadow-summer-green-800/10 hover:bg-summer-green-700 transition-all self-start">
                        <Plus className="w-4 h-4" />
                        <span>写新创意</span>
                      </Link>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                      {myWorks.map((work) => {
                        const isRendering = work.status === 'rendering';
                        // Determine step text based on progress
                        let stepText = "🌌 正在连接时空折叠轨道...";
                        if (work.progress >= 25 && work.progress < 50) {
                          stepText = "📝 正在读取并拓展创意脑洞...";
                        } else if (work.progress >= 50 && work.progress < 80) {
                          stepText = "✨ 正在由时光笔尖润饰词藻细节...";
                        } else if (work.progress >= 80) {
                          stepText = "🎨 正在进行最后的宇宙印制胶装...";
                        }

                        return (
                          <motion.div
                            key={work.id}
                            layout
                            initial={{ opacity: 0, y: 15 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="bg-white/90 backdrop-blur-md border border-stone-100 rounded-[36px] p-8 md:p-10 shadow-sm hover:shadow-xl transition-all flex flex-col justify-between group"
                          >
                            <div className="space-y-5">
                              <div className="flex justify-between items-center text-[10px] text-stone-400 font-mono tracking-widest">
                                <span className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-[9px] font-bold uppercase transition-all tracking-wider ${
                                  isRendering ? 'bg-amber-50 text-amber-600 border border-amber-100' : 'bg-summer-green-50 text-summer-green-800 border border-summer-green-100'
                                }`}>
                                  {isRendering ? (
                                    <>
                                      <Loader2 className="w-2.5 h-2.5 text-amber-600 animate-spin" />
                                      <span>微缩宇宙生成中</span>
                                    </>
                                  ) : (
                                    <>
                                      <BookOpen className="w-2.5 h-2.5 text-summer-green-800" />
                                      <span>完稿已封印</span>
                                    </>
                                  )}
                                </span>
                                <span>{work.date}</span>
                              </div>

                              <div>
                                <h4 className="text-2xl font-serif font-bold text-stone-900 leading-tight">
                                  {work.title}
                                </h4>
                                <p className="text-[10px] text-stone-400 font-serif tracking-widest uppercase mt-1">
                                  灵感原设：你本人 • 制作：时光机协助
                                </p>
                              </div>

                              <p className="text-stone-500 text-sm line-clamp-3 leading-relaxed font-serif italic border-l border-stone-200 pl-4 py-0.5">
                                "{work.excerpt}"
                              </p>
                            </div>

                            <div className="mt-8 pt-6 border-t border-stone-100">
                              {isRendering ? (
                                <div className="space-y-3">
                                  <div className="flex justify-between items-center text-xs">
                                    <span className="text-stone-700 font-serif font-semibold animate-pulse">
                                      {stepText}
                                    </span>
                                    <span className="font-mono font-bold text-summer-green-950">
                                      {work.progress}%
                                    </span>
                                  </div>
                                  <div className="w-full bg-stone-100 h-2 rounded-full overflow-hidden">
                                    <motion.div 
                                      className="bg-summer-green-800 h-full rounded-full"
                                      animate={{ width: `${work.progress}%` }}
                                      transition={{ duration: 0.8 }}
                                    />
                                  </div>
                                </div>
                              ) : (
                                <div className="space-y-4">
                                  <div className="flex items-center justify-between text-stone-400 text-xs">
                                    <span className="flex items-center gap-1.5 font-serif">
                                      <Clock className="w-3.5 h-3.5 text-stone-300" />
                                      全篇 2 章 • 解锁完成
                                    </span>
                                    {work.published ? (
                                      <span className="flex items-center gap-1 text-summer-green-800 font-bold text-[10px] bg-summer-green-50 px-2.5 py-0.5 rounded-full border border-summer-green-100">
                                        <Globe className="w-3.5 h-3.5 text-summer-green-700 animate-pulse" />
                                        已公开至文库广场
                                      </span>
                                    ) : (
                                      <span className="text-stone-400 text-[10px] bg-stone-50 px-2 py-0.5 rounded-full border border-stone-200">
                                        待发布
                                      </span>
                                    )}
                                  </div>
                                  
                                  <div className="flex items-center justify-end gap-3 pt-2 border-t border-stone-50">
                                    {!work.published && (
                                      <button
                                        onClick={(e) => {
                                          e.preventDefault();
                                          handlePublish(work.id);
                                        }}
                                        className="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-full font-serif font-bold text-xs transition-all shadow-md hover:shadow-lg active:scale-95 flex items-center gap-1 cursor-pointer"
                                      >
                                        <Globe className="w-3.5 h-3.5" />
                                        <span>发布创作</span>
                                      </button>
                                    )}
                                    <Link
                                      to="/catalog"
                                      state={{
                                        title: work.title,
                                        author: "时光机协助 & " + "你",
                                        chapters: work.chapters,
                                        isDerivative: true
                                      }}
                                      className="px-5 py-2 bg-summer-green-950 text-white rounded-full font-serif font-bold text-xs hover:bg-summer-green-900 transition-all shadow-lg hover:shadow-xl active:scale-[0.97]"
                                    >
                                      立即阅读 →
                                    </Link>
                                  </div>
                                </div>
                              )}
                            </div>
                          </motion.div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* Elegant Publish Success Toast Overlay */}
      <AnimatePresence>
        {showPublishToast && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            className="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 bg-stone-900/95 backdrop-blur-md text-white border border-white/10 px-6 py-4 rounded-2xl flex items-center gap-3 shadow-2xl max-w-sm sm:max-w-md"
          >
            <div className="w-8 h-8 rounded-full bg-summer-green-800 flex items-center justify-center shrink-0">
              <Check className="w-4 h-4 text-white" />
            </div>
            <div className="text-left">
              <h5 className="text-xs font-serif font-bold tracking-widest text-stone-200">发布成功！</h5>
              <p className="text-[11px] text-stone-400 mt-0.5 leading-snug">{showPublishText}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
