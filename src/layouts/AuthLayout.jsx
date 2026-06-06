import { Outlet } from "react-router-dom";

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 text-slate-100 px-4">
      <div className="w-full max-w-md p-8 bg-slate-800 rounded-2xl shadow-xl border border-slate-700">
        <div className="text-center mb-8">
          <div className="inline-flex bg-indigo-600 p-3 rounded-xl text-white shadow-md mb-4">
            <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">GTH Agents</h1>
          <p className="text-slate-400 mt-2 text-sm">Gestão de Talentos e Desempenho com Agentes de IA</p>
        </div>
        <Outlet />
      </div>
    </div>
  );
}
