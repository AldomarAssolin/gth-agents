import { Link } from "react-router-dom";
import Card from "../../components/ui/Card";
import Button from "../../components/ui/Button";
import StatusColaboradorBadge from "./StatusColaboradorBadge";
import {
  resolverNomeSetor,
  resolverNomeFuncao,
  formatarDataBrasil,
} from "./colaboradoresHelpers";

export default function ColaboradorDetalhe({ colaborador, setores = [], funcoes = [] }) {
  const resolvedSetor = resolverNomeSetor(colaborador, setores);
  const resolvedFuncao = resolverNomeFuncao(colaborador, funcoes);

  return (
    <div className="space-y-6">
      <Card>
        <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-6 border-b border-slate-700">
          <div>
            <h2 className="text-xl font-bold text-white">Dados do Colaborador</h2>
            <p className="text-slate-400 text-sm mt-1">
              Informações básicas do cadastro institucional
            </p>
          </div>
          <div className="mt-4 md:mt-0">
            <StatusColaboradorBadge status={colaborador.status} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-sm font-medium text-slate-400">Nome</h3>
            <p className="text-white text-lg mt-1 font-semibold">
              {colaborador.nome}
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-slate-400">Matrícula</h3>
            <p className="text-white text-lg mt-1 font-semibold">
              {colaborador.matricula}
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-slate-400">
              E-mail Corporativo
            </h3>
            <p className="text-white text-lg mt-1 font-semibold">
              {colaborador.email || "Não informado"}
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-slate-400">
              Data de Admissão
            </h3>
            <p className="text-white text-lg mt-1 font-semibold">
              {formatarDataBrasil(colaborador.data_admissao)}
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-slate-400">Setor</h3>
            <p className="text-white text-lg mt-1 font-semibold">
              {resolvedSetor}
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-slate-400">Função</h3>
            <p className="text-white text-lg mt-1 font-semibold">
              {resolvedFuncao}
            </p>
          </div>
        </div>
      </Card>

      <Card>
        <div className="pb-4 mb-4 border-b border-slate-700">
          <h2 className="text-lg font-bold text-white">Ações e Atalhos</h2>
          <p className="text-slate-400 text-sm mt-1">
            Gerenciamento e ações vinculadas ao colaborador
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <Link to={`/colaboradores/${colaborador.id}/evolucao`} className="w-full">
            <Button variant="primary" className="w-full justify-center">
              Ver Evolução
            </Button>
          </Link>

          <Link to={`/avaliacoes/nova?colaborador_id=${colaborador.id}`} className="w-full">
            <Button variant="outline" className="w-full justify-center">
              Registrar Avaliação
            </Button>
          </Link>

          <Button
            variant="outline"
            className="w-full justify-center"
            disabled
            aria-disabled="true"
            title="Disponível em breve"
          >
            Criar Meta (Em breve)
          </Button>

          <Button
            variant="outline"
            className="w-full justify-center"
            disabled
            aria-disabled="true"
            title="Disponível em breve"
          >
            Criar PDI (Em breve)
          </Button>

          <Button
            variant="outline"
            className="w-full justify-center"
            disabled
            aria-disabled="true"
            title="Disponível em breve"
          >
            Registrar Feedback (Em breve)
          </Button>

          <Button
            variant="outline"
            className="w-full justify-center"
            disabled
            aria-disabled="true"
            title="Disponível em breve"
          >
            Registrar Reconhecimento (Em breve)
          </Button>
        </div>
      </Card>
    </div>
  );
}
