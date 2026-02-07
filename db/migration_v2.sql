-- ILearn v2 Migration
-- 4 new tables + 1 ALTER

-- Saved episodes (bookmarks)
CREATE TABLE IF NOT EXISTS "SALVATI" (
    "utente_id"       INTEGER NOT NULL,
    "episodio_id"     INTEGER NOT NULL,
    "DataSalvataggio" TEXT NOT NULL,
    PRIMARY KEY ("utente_id", "episodio_id"),
    FOREIGN KEY ("utente_id") REFERENCES "UTENTI"("ID") ON DELETE CASCADE,
    FOREIGN KEY ("episodio_id") REFERENCES "EPISODI"("episodio_id") ON DELETE CASCADE
);

-- Tags system
CREATE TABLE IF NOT EXISTS "TAGS" (
    "tag_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Nome"   TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "EPISODIO_TAGS" (
    "episodio_id" INTEGER NOT NULL,
    "tag_id"      INTEGER NOT NULL,
    PRIMARY KEY ("episodio_id", "tag_id"),
    FOREIGN KEY ("episodio_id") REFERENCES "EPISODI"("episodio_id") ON DELETE CASCADE,
    FOREIGN KEY ("tag_id") REFERENCES "TAGS"("tag_id") ON DELETE CASCADE
);

-- Podcast ratings (1-5 stars)
CREATE TABLE IF NOT EXISTS "VALUTAZIONI" (
    "utente_id"  INTEGER NOT NULL,
    "podcast_id" INTEGER NOT NULL,
    "Voto"       INTEGER NOT NULL CHECK(Voto >= 1 AND Voto <= 5),
    "DataVoto"   TEXT NOT NULL,
    PRIMARY KEY ("utente_id", "podcast_id"),
    FOREIGN KEY ("utente_id") REFERENCES "UTENTI"("ID") ON DELETE CASCADE,
    FOREIGN KEY ("podcast_id") REFERENCES "PODCAST"("podcast_id") ON DELETE CASCADE
);

-- Listening progress tracking
CREATE TABLE IF NOT EXISTS "PROGRESSO" (
    "utente_id"            INTEGER NOT NULL,
    "episodio_id"          INTEGER NOT NULL,
    "Posizione"            REAL NOT NULL DEFAULT 0,
    "Durata"               REAL NOT NULL DEFAULT 0,
    "Completato"           INTEGER NOT NULL DEFAULT 0,
    "UltimoAggiornamento"  TEXT NOT NULL,
    PRIMARY KEY ("utente_id", "episodio_id"),
    FOREIGN KEY ("utente_id") REFERENCES "UTENTI"("ID") ON DELETE CASCADE,
    FOREIGN KEY ("episodio_id") REFERENCES "EPISODI"("episodio_id") ON DELETE CASCADE
);

-- Episode duration column
ALTER TABLE EPISODI ADD COLUMN Durata REAL DEFAULT NULL;
