import { motion, AnimatePresence } from "motion/react";
import { X, Mail, Lock, User, Github, Chrome } from "lucide-react";
import { useState } from "react";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [authMethod, setAuthMethod] = useState<'email' | 'phone'>('email');

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 overflow-hidden">
          {/* Backdrop */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-stone-900/60 backdrop-blur-sm"
          />

          {/* Modal Content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="relative w-full max-w-md bg-white rounded-[40px] shadow-2xl overflow-hidden border border-white/20 flex flex-col max-h-[90vh]"
          >
            {/* Top Decorative Bar */}
            <div className="h-2 bg-summer-green-800 w-full shrink-0" />
            
            <button 
              onClick={onClose}
              className="absolute top-6 right-6 p-2 text-stone-400 hover:text-stone-900 hover:bg-stone-100 rounded-full transition-all z-10"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="overflow-y-auto p-8 sm:p-10 pt-12 custom-scrollbar">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-serif font-bold text-stone-900 mb-2">
                  成为最好的我们
                </h2>
                <p className="text-stone-400 text-sm italic">
                  记录青春的点滴，开启一段新篇章
                </p>
              </div>

              {/* Main Tabs: Login vs Register */}
              <div className="flex bg-stone-100 p-1.5 rounded-2xl mb-8">
                <button 
                  onClick={() => setIsLogin(true)}
                  className={`flex-1 py-3 text-xs font-bold rounded-xl transition-all ${isLogin ? 'bg-white text-summer-green-800 shadow-sm' : 'text-stone-400'}`}
                >
                  登录
                </button>
                <button 
                  onClick={() => setIsLogin(false)}
                  className={`flex-1 py-3 text-xs font-bold rounded-xl transition-all ${!isLogin ? 'bg-white text-summer-green-800 shadow-sm' : 'text-stone-400'}`}
                >
                  注册
                </button>
              </div>

              {/* Sub Tabs: Method Selection */}
              <div className="flex justify-center gap-6 mb-6">
                <button 
                  onClick={() => setAuthMethod('email')}
                  className={`text-[10px] font-bold tracking-widest uppercase pb-1 border-b-2 transition-all ${authMethod === 'email' ? 'text-summer-green-800 border-summer-green-800' : 'text-stone-300 border-transparent'}`}
                >
                  QQ邮箱
                </button>
                <button 
                  onClick={() => setAuthMethod('phone')}
                  className={`text-[10px] font-bold tracking-widest uppercase pb-1 border-b-2 transition-all ${authMethod === 'phone' ? 'text-summer-green-800 border-summer-green-800' : 'text-stone-300 border-transparent'}`}
                >
                  手机号
                </button>
              </div>

              <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
                {!isLogin && (
                  <div className="relative group">
                    <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-stone-300 group-focus-within:text-summer-green-800 transition-colors" />
                    <input 
                      type="text" 
                      placeholder="设置昵称"
                      className="w-full pl-12 pr-4 py-4 bg-stone-50 border border-stone-100 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-summer-green-200 transition-all font-medium"
                    />
                  </div>
                )}

                {authMethod === 'email' ? (
                  <div className="relative group">
                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-stone-300 group-focus-within:text-summer-green-800 transition-colors" />
                    <input 
                      type="email" 
                      placeholder="QQ邮箱 / 常用邮箱"
                      className="w-full pl-12 pr-4 py-4 bg-stone-50 border border-stone-100 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-summer-green-200 transition-all font-medium"
                    />
                  </div>
                ) : (
                  <div className="relative group">
                    <div className="absolute left-4 top-1/2 -translate-y-1/2 flex items-center gap-2 border-r border-stone-200 pr-2">
                       <span className="text-[10px] font-bold text-stone-400">+86</span>
                    </div>
                    <input 
                      type="tel" 
                      placeholder="手机号"
                      className="w-full pl-20 pr-4 py-4 bg-stone-50 border border-stone-100 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-summer-green-200 transition-all font-medium"
                    />
                  </div>
                )}

                <div className="relative group">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-stone-300 group-focus-within:text-summer-green-800 transition-colors" />
                  <input 
                    type="password" 
                    placeholder={isLogin ? "登录密码" : "设置密码"}
                    className="w-full pl-12 pr-4 py-4 bg-stone-50 border border-stone-100 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-summer-green-200 transition-all font-medium"
                  />
                </div>

                <button className="w-full bg-summer-green-950 text-white py-4 rounded-2xl font-serif font-bold tracking-widest hover:bg-summer-green-900 transition-all shadow-xl shadow-summer-green-900/20 active:scale-95 mt-4">
                  {isLogin ? "立即登录" : "立即注册"}
                </button>
              </form>
            </div>

            {/* Footer Quote */}
            <div className="bg-stone-50 p-6 text-center shrink-0">
              <p className="text-[10px] text-stone-300 font-serif italic text-stone-400">
                "当时的他是最好的他，后来的我是最好的我。"
              </p>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
