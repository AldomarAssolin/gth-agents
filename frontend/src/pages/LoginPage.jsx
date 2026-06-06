import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import LoginForm from "../features/auth/LoginForm";
import Loading from "../components/ui/Loading";

export default function LoginPage() {
  const { isAuthenticated, isInitializing } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isInitializing && isAuthenticated) {
      navigate("/dashboard", { replace: true });
    }
  }, [isAuthenticated, isInitializing, navigate]);

  if (isInitializing) {
    return <Loading message="Carregando..." className="py-6" />;
  }

  if (isAuthenticated) {
    return null;
  }

  return <LoginForm />;
}
