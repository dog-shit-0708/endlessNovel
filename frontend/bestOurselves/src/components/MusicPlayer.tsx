import { useState, useRef, useEffect } from 'react';
import { Volume2, VolumeX } from 'lucide-react';

export default function MusicPlayer() {
  const [isMuted, setIsMuted] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    // 尝试自动播放
    const audio = audioRef.current;
    if (audio) {
      audio.volume = 0.3;
      audio.play().then(() => {
        setIsPlaying(true);
      }).catch(() => {
        // 自动播放被阻止，等待用户交互
        setIsPlaying(false);
      });
    }
  }, []);

  const toggleMute = () => {
    const audio = audioRef.current;
    if (audio) {
      audio.muted = !isMuted;
      setIsMuted(!isMuted);
    }
  };

  const handleFirstInteraction = () => {
    const audio = audioRef.current;
    if (audio && !isPlaying) {
      audio.play().then(() => {
        setIsPlaying(true);
      });
    }
  };

  return (
    <div 
      className="fixed bottom-6 left-6 z-50 flex items-center gap-3 glass-card rounded-full px-4 py-2 cursor-pointer hover:bg-white/60 transition-all"
      onClick={handleFirstInteraction}
    >
      <audio
        ref={audioRef}
        src="/audio/耿耿于怀.mp3"
        loop
        preload="auto"
      />
      <button
        onClick={(e) => {
          e.stopPropagation();
          toggleMute();
        }}
        className="flex items-center justify-center w-8 h-8 rounded-full bg-summer-green-100 hover:bg-summer-green-200 transition-colors"
      >
        {isMuted ? (
          <VolumeX className="w-4 h-4 text-summer-green-700" />
        ) : (
          <Volume2 className="w-4 h-4 text-summer-green-700" />
        )}
      </button>
      <div className="flex flex-col">
        <span className="text-xs font-medium text-summer-green-800">耿耿于怀</span>
        <span className="text-[10px] text-summer-green-600/60">王笑文</span>
      </div>
      {!isPlaying && (
        <span className="text-[10px] text-summer-green-600/80 animate-pulse">
          点击播放
        </span>
      )}
    </div>
  );
}
