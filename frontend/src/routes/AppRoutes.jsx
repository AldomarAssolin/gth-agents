import { Routes, Route, Navigate } from "react-router-dom";
import AppLayout from "../layouts/AppLayout";
import AuthLayout from "../layouts/AuthLayout";

// Import Pages
import LoginPage from "../pages/LoginPage";
import DashboardPage from "../pages/DashboardPage";
import ColaboradoresPage from "../pages/ColaboradoresPage";
import NovoColaboradorPage from "../pages/NovoColaboradorPage";
import ColaboradorDetalhePage from "../pages/ColaboradorDetalhePage";
import EvolucaoColaboradorPage from "../pages/EvolucaoColaboradorPage";
import AvaliacoesPage from "../pages/AvaliacoesPage";
import NovaAvaliacaoPage from "../pages/NovaAvaliacaoPage";
import MetasPage from "../pages/MetasPage";
import NovaMetaPage from "../pages/NovaMetaPage";
import MetasColaboradorPage from "../pages/MetasColaboradorPage";
import PDISPage from "../pages/PDISPage";
import FeedbacksPage from "../pages/FeedbacksPage";
import ReconhecimentosPage from "../pages/ReconhecimentosPage";
import ConfiguracoesPage from "../pages/ConfiguracoesPage";

import PrivateRoute from "../features/auth/PrivateRoute";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public/Auth Routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
      </Route>

      {/* Protected/App Routes */}
      <Route element={<PrivateRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/colaboradores" element={<ColaboradoresPage />} />
          <Route path="/colaboradores/novo" element={<NovoColaboradorPage />} />
          <Route path="/colaboradores/:id" element={<ColaboradorDetalhePage />} />
          <Route path="/colaboradores/:id/evolucao" element={<EvolucaoColaboradorPage />} />
          <Route path="/avaliacoes" element={<AvaliacoesPage />} />
          <Route path="/avaliacoes/nova" element={<NovaAvaliacaoPage />} />
          <Route path="/metas" element={<MetasPage />} />
          <Route path="/metas/nova" element={<NovaMetaPage />} />
          <Route path="/colaboradores/:id/metas" element={<MetasColaboradorPage />} />
          <Route path="/pdis" element={<PDISPage />} />
          <Route path="/feedbacks" element={<FeedbacksPage />} />
          <Route path="/reconhecimentos" element={<ReconhecimentosPage />} />
          <Route path="/configuracoes" element={<ConfiguracoesPage />} />
        </Route>
      </Route>

      {/* Fallbacks */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
