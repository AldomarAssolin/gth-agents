import { useNavigate } from "react-router-dom";

export default function Topbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/login");
  };

  return (
    <header className="h-16 bg-slate-800 border-b border-slate-700 px-8 flex justify-between items-center shadow-sm shrink-0">
      <div>
        <span className="text-slate-400 text-sm font-medium">Bem-vindo ao painel de controle</span>
      </div>
      
      {/* User menu and Logout */}
      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-3">
          <div className="h-8 w-8 rounded-full bg-indigo-500/20 border border-indigo-500/35 flex items-center justify-center text-indigo-400 font-bold text-sm">
            AA
          </div>
          <span className="text-slate-200 text-sm font-semibold">Aldomar Assolin</span>
        </div>
        
        <div className="border-l border-slate-700 h-6"></div>

        <button
          onClick={handleLogout}
          className="flex items-center space-x-1.5 text-slate-400 hover:text-red-400 text-sm font-semibold transition-colors cursor-pointer"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span>Sair</span>
        </button>
      </div>
    </header>
  );
}
