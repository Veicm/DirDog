CREATE TABLE directory (
    id INTEGER PRIMARY KEY,
    file_name TEXT NOT NULL,
    file_extension TEXT NOT NULL,
    last_modified INTEGER NOT NULL,
    hash TEXT NOT NULL
)
