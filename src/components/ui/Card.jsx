export default function Card({ children, className = "", ...props }) {
  return (
    <div
      className={`p-6 bg-slate-800 rounded-xl border border-slate-700 shadow-md ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
