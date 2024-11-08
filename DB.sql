-- Criação do banco de dados
CREATE DATABASE telecom_db;

-- Seleção do banco de dados
USE telecom_db;

-- Criação da tabela de registros de chamadas
CREATE TABLE call_records (
    id INT AUTO_INCREMENT PRIMARY KEY,      -- Chave primária (auto incremento)
    record_id VARCHAR(255) NOT NULL,         -- ID do registro da chamada
    type ENUM('start', 'end') NOT NULL,     -- Tipo do registro (start ou end)
    timestamp DATETIME NOT NULL,            -- Timestamp da chamada (data e hora)
    call_id VARCHAR(255) NOT NULL,          -- ID único para a chamada
    source VARCHAR(20),                     -- Número de origem (para chamadas de início)
    destination VARCHAR(20),                -- Número de destino (para chamadas de início)
    UNIQUE (call_id)                        -- Garantindo que cada chamada tenha um único ID
);
