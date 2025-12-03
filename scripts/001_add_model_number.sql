-- Migration: add model_number column to assets table
-- Run this SQL against your database (PostgreSQL / SQLite / MySQL variants may use similar syntax).

-- PostgreSQL:
ALTER TABLE assets
    ADD COLUMN IF NOT EXISTS model_number VARCHAR;

-- SQLite (ALTER TABLE supports adding columns, but IF NOT EXISTS isn't available on older SQLite versions):
-- ALTER TABLE assets ADD COLUMN model_number TEXT;

-- MySQL:
-- ALTER TABLE `assets` ADD COLUMN IF NOT EXISTS `model_number` VARCHAR(255) NULL;

-- Note: After running, you may want to backfill values for existing records if you have model data elsewhere.
