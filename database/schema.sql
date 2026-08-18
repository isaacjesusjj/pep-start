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
