import { motion } from "motion/react";

export default function Hero() {
  return (
    <section className="relative h-screen flex flex-col items-center justify-center overflow-hidden pt-32 pb-12">
      {/* Background Image with Overlay - Overlays minimized */}
      <motion.div 
        initial={{ scale: 1.1 }}
        animate={{ scale: 1 }}
        transition={{ duration: 1.5, ease: "easeOut" }}
        className="absolute inset-0 z-0"
      >
        <img 
          src="https://zhouxi-1417306345.cos.ap-guangzhou.myqcloud.com/bestOurselves/picture/Wisteria%20%281%29.jpg" 
          alt="Summer Wisteria"
          className="w-full h-full object-cover"
        />
      </motion.div>

      {/* Hero Content */}
      <div className="relative z-10 text-center px-4 max-w-full w-full mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.8 }}
          className="flex flex-col items-center"
        >
          <h2 className="font-serif text-white text-xl md:text-2xl mb-6 tracking-[0.4em] font-medium drop-shadow-[0_2px_15px_rgba(0,0,0,0.9)]">
            耿耿余淮 • 那个盛夏
          </h2>
          <h1 className="font-serif text-4xl md:text-6xl lg:text-7xl xl:text-8xl text-white font-bold leading-tight drop-shadow-[0_4px_45px_rgba(0,0,0,0.9)] mb-10">
            如果世界末日到来的话，<br/>
            一定不会是夏天
          </h1>
          
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.2 }}
            className="flex flex-col md:flex-row items-center justify-center gap-10 mt-16"
          >
            <p className="font-cursive text-white text-3xl tracking-widest italic drop-shadow-[0_2px_15px_rgba(0,0,0,1)]">
              — 最好的我们
            </p>
          </motion.div>
        </motion.div>
      </div>

      {/* Floating Elements */}
      <motion.div 
        animate={{ 
          y: [0, -15, 0],
          opacity: [0.3, 0.6, 0.3]
        }}
        transition={{ duration: 4, repeat: Infinity }}
        className="absolute bottom-10 left-1/2 -translate-x-1/2 text-summer-green-800"
      >
        <div className="flex flex-col items-center gap-2">
          <span className="text-xs tracking-[0.5em] uppercase font-medium">Scroll</span>
          <div className="w-[1px] h-12 bg-summer-green-800/30" />
        </div>
      </motion.div>
    </section>
  );
}
