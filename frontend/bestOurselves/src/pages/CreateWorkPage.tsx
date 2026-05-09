import { motion, AnimatePresence } from "motion/react";
import { ChevronLeft, Send, PenTool, X, Loader2, Sparkles, CheckCircle2 } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

export default function CreateWorkPage() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [submitStatus, setSubmitStatus] = useState<"idle" | "sending" | "success">("idle");
  const [sendingStep, setSendingStep] = useState(0);

  const [showTips, setShowTips] = useState(() => {
    return localStorage.getItem("hide_create_tips") !== "true";
  });

  const handleCloseTips = () => {
    setShowTips(false);
    localStorage.setItem("hide_create_tips", "true");
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) {
      alert("请填写完整的标题与创意。");
      return;
    }

    setSubmitStatus("sending");
    setSendingStep(1);

    // Step 1: Connecting connection band
    setTimeout(() => {
      setSendingStep(2);
    }, 1000);

    // Step 2: Encapsulating memory capsule & write local storage
    setTimeout(() => {
      setSendingStep(3);
      
      const newWork = {
        id: Date.now(),
        title: title.trim(),
        prompt: content.trim(),
        author: "我的脑洞 (AI 协创)",
        excerpt: content.trim().substring(0, 80) + (content.trim().length > 80 ? "..." : ""),
        date: new Date().toLocaleDateString('zh-CN'),
        status: 'rendering', // 'rendering' | 'completed'
        progress: 0,
        likes: 0,
         comments: 0,
        tags: ["平行宇宙", "独家创意"],
        chapters: []
      };

      const existing = JSON.parse(localStorage.getItem("my_derivative_works") || "[]");
      localStorage.setItem("my_derivative_works", JSON.stringify([newWork, ...existing]));
      setSubmitStatus("success");
    }, 2200);

    // Transition to /derivative (mine tab)
    setTimeout(() => {
      navigate("/derivative", { state: { activeTab: "mine" } });
    }, 3800);
  };

  return (
    <div className="min-h-screen selection:bg-summer-green-200 relative text-stone-900 flex flex-col justify-between">
      {/* Fixed Background Image - No Overlay */}
      <div className="fixed inset-0 z-0">
        <img 
          src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/%E8%83%8C%E6%99%AF%E5%9B%BE/%E4%B8%8B%E8%BD%BD.jpg" 
          alt="Background"
          className="w-full h-full object-cover"
        />
      </div>

      <header className="fixed top-0 left-0 right-0 z-50 bg-white/20 backdrop-blur-md border-b border-white/10 px-8 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <Link to="/derivative" className="text-stone-700 hover:text-summer-green-950 transition-colors flex items-center gap-2 group">
            <ChevronLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            <span className="text-sm font-medium">返回文库</span>
          </Link>
          <div className="flex items-center gap-2">
             <PenTool className="w-5 h-5 text-summer-green-900" />
             <h1 className="text-lg font-serif font-bold text-summer-green-950 tracking-wider">创意沙盒</h1>
          </div>
          <div className="w-20" />
        </div>
      </header>

      <main className="relative z-10 flex-1 flex items-center justify-center pt-32 pb-24 px-6 md:px-8">
        <div className="w-full max-w-xl">
          <motion.div 
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="w-full bg-white/10 backdrop-blur-md hover:bg-white/15 border border-white/20 rounded-[28px] p-6 md:p-8 shadow-2xl transition-all min-h-[410px] flex flex-col justify-center"
          >
            <AnimatePresence mode="wait">
              {submitStatus === "idle" ? (
                <motion.form 
                  key="form"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0, y: -20 }}
                  onSubmit={handleSubmit} 
                  className="space-y-6"
                >
                  {/* Title Section */}
                  <div className="space-y-1.5 border-b border-white/10 pb-3">
                    <label className="block text-[10px] font-serif font-bold text-stone-700/60 uppercase tracking-[0.2em]">
                      Title / 标题
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="标题（如《耿耿于怀的平行旅途》）..."
                      className="w-full bg-transparent border-0 outline-none focus:ring-0 text-stone-900 placeholder:text-stone-700/50 font-serif text-xl font-bold tracking-wider"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                    />
                  </div>

                  {/* Content Section */}
                  <div className="space-y-1.5">
                    <label className="block text-[10px] font-serif font-bold text-stone-700/60 uppercase tracking-[0.2em]">
                      Creative Idea / 同人创意与设想
                    </label>
                    <textarea
                      required
                      placeholder="在这里尽情书写你的脑洞与情感..."
                      rows={8}
                      className="w-full bg-transparent border-0 outline-none focus:ring-0 text-stone-900 placeholder:text-stone-700/50 font-serif text-base leading-relaxed resize-none custom-scrollbar"
                      value={content}
                      onChange={(e) => setContent(e.target.value)}
                    />
                  </div>

                  {/* Submit & Status bar */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-4 border-t border-white/10">
                    <p className="text-stone-700/80 text-[10px] font-serif font-medium tracking-wide">
                      标题：{title.length}字 | 创意：{content.length}字
                    </p>
                    <button
                      type="submit"
                      className="px-8 py-3 bg-summer-green-950 text-white rounded-full font-serif font-bold text-base tracking-widest hover:bg-summer-green-900 hover:shadow-xl hover:shadow-summer-green-900/10 transition-all active:scale-[0.98] flex items-center justify-center gap-2 self-end sm:self-auto"
                    >
                      <span>投递创意</span>
                      <Send className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </motion.form>
              ) : (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-center py-6 space-y-8 flex flex-col items-center justify-center"
                >
                  {submitStatus === "sending" ? (
                    <>
                      <div className="relative flex items-center justify-center w-24 h-24">
                        {/* Dynamic back-circles */}
                        <motion.div 
                          animate={{ rotate: 360 }}
                          transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                          className="absolute inset-0 border-2 border-dashed border-summer-green-800/40 rounded-full"
                        />
                        <motion.div 
                          animate={{ rotate: -360 }}
                          transition={{ repeat: Infinity, duration: 4, ease: "linear" }}
                          className="absolute inset-2 border border-dotted border-summer-green-900/60 rounded-full"
                        />
                        <Loader2 className="w-10 h-10 text-summer-green-950 animate-spin" />
                      </div>
                      
                      <div className="space-y-3">
                        <motion.h3 
                          key={sendingStep}
                          initial={{ opacity: 0, y: 8 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -8 }}
                          className="text-xl font-serif font-bold text-summer-green-950 tracking-wider px-4"
                        >
                          {sendingStep === 1 ? "🚀 正在向时空回廊投递你的创意..." : "💌 正在将记忆胶囊封存至时光机..."}
                        </motion.h3>
                        <p className="text-[10px] text-stone-700/60 font-mono tracking-widest uppercase animate-pulse">
                          {sendingStep === 1 ? "TEMPORAL CHANNEL SYNCING..." : "ENCAPSULATING MEMORY SEEDS FOR PARALLEL TIME..."}
                        </p>
                      </div>
                    </>
                  ) : (
                    <>
                      <motion.div 
                        initial={{ scale: 0.4, rotate: -30 }}
                        animate={{ scale: [1.3, 1], rotate: 0 }}
                        transition={{ duration: 0.6, type: "spring" }}
                        className="w-20 h-20 bg-summer-green-800/15 rounded-full flex items-center justify-center"
                      >
                        <CheckCircle2 className="w-12 h-12 text-summer-green-900" />
                      </motion.div>
                      
                      <div className="space-y-3">
                        <h3 className="text-2xl font-serif font-bold text-summer-green-950 tracking-wider">
                          投递成功！
                        </h3>
                        <p className="text-sm text-stone-700 font-serif max-w-[280px] mx-auto leading-relaxed px-4">
                          时代回音已接收，时光机正在为你搭建回忆的桥梁。
                        </p>
                      </div>
                      
                      <div className="text-[10px] text-stone-500 font-bold tracking-widest uppercase mt-4 animate-pulse">
                        正在前往「我的创作」足迹...
                      </div>
                    </>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>
      </main>
    </div>
  );
}
