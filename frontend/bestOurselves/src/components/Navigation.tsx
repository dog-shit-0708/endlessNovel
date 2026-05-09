import { motion } from "motion/react";
import { BookOpen, Palette, Quote, Search, User } from "lucide-react";
import { Link } from "react-router-dom";
import { useState } from "react";
import AuthModal from "./AuthModal";

export default function Navigation() {
  const [isAuthOpen, setIsAuthOpen] = useState(false);

  return (
    <>
      <motion.nav 
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="fixed top-0 left-0 right-0 z-50 px-6 py-4 flex justify-between items-center bg-white/60 backdrop-blur-2xl border-b border-summer-green-100 shadow-sm"
      >
        <Link to="/" className="flex items-center gap-2 group transition-all">
          <div className="w-10 h-10 bg-summer-green-700 rounded-xl flex items-center justify-center shadow-lg shadow-summer-green-700/20 group-hover:bg-summer-green-800 transition-colors">
            <Quote className="text-white w-5 h-5" />
          </div>
          <span className="font-serif font-bold text-2xl tracking-wider text-summer-green-900">最好的我们</span>
        </Link>
        
        <div className="hidden md:flex items-center gap-8 text-sm font-semibold text-summer-green-800">
          <Link to="/catalog" className="hover:text-summer-green-600 transition-colors flex items-center gap-2">
            <BookOpen className="w-4 h-4" />
            <span>原文阅读</span>
          </Link>
          <Link to="/derivative" className="hover:text-summer-green-600 transition-colors flex items-center gap-2">
            <Palette className="w-4 h-4" />
            <span>二创社区</span>
          </Link>
          <button className="p-2 hover:bg-summer-green-100 rounded-full transition-colors ml-4">
            <Search className="w-5 h-5" />
          </button>
        </div>
        
        <button 
          onClick={() => setIsAuthOpen(true)}
          className="flex items-center gap-2 bg-summer-green-800 text-white px-6 py-2 rounded-full text-sm font-medium hover:bg-summer-green-700 transition-all shadow-lg hover:shadow-summer-green-800/20 active:scale-95"
        >
          <User className="w-4 h-4" />
          <span>登录 / 注册</span>
        </button>
      </motion.nav>

      <AuthModal isOpen={isAuthOpen} onClose={() => setIsAuthOpen(false)} />
    </>
  );
}
