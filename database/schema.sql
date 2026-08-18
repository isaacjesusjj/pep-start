PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL CHECK(length(trim(nome)) > 0),
    data_nascimento TEXT NOT NULL,
    telefone TEXT
);

CREATE TABLE IF NOT EXISTS alergias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    descricao TEXT NOT NULL CHECK(length(trim(descricao)) > 0),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE RESTRICT,
    UNIQUE (paciente_id, descricao COLLATE NOCASE)
);

CREATE TABLE IF NOT EXISTS atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    motivo TEXT NOT NULL CHECK(length(trim(motivo)) > 0),
    observacao TEXT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_pacientes_nome
ON pacientes(nome COLLATE NOCASE);

CREATE INDEX IF NOT EXISTS idx_alergias_paciente
ON alergias(paciente_id);

CREATE INDEX IF NOT EXISTS idx_atendimentos_paciente_data
ON atendimentos(paciente_id, data DESC);

-- Tabelas adicionadas na evolução web (versão 2).
CREATE TABLE IF NOT EXISTS exames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    nome TEXT NOT NULL CHECK(length(trim(nome)) > 0),
    data_exame TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'SOLICITADO',
    resultado TEXT,
    observacao TEXT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS prescricoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    medicamento TEXT NOT NULL CHECK(length(trim(medicamento)) > 0),
    dose TEXT NOT NULL CHECK(length(trim(dose)) > 0),
    frequencia TEXT NOT NULL CHECK(length(trim(frequencia)) > 0),
    data_prescricao TEXT NOT NULL,
    observacao TEXT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL CHECK(perfil IN ('ADMIN', 'RECEPCAO', 'PROFISSIONAL')),
    ativo INTEGER NOT NULL DEFAULT 1,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    acao TEXT NOT NULL,
    recurso TEXT NOT NULL,
    recurso_id TEXT,
    detalhes TEXT,
    ip TEXT,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_exames_paciente_data
ON exames(paciente_id, data_exame DESC);

CREATE INDEX IF NOT EXISTS idx_prescricoes_paciente_data
ON prescricoes(paciente_id, data_prescricao DESC);

CREATE INDEX IF NOT EXISTS idx_auditoria_data
ON auditoria(criado_em DESC);
