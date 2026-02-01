End-to-End Power BI Project – Performance & KPI Analysis
Overview

Questo progetto implementa un flusso completo di Business Intelligence, dalla preparazione dei dati alla realizzazione di dashboard analitiche, con particolare attenzione a modellazione dati, qualità dell’informazione e coerenza dei KPI.

Il dominio della Premier League viene utilizzato come contesto applicativo per simulare uno scenario reale di analisi delle performance, adottando approcci e soluzioni tipiche di progetti BI in ambito enterprise.

Scope of the Analysis

La dashboard fornisce una visione di sintesi delle performance, focalizzata su:

indicatori chiave di performance (KPI)

confronti tra entità

trend e andamenti aggregati

Il modello dati è stato progettato per essere estendibile, consentendo l’integrazione di più stagioni, analisi temporali e pagine di approfondimento.

BI Architecture & Technologies

SQL Server come database di staging e supporto analitico

ETL scripts per la preparazione e trasformazione dei dati

Power BI per modellazione semantica e visualizzazione

Activities Performed

Ingestione e caricamento dati su SQL Server

Preparazione e trasformazione dei dati tramite processi ETL

Progettazione del modello dati (fact e dimensioni)

Sviluppo di una dashboard analitica di sintesi in Power BI

Data Profiling & Data Quality

Il progetto include un processo strutturato di data profiling e data quality, integrato nel flusso BI per garantire affidabilità e coerenza delle analisi.

Step 1 – Table-level profiling

Analisi del volume dati e della completezza delle tabelle di staging.

Step 2 – Column-level profiling

Per ogni colonna vengono analizzati:

numero totale di record

valori null o non valorizzati

valori distinti

percentuali di nullità e univocità

Questo consente di individuare attributi poco significativi o potenzialmente problematici.

Step 3 – Numerical profiling

Analisi statistica dei campi numerici tramite:

MIN / MAX

AVG

standard deviation

individuazione di outlier

Utilizzata per intercettare valori anomali che potrebbero compromettere KPI e aggregazioni.

Step 4 – Business rules validation

Applicazione di regole di dominio per verificare la coerenza logica dei dati, ad esempio:

Starts ≤ Matches

Goals ≤ Shots

Minutes ≥ 0




