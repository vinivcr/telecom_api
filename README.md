# Projeto de Cálculo de Conta Telefônica

## Descrição

Esta aplicação fornece uma API RESTful para calcular contas telefônicas baseadas em registros de chamadas recebidos.

## Estrutura de Endpoints

### `POST /call_records`

- Recebe registros detalhados de chamadas (início e fim).
- Campos obrigatórios: `id`, `type`, `timestamp`, `call_id`.

### `GET /billing`

- Calcula e retorna a conta telefônica para o número especificado.
- Parâmetros:
  - `phone_number` (obrigatório): O número de telefone do assinante.
  - `period` (opcional): Período no formato `YYYY-MM`. Caso não seja informado, usa o mês anterior.

## Regras de Precificação

- **Horário Padrão (6h00 - 22h00)**: Taxa fixa de R$ 0,36 e R$ 0,09 por minuto.
- **Horário Reduzido (22h00 - 6h00)**: Taxa fixa de R$ 0,36 e R$ 0,00 por minuto.

## Instruções de Instalação

1. Clone o repositório e instale as dependências:
   ```bash
   pip install -r requirements.txt
