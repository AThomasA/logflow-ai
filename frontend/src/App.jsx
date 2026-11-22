import { useEffect, useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'

import './App.css'

import {
  getShipments,
  getPendingShipments, 
  getDelayedShipments
} from "./services/api"

function App() {

  // Dados recebidos do backend
  const [data, setData] = useState({
    all: [],
    pending: [],
    delayed: [],
  });

  // Filtro atualmente selecionado
  const [activeFilter, setActiveFilter] = useState("all");

  // Estados de carregamento e erro
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Permite tentar carregar novamente
  const [reloadkey, setRealoadKey] = useState(0)

  // Executa quando o componente é carregado
  useEffect(() => {
    let isActive = true;

    async function loadDashboard() {
      setLoading(true);
      setError("");

      try{
        const [all, pending, delayed] = await Promise.all([
          getShipments(),
          getPendingShipments(),
          getDelayedShipments(),
        ]);

        if(isActive) {
          setData({
            all,
            pending,
            delayed,
          });
        }
      } catch(err) {
        if (isActive) {
          setError(err.message || "Não foi possível carregar os dados");
        }
      } finally {
        if(isActive) {
          setLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      isActive = false;
    };
  },[reloadkey]);

  // Dados da tabela conforme filtro selecionado
  const visableShipments = data[activeFilter];

  // Calculando os indicadores
  const totalShipments = data.all.length;

  const dispatchedCount = data.all.filter(
    (shipment) => shipment.status === "dispatched"
  ).length;

  const pendingCount = data.pending.length;
  const delayedCount = data.delayed.length;

  // Formata datas para o padrão brasileiro
  function formatDate(date) {
    if (!date) return "-";

    return new Intl.DateTimeFormat("pt-BR", {
      dateStyle: "short",
      timeStyle: "short",
    }).format(new Date(date));
  }

  // Traduz estados para exibição
  function getStatusLabel(status) {
    const labels = {
      dispatched: "Dispachada",
      pending: "Pendente",
      delayed: "Atrasada",
      dispatched_without_receipt: "Sem recebimento",
    };

    return labels[status] || status;
  }



  return (
    <main className='dashboard'>
      <header className='dashboard-header'>
        <div>
          <span className='eyebrown'>LOGÍSTICA INTELIGENTE</span>
          <h1>LogFlow AI</h1>
          <p>Visão geral das operações logisticas</p>
        </div>

        <div className='connection-status'>
          <span className='status-dot'></span>
          API conectada
        </div>
      </header>

      <section className='metrics-grid'>

        <article className='metric-card'>
          <span>Total de encomndas</span>
          <strong>{totalShipments}</strong>
          <small>Todos os registros</small>
        </article>
        
        <article className='metric-card dispatched'>
          <span>Dispachadas</span>
          <strong>{dispatchedCount}</strong>
          <small>Operações concluídas</small>
        </article>
        
        <article className='metric-card pending'>
          <span>Pendentes</span>
          <strong>{pendingCount}</strong>
          <small>Aguardando dispacho</small>
        </article>
        
        <article className='metric-card delayed'>
          <span>Atrasadas</span>
          <strong>{delayedCount}</strong>
          <small>Precisam de atenção</small>
        </article>

      </section>

      <section className='shipments-section'>

        <div className='section-heading'>
          <div>
            <h2>Encomendas</h2>
            <p>Acompanhe os registros da operação</p>
          </div>
        </div>

        <nav className='filter-tabs'>
          <button 
          className={activeFilter === "all" ? "active" : ""}
          onClick={() => setActiveFilter("all")}
          >
            Todas ({totalShipments})
          </button>
          
          <button 
          className={activeFilter === "pending" ? "active" : ""}
          onClick={() => setActiveFilter("pending")}
          >
            Pendentes ({pendingCount})
          </button>
          
          <button 
          className={activeFilter === "delayed" ? "active" : ""}
          onClick={() => setActiveFilter("delayed")}
          >
            Atrasadas ({delayedCount})
          </button>
          
        </nav>

        {loading && (
          <div className='feedback-message'>
            Carregando informações logísticas...
          </div>
        )}
        
        {error && (
          <div className='feedback-message error'>
            <p>{error}</p>
            <button onClick={() => setRealoadKey((key) => key + 1)}>
              Tentar novamente
            </button>
          </div>
        )}
        
        {!loading && !error && (
          <div className='table-container'>
            <table>
              <thead>
                <tr>
                  <th>Rastreamento</th>
                  <th>Unidade</th>
                  <th>Recebimento</th>
                  <th>Despacho</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {visableShipments.length === 0 ? (
                  <tr>
                    <td colSpan={5} className='empty-message'>
                      Nenhuma encomenda encontrada.
                    </td>
                  </tr>
                ) : (
                  visableShipments.map((shipment) => (
                    <tr key={shipment.id}>
                      <td className='tracking-code'>
                        {shipment.tracking_code}
                      </td>

                      <td>
                        Unidade {shipment.operation_unit_id}
                      </td>

                      <td>
                        {formatDate(shipment.recived_at)}
                      </td>
                      
                      <td>
                        {formatDate(shipment.dispatched_at)}
                      </td>

                      <td>
                        <span className={`status-badge ${shipment.status}`}>
                          {getStatusLabel(shipment.status)}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>            
          </div>
        )}
      </section>

      <footer className='dashboard-footer'>
        LogFlow AI · Ambiente demonstrativo com dados sintéticos
      </footer>
      
    </main>
  );
}

export default App
