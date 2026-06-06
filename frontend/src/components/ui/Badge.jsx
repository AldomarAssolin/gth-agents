export default function Badge({ children, variant = "info", className = "" }) {
  const base = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border";
  
  const variants = {
    success: "bg-emerald-500/10 text-emerald-400 border-emerald-500/25",
    danger: "bg-red-500/10 text-red-400 border-red-500/25",
    warning: "bg-amber-500/10 text-amber-400 border-amber-500/25",
    info: "bg-indigo-500/10 text-indigo-400 border-indigo-500/25",
    secondary: "bg-slate-500/10 text-slate-400 border-slate-500/25"
  };

  return (
    <span className={`${base} ${variants[variant] || variants.info} ${className}`}>
      {children}
    </span>
  );
}
