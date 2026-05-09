import { motion } from "motion/react";
import { Heart, MessageSquare, Share2, Plus } from "lucide-react";
import { Link } from "react-router-dom";

const WORKS = [
  {
    id: 1,
    title: "晚秋回忆录",
    author: "余小淮",
    image: "https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/_%E3%85%A4%D6%B4%D6%B4%E3%85%A4%E3%85%A4%20_%DB%AB%D6%B4%20%EA%AF%AD%F0%93%88%92%F0%9F%8D%80%20_%E3%85%A4%E3%85%A4%F0%9D%96%BF%F0%9D%97%88%F0%9D%97%85%F0%9D%97%85%F0%9D%97%88%F0%9D%97%90%E3%85%A4%20%F0%9D%96%BF%F0%9D%97%88%F0%9D%97%8B%20%E3%85%A4%F0%9D%85%84%20%E3%85%A4%E3%85%A4%E3%85%A4%E3%85%A4%E3%85%A4%E3%85%A4%F0%9D%97%86%F0%9D%97%88%F0%9D%97%8B%F0%9D%96%BE%E3%85%A4%E3%85%A4%E3%85%A4%E3%85%A4%F0%93%8F%B8%E2%83%98%20%E3%85%A4%E3%85%A4%E3%85%A4%E3%85%A4.jpg",
    likes: 1240,
  },
  {
    id: 2,
    title: "振华中学二三事",
    author: "耿耿星河",
    image: "https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/%E4%B8%8B%E8%BD%BD%20%282%29.jpg",
    likes: 856,
  },
  {
    id: 3,
    title: "如果我是清风",
    author: "余小淮",
    image: "https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/%E4%B8%8B%E8%BD%BD%20%281%29.jpg",
    likes: 2103,
  }
];

export default function FanWorks() {
  return (
    <section id="derivative" className="relative py-16 overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <img 
          src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/%E4%B8%8B%E8%BD%BD%20%283%29.jpg" 
          alt="Memory Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-white/80" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-16">
          <div>
            <motion.span 
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              className="text-summer-green-600 font-medium tracking-[0.3em] uppercase text-sm"
            >
              Creative Space
            </motion.span>
            <motion.h2 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              className="text-4xl md:text-5xl font-serif font-bold mt-4"
            >
              二创天地 • 我们的故事
            </motion.h2>
          </div>
          <div className="flex items-center gap-6">
            <p className="font-cursive text-3xl text-summer-green-800/60 hidden lg:block">
              "小爷我一直都在"
            </p>
            <Link to="/derivative/create" className="flex items-center gap-2 bg-summer-green-800 text-white px-8 py-3 rounded-full hover:bg-summer-green-700 transition-all shadow-xl shadow-summer-green-800/20 active:scale-95">
              <Plus className="w-5 h-5" />
              <span>发布创作</span>
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {WORKS.map((work, index) => (
            <motion.div
              key={work.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="group bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-2xl hover:shadow-summer-green-800/10 transition-all duration-500 flex flex-col"
            >
              <div className="relative aspect-square overflow-hidden">
                <img 
                  src={work.image} 
                  alt={work.title}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-black/10 group-hover:bg-black/0 transition-colors" />
                <div className="absolute top-4 left-4">
                  <span className="glass-card px-3 py-1 rounded-full text-[10px] font-bold text-summer-green-900 tracking-wider">
                    NEW WORK
                  </span>
                </div>
              </div>
              
              <div className="p-6 flex flex-col flex-grow">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-6 h-6 bg-summer-green-200 rounded-full" />
                  <span className="text-xs text-summer-green-800/60 font-medium">{work.author}</span>
                </div>
                <h3 className="text-xl font-serif font-bold mb-4 group-hover:text-summer-green-600 transition-colors">
                  {work.title}
                </h3>
                
                <div className="mt-auto flex items-center justify-between border-t border-summer-green-50 pt-4">
                  <div className="flex items-center gap-6">
                    <button className="flex items-center gap-1.5 text-summer-green-800/40 hover:text-red-500 transition-colors">
                      <Heart className="w-4 h-4" />
                      <span className="text-xs font-medium">{work.likes}</span>
                    </button>
                    <button className="flex items-center gap-1.5 text-summer-green-800/40 hover:text-blue-500 transition-colors">
                      <MessageSquare className="w-4 h-4" />
                      <span className="text-xs font-medium">82</span>
                    </button>
                  </div>
                  <button className="p-2 text-summer-green-800/40 hover:bg-summer-green-50 rounded-full transition-colors">
                    <Share2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
