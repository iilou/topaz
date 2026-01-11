export default function StaticHelix() {
  const width = 1200;
  const height = 2000;
  const strands = 20; // Number of "segments" or turns
  const points = 200; // Smoothness

  // Generate the path for a strand
  const getPath = (phase: number) => {
    return Array.from({ length: points })
      .map((_, i) => {
        const y = (i / points) * height;
        const x = width / 2 + Math.sin((i / points) * Math.PI * 4 + phase) * 130;
        return `${i === 0 ? "M" : "L"} ${x} ${y}`;
      })
      .join(" ");
  };

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
      <defs>
        <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
          {/* Layer 1: The soft outer glow */}
          <feGaussianBlur stdDeviation="15" result="blur15" />

          {/* Layer 2: The mid-range glow */}
          <feGaussianBlur stdDeviation="8" result="blur8" />

          {/* Layer 3: Boosting the intensity using a color matrix */}
          <feColorMatrix
            in="blur15"
            type="matrix"
            values="1 0 0 0 0
            0 1 0 0 0
            0 0 1 0 0
            0 0 0 2.8 0"
            result="boostedBlur"
          />

          {/* Stacking the layers */}
          <feMerge>
            <feMergeNode in="boostedBlur" />
            <feMergeNode in="blur8" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        {/* The Repeating Gradient */}
        <linearGradient id="helix-grad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#ABEBF6" />
          <stop offset="50%" stopColor="#144E58" />
          <stop offset="100%" stopColor="#ABEBF6" />
        </linearGradient>
        <linearGradient id="rung-grad" x1="0%" y1="0%" x2="0%" y2="100%" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#ABEBF6aa" />
          <stop offset="50%" stopColor="#144E58aa" />
          <stop offset="100%" stopColor="#ABEBF6aa" />
        </linearGradient>
      </defs>

      {/* Strand 2 (Back) */}
      <path d={getPath(Math.PI)} fill="none" filter="url(#glow)" stroke="url(#helix-grad)" strokeWidth="80" strokeLinecap="round" opacity="0.4" />

      {/* Connecting "Shoelace" Rungs */}
      {Array.from({ length: 15 }).map((_, i) => {
        // Offset y slightly so the first/last rungs aren't cut off at the edge
        const y = (i / 14) * (height - 40) + 20;
        const x1 = width / 2 + Math.sin((i / 15) * Math.PI * 4) * 100; // Adjusted to fit width
        const x2 = width / 2 + Math.sin((i / 15) * Math.PI * 4 + Math.PI) * 100;

        return <path key={i} d={`M ${x1} ${y} L ${x2} ${y}`} stroke="url(#rung-grad)" strokeWidth="80" strokeLinecap="round" />;
      })}

      {/* Strand 1 (Front) */}
      <path d={getPath(0)} fill="none" filter="url(#glow)" stroke="url(#helix-grad)" strokeWidth="80" strokeLinecap="round" />
    </svg>
  );
}
