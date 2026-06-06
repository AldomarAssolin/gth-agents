import Card from "../../components/ui/Card";

export default function DashboardCard({ title, value, footer, className = "", valueClassName = "text-white", icon }) {
  return (
    <Card className={`flex flex-col justify-between hover:border-slate-600 transition-all duration-200 ${className}`}>
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-sm font-medium text-slate-400">{title}</h3>
          <p className={`text-3xl font-bold mt-2 ${valueClassName}`}>{value}</p>
        </div>
        {icon && (
          <div className="p-2 bg-slate-700/40 rounded-lg text-slate-400 shrink-0">
            {icon}
          </div>
        )}
      </div>
      {footer && <p className="text-xs text-slate-500 mt-4 font-medium">{footer}</p>}
    </Card>
  );
}
