-- Execute no banco MySQL criado no FreeDB.
-- O nome do banco é definido pelo serviço e deve ser informado no .env.
CREATE TABLE IF NOT EXISTS ocorrencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    categoria VARCHAR(20) NOT NULL,
    cep CHAR(8) NOT NULL,
    rua VARCHAR(120) NOT NULL,
    bairro VARCHAR(80) NOT NULL,
    cidade VARCHAR(80) NOT NULL,
    uf CHAR(2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'aberta',
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
