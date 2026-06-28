export default function Card({ children, className = "", ...props }) {
  return (
    <div
      className={`p-4 sm:p-6 bg-slate-800 rounded-xl border border-slate-700 shadow-md ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
