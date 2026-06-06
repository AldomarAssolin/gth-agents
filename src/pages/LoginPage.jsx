import { useNavigate } from "react-router-dom";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";

export default function LoginPage() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    navigate("/dashboard");
  };

  return (
    <form onSubmit={handleLogin} className="space-y-6">
      <Input
        label="E-mail"
        type="email"
        required
        placeholder="seu-email@empresa.com"
      />
      <Input
        label="Senha"
        type="password"
        required
        placeholder="••••••••"
      />
      <Button
        type="submit"
        className="w-full py-3"
      >
        Entrar
      </Button>
    </form>
  );
}
