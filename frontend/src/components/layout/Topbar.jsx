import { useNavigate } from "react-router-dom";
import { useAuth } from "../../features/auth/useAuth";

export default function Topbar({ isSidebarOpen, onToggleSidebar }) {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const getInitials = (name) => {
    if (!name) return "U";
    const parts = name.trim().split(/\s+/);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return name.slice(0, 2).toUpperCase();
  };

  return (
    <header className="h-16 bg-slate-800 border-b border-slate-700 px-4 md:px-8 flex justify-between items-center shadow-sm shrink-0">
      <div className="flex items-center space-x-3">
        {/* Toggle Sidebar Button for Mobile */}
        <button
          onClick={onToggleSidebar}
          className="lg:hidden p-2 -ml-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer"
          aria-label="Abrir menu"
          aria-expanded={isSidebarOpen}
        >
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <span className="text-slate-400 text-xs md:text-sm font-medium hidden sm:inline">
          Bem-vindo ao painel de controle
        </span>
      </div>
      
      {/* User menu and Logout */}
      <div className="flex items-center space-x-3 md:space-x-6">
        <div className="flex items-center space-x-2 md:space-x-3">
          <div 
            className="h-8 w-8 rounded-full bg-indigo-500/20 border border-indigo-500/35 flex items-center justify-center text-indigo-400 font-bold text-sm shrink-0"
            title={user?.email || ""}
          >
            {getInitials(user?.nome || user?.email || "U")}
          </div>
          <div className="flex flex-col min-w-0 max-w-[100px] sm:max-w-[150px] md:max-w-none">
            <span className="text-slate-200 text-xs md:text-sm font-semibold leading-tight truncate">
              {user?.nome || user?.email || "Usuário"}
            </span>
            {user?.perfil && (
              <span className="text-slate-400 text-[9px] md:text-[10px] uppercase tracking-wider font-bold mt-0.5 truncate">
                {user.perfil}
              </span>
            )}
          </div>
        </div>
        
        <div className="border-l border-slate-700 h-6"></div>

        <button
          onClick={handleLogout}
          className="flex items-center space-x-1 md:space-x-1.5 text-slate-400 hover:text-red-400 text-xs md:text-sm font-semibold transition-colors cursor-pointer shrink-0"
        >
          <svg className="h-4 w-4 md:h-5 md:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span className="hidden sm:inline">Sair</span>
        </button>
      </div>
    </header>
  );
}
