export default function ErrorMessage({ title = "Erro", message = "Ocorreu um erro inesperado.", className = "" }) {
  return (
    <div className={`p-4 bg-red-500/10 border border-red-500/25 rounded-xl flex items-start space-x-3 ${className}`}>
      <svg
        className="h-5 w-5 text-red-400 mt-0.5 shrink-0"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
          clipRule="evenodd"
        />
      </svg>
      <div>
        <h4 className="font-semibold text-red-400 text-sm">{title}</h4>
        <p className="text-red-300/85 text-xs mt-1">{message}</p>
      </div>
    </div>
  );
}
