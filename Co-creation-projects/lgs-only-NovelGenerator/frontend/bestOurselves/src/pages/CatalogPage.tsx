import { motion } from "motion/react";
import { ChevronLeft } from "lucide-react";
import { Link, useLocation } from "react-router-dom";

const DEFAULT_CHAPTERS = [
  { id: 1, title: "第一章 耿耿（No.1）" },
  { id: 2, title: "第二章 耿耿余淮" },
  { id: 3, title: "第三章 另一只脚" },
  { id: 4, title: "第四章 喂，所以我们是..." },
  { id: 5, title: "第五章 最好莫过陌生人" },
  { id: 6, title: "第六章 新生活（No.2）" },
  { id: 7, title: "第七章 我们的生活" },
  { id: 8, title: "第八章 形式主义大好" },
  { id: 9, title: "第九章 摸底（No.3）" },
  { id: 10, title: "第十章 对不起，我不..." },
  { id: 11, title: "第十一章 寂寞的季节" },
  { id: 12, title: "第十二章 别人的生活" },
  { id: 13, title: "第十三章 校庆（上）" },
  { id: 14, title: "第十四章 校庆（中）" },
  { id: 15, title: "第十五章 校庆（下）" },
];

export default function CatalogPage() {
  const location = useLocation();
  const state = location.state || {};
  
  const isDerivative = state.isDerivative;
  const title = state.title || "最好的我们";
  const author = state.author || "八月长安";
  const chapters = state.chapters || DEFAULT_CHAPTERS;
  const backPath = isDerivative ? "/derivative" : "/";

  return (
    <div className="min-h-screen selection:bg-summer-green-200 font-serif text-stone-900 relative">
      {/* Fixed Background Image */}
      <div className="fixed inset-0 z-0">
        <img 
          src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/%E4%B8%8B%E8%BD%BD%20%282%29.jpg" 
          alt="Background"
          className="w-full h-full object-cover"
        />
        {/* Overall subtle darkening to ensure header visibility if needed, or just the main overlay */}
        <div className="absolute inset-0 bg-white/30 backdrop-blur-[2px]" />
      </div>

      <header className="fixed top-0 left-0 right-0 z-50 bg-white/60 backdrop-blur-md px-8 py-6 flex items-center justify-between border-b border-white/20">
        <Link to={backPath} className="text-stone-600 hover:text-stone-900 transition-colors flex items-center gap-2 group">
          <ChevronLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
          <span className="text-sm font-medium tracking-widest uppercase">返回{isDerivative ? '广场' : '主页'}</span>
        </Link>
        <h1 className="text-sm font-bold text-stone-500 tracking-[0.4em] uppercase">Table of Contents</h1>
        <div className="w-10 text-right">
           <span className="text-[10px] text-stone-400">01</span>
        </div>
      </header>

      <main className="relative z-10 max-w-2xl mx-auto mt-40 mb-32 px-10 py-16 bg-white/30 backdrop-blur-xl rounded-[40px] shadow-2xl border border-white/40">
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-24 text-center"
        >
          <h2 className="text-4xl font-bold text-black tracking-tight mb-2">{title}</h2>
          <p className="text-sm text-stone-500 mb-6 font-sans tracking-wide">作者：{author}</p>
          <div className="flex items-center justify-center gap-4">
            <div className="w-8 h-[1px] bg-stone-300" />
            <span className="text-xs text-stone-500 uppercase tracking-[0.3em]">
              {isDerivative ? "Community Work" : "With You"}
            </span>
            <div className="w-8 h-[1px] bg-stone-300" />
          </div>
        </motion.div>

        <div className="space-y-1">
          {chapters.map((chapter: any, index: number) => (
            <motion.div
              key={chapter.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.03 }}
            >
              <Link 
                to={`/read/${chapter.id}`}
                state={{ 
                  from: 'catalog', 
                  isDerivative: isDerivative,
                  title: title,
                  author: author,
                  chapterTitle: chapter.title,
                  chapterContent: chapter.content,
                  chapters: chapters
                }}
                className="group block"
              >
                <div className="flex items-baseline gap-4 py-4 border-b border-stone-100 group-hover:border-stone-900/10 transition-colors">
                  <span className="text-lg text-stone-700 group-hover:text-black transition-colors flex-1">
                    {chapter.title}
                  </span>
                  <div className="hidden group-hover:block transition-all italic text-xs text-summer-green-600 font-medium">
                    Read →
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>

        <footer className="mt-40 text-center space-y-4">
          <div className="w-12 h-[1px] bg-stone-200 mx-auto" />
          <p className="text-[9px] tracking-[0.8em] font-sans text-stone-300 uppercase">Memory Keeps All The Best Ourselves</p>
        </footer>
      </main>

      {/* Side Numbers Decor */}
      <div className="fixed top-1/2 -right-4 -translate-y-1/2 vertical-text select-none opacity-10 pointer-events-none">
        <span className="text-[120px] font-bold tracking-tighter text-stone-400">2010</span>
      </div>
    </div>
  );
}
