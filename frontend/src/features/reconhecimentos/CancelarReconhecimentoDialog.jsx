import { useState } from "react";
import Button from "../../components/ui/Button";

export default function CancelarReconhecimentoDialog({
  isOpen,
  onClose,
  onConfirm,
  isSubmitting,
  apiError = "",
}) {
  const [motivo, setMotivo] = useState("");
  const [error, setError] = useState("");

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!motivo.trim()) {
      setError("O motivo do cancelamento é obrigatório.");
      return;
    }
    setError("");
    onConfirm(motivo.trim());
  };

  const displayError = error || apiError;

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-800 border border-slate-700 rounded-xl shadow-2xl max-w-md w-full p-6 space-y-4">
        <div>
          <h3 className="text-lg font-bold text-white">
            Cancelar Reconhecimento
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Por favor, informe a justificativa para o cancelamento deste registro. Esta ação é irreversível.
          </p>
        </div>

        {displayError && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-xs px-3 py-2 rounded-lg">
            {displayError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label htmlFor="motivo_cancelamento" className="block text-sm font-medium text-slate-300">
              Motivo do Cancelamento
            </label>
            <textarea
              id="motivo_cancelamento"
              rows={4}
              value={motivo}
              onChange={(e) => {
                setMotivo(e.target.value);
                if (e.target.value.trim()) setError("");
              }}
              placeholder="Digite o motivo do cancelamento..."
              className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
              disabled={isSubmitting}
              required
            />
          </div>

          <div className="flex items-center justify-end space-x-2 pt-2">
            <Button
              type="button"
              onClick={onClose}
              variant="secondary"
              disabled={isSubmitting}
            >
              Cancelar
            </Button>
            <Button type="submit" variant="primary" disabled={isSubmitting}>
              {isSubmitting ? "Confirmando..." : "Confirmar Cancelamento"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
