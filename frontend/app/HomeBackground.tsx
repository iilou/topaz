"use client";

import { LightRays } from "@/components/ui/light-rays";
import { motion } from "framer-motion";

import { useState, useEffect } from "react";

import Image from "next/image";

export default function HomeBackground() {
  const [mounted, setMounted] = useState(false);
  // const particles = Array.from({ length: 10 });
  const [particles] = useState(Array.from({ length: 15 }));

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <div className="fixed top-0 left-0 w-full h-full -z-10 overflow-hidden bg-home-bg">
      {particles.map((_, index) => (
        <motion.div
          key={index}
          className="absolute rounded-full bg-home-bg-particles/60 blur-[280px]"
          style={{
            width: Math.random() * 300 + 100,
            height: Math.random() * 300 + 100,
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
          }}
          animate={{
            x: [0, Math.random() * 100 - 50, 0],
            y: [0, Math.random() * 100 - 50, 0],
          }}
          transition={{
            duration: Math.random() * 10 + 10,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      ))}
      <Image src="/helix.svg" alt="DNA Helix" width={1920} height={1024} className="absolute top-0 left-0 w-full h-full object-cover blur-xs" />

      <LightRays color="#56aab9" blur={50} speed={10} />
    </div>
  );
}
