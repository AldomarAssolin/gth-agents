export default function PageHeader({ title, description, actions }) {
  return (
    <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0 mb-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white">{title}</h1>
        {description && <p className="text-slate-400 mt-1.5 text-sm">{description}</p>}
      </div>
      {actions && <div className="flex items-center flex-wrap gap-3">{actions}</div>}
    </div>
  );
}
