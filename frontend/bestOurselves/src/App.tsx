import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import Hero from "./components/Hero";
import StoryReader from "./components/StoryReader";
import FanWorks from "./components/FanWorks";
import ReadingPage from "./pages/ReadingPage";
import CatalogPage from "./pages/CatalogPage";
import FanWorksPage from "./pages/FanWorksPage";
import CreateWorkPage from "./pages/CreateWorkPage";
import ScrollToTop from "./components/ScrollToTop";
import { motion } from "motion/react";
import { Trees as Tree, Heart } from "lucide-react";

function LandingPage() {
  return (
    <div className="min-h-screen selection:bg-summer-green-200">
      <Navigation />
      
      <main>
        <Hero />
        
        {/* Quote Buffer with Background */}
        <section className="relative py-24 flex justify-center items-center overflow-hidden">
          <div className="absolute inset-0 z-0">
            <img 
              src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/%E4%B8%8B%E8%BD%BD%20%282%29.jpg" 
              alt="Classroom Memory"
              className="w-full h-full object-cover"
            />
          </div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="relative z-10 text-center px-12 max-w-4xl"
          >
            <p className="font-cursive text-2xl md:text-3xl lg:text-5xl text-white leading-relaxed drop-shadow-[0_4px_25px_rgba(0,0,0,0.9)] text-outline">
              当时的他是最好的他，<br/>
              后来的我是最好的我。<br/>
              可是最好的我们之间，<br/>
              隔了一整个青春。
            </p>
          </motion.div>
        </section>

        <StoryReader />
        
        <FanWorks />

        {/* Closing Quote */}
        <section className="relative py-24 flex flex-col items-center justify-center overflow-hidden">
          {/* Background Image */}
          <div className="absolute inset-0 z-0">
            <img 
              src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/1.jpg" 
              alt="Closing Memory"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-white/80" />
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="relative z-10 text-center px-6"
          >
            <div className="flex justify-center gap-1 mb-8">
              {[1, 2, 3].map(i => (
                <Tree key={i} className="w-5 h-5 text-summer-green-600/30" />
              ))}
            </div>
            <h3 className="font-serif text-3xl md:text-4xl text-summer-green-900 font-bold mb-6 italic">
              — "如果我是清风，我一定弄死心相印"
            </h3>
            <p className="text-summer-green-700/60 font-light tracking-[0.2em]">那些孩子气的瞬间，才是最好的我们。</p>
          </motion.div>
        </section>
      </main>

      {/* Simple Footer */}
      <footer className="py-12 border-t border-summer-green-100/50 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="font-serif font-bold text-lg text-summer-green-900">最好的我们</span>
            <span className="text-xs text-summer-green-800/40 font-medium">© 2026 Memory Studio</span>
          </div>
          
          <div className="flex items-center gap-6 text-sm text-summer-green-800/60 font-medium">
            <a href="#" className="hover:text-summer-green-600 transition-colors">关于</a>
            <a href="#" className="hover:text-summer-green-600 transition-colors">版权申明</a>
            <a href="#" className="hover:text-summer-green-600 transition-colors">联系我们</a>
          </div>
          
          <div className="flex items-center gap-1 text-[10px] text-summer-green-800/20 uppercase tracking-widest font-bold">
            Made with <Heart className="w-3 h-3 text-red-400" /> for Geng Geng & Yu Huai
          </div>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/read/:id" element={<ReadingPage />} />
        <Route path="/catalog" element={<CatalogPage />} />
        <Route path="/derivative" element={<FanWorksPage />} />
        <Route path="/derivative/create" element={<CreateWorkPage />} />
      </Routes>
    </BrowserRouter>
  );
}
