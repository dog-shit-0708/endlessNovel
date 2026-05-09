import { useState } from "react";
import { motion } from "motion/react";
import { BookOpen, ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";

const CHAPTERS = [
  { id: 1, title: "耿耿于怀", excerpt: "我叫耿耿，我爸爸叫耿耿。他说，这个名字好记...", date: "2010.09.01" },
  { id: 2, title: "最好的同桌", excerpt: "那个午后，阳光斜斜地洒在课桌上，余淮正低头做着物理题...", date: "2010.09.15" },
  { id: 3, title: "物理竞赛的秘密", excerpt: "如果你是清风，我一定弄死心相印——这大概是他最孩子气的表白。", date: "2010.10.10" },
  { id: 4, title: "晚秋的高考", excerpt: "如果我是清风，我一定弄死心相印...", date: "2011.06.07" },
];

export default function StoryReader() {
  const visibleChapters = CHAPTERS.slice(0, 3);

  return (
    <section id="reading" className="relative py-20 px-6 overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <img 
          src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/%E4%B8%8B%E8%BD%BD%20%283%29.jpg" 
          alt="School Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-white/80" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto">
        <div className="mb-12">
          <motion.span 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            className="text-summer-green-800 font-bold tracking-[0.3em] uppercase text-sm"
          >
            Memory Lane
          </motion.span>
          <motion.h2 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            className="text-4xl md:text-5xl font-serif font-bold mt-4 mb-2 text-summer-green-950"
          >
            原文阅读 • 时光回溯
          </motion.h2>
          <p className="text-summer-green-900/70 font-serif italic text-xl">
            "我们不是说好一起做同桌的吗?"
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-stretch">
          <div className="space-y-6">
            {visibleChapters.map((chapter) => (
              <Link to={`/read/${chapter.id}`} key={chapter.id} state={{ from: 'home' }}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  whileHover={{ x: 10 }}
                  className="group cursor-pointer p-6 rounded-2xl bg-white/60 backdrop-blur-md border border-white/40 shadow-xl transition-all hover:bg-white/80 mb-6"
                >
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-xs font-mono text-summer-green-700 font-bold">Chapter {chapter.id}</span>
                    <span className="text-xs text-summer-green-900/60 font-medium">{chapter.date}</span>
                  </div>
                  <h3 className="text-2xl font-serif font-bold mb-3 group-hover:text-summer-green-800 transition-colors text-summer-green-950">
                    {chapter.title}
                  </h3>
                  <p className="text-summer-green-900/90 text-sm line-clamp-2 leading-relaxed mb-4">
                    {chapter.excerpt}
                  </p>

                </motion.div>
              </Link>
            ))}

            <div className="flex justify-center pt-4">
              <Link
                to="/catalog"
                className="flex items-center gap-2 text-summer-green-800 hover:text-summer-green-600 font-bold text-xs uppercase tracking-[0.2em] transition-all group"
              >
                <span>查看全部章节</span>
                <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>

          <div className="flex flex-col">
            <Link to="/read/1" state={{ from: 'home' }} className="block flex-1">
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                className="h-full rounded-3xl overflow-hidden shadow-2xl relative group cursor-pointer"
              >
                <img 
                  src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20260417151254_467_21.jpg" 
                  alt="Memory"
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-summer-green-900/40 to-transparent" />
                <div className="absolute bottom-8 left-8 right-8 text-white">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-[1px] bg-white/50" />
                    <span className="text-sm font-light tracking-widest uppercase">Featured Chapter</span>
                  </div>
                  <h4 className="text-3xl font-serif font-bold italic mb-2">耿耿 & 余淮</h4>
                  <p className="text-white/80 text-sm italic font-light">"当时的他是最好的他，后来的我是最好的我。"</p>
                </div>
              </motion.div>
            </Link>
          </div>
      </div>
    </div>
    </section>
  );
}
