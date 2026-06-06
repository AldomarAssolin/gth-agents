import { Link, useNavigate } from "react-router-dom";

export default function Layout({ children }) {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex justify-between items-center shadow-md">
        <div className="flex items-center space-x-6">
          <span className="text-2xl font-bold text-indigo-400 tracking-tight">GTH Agents</span>
          <nav className="flex space-x-4">
            <Link
              to="/dashboard"
              className="text-slate-300 hover:text-indigo-400 transition-colors font-medium"
            >
              Dashboard
            </Link>
            <Link
              to="/colaboradores"
              className="text-slate-300 hover:text-indigo-400 transition-colors font-medium"
            >
              Colaboradores
            </Link>
          </nav>
        </div>
        <div>
          <button
            onClick={() => navigate("/login")}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm font-medium transition-all cursor-pointer"
          >
            Sair
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 p-8 max-w-7xl w-full mx-auto">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-slate-800 border-t border-slate-700 px-6 py-4 text-center text-sm text-slate-400">
        &copy; {new Date().getFullYear()} GTH Agents. Todos os direitos reservados.
      </footer>
    </div>
  );
}
