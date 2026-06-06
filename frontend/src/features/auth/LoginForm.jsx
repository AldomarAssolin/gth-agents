import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "./useAuth";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import ErrorMessage from "../../components/ui/ErrorMessage";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLoading) return;

    try {
      setError(null);
      setIsLoading(true);
      await login(email, senha);

      const from = location.state?.from || { pathname: "/dashboard" };
      navigate(from, { replace: true });
    } catch (err) {
      if (err.response) {
        const { status, data } = err.response;
        if (status === 401) {
          setError("E-mail ou senha inválidos.");
        } else if (status === 403) {
          setError("Seu usuário está inativo. Entre em contato com o administrador.");
        } else if (status === 400 || status === 422) {
          setError(data?.message || "Verifique os dados informados.");
        } else {
          setError("Não foi possível realizar o login. Tente novamente.");
        }
      } else if (err.request) {
        setError("Não foi possível conectar à API. Verifique se o servidor está em execução.");
      } else {
        setError("Não foi possível realizar o login. Tente novamente.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && <ErrorMessage title="Erro de autenticação" message={error} />}

      <Input
        label="E-mail"
        type="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="seu-email@empresa.com"
        disabled={isLoading}
      />

      <Input
        label="Senha"
        type="password"
        required
        value={senha}
        onChange={(e) => setSenha(e.target.value)}
        placeholder="••••••••"
        disabled={isLoading}
      />

      <Button
        type="submit"
        variant="primary"
        className="w-full py-3 shrink-0"
        disabled={isLoading}
      >
        {isLoading ? "Entrando..." : "Entrar"}
      </Button>
    </form>
  );
}
