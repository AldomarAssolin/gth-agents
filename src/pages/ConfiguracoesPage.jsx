import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";

export default function ConfiguracoesPage() {
  const handleSave = (e) => {
    e.preventDefault();
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Configurações"
        description="Gerencie as configurações e preferências do seu perfil"
      />
      
      <Card className="max-w-2xl">
        <h2 className="text-xl font-bold text-white mb-6">Preferências do Perfil</h2>
        
        <form onSubmit={handleSave} className="space-y-6">
          <Input
            label="Nome Completo"
            defaultValue="Aldomar Assolin"
            required
          />
          <Input
            label="E-mail"
            type="email"
            defaultValue="aldomar@empresa.com"
            disabled
          />
          
          <div className="flex justify-end space-x-3 pt-4 border-t border-slate-700">
            <Button
              type="submit"
              variant="primary"
            >
              Salvar Alterações
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
