
import pandas as pd
import os
import statsmodels.api as sm
df=pd.read_csv(r"C:\Users\lef1\regressione.csv",sep=';',dtype=str)
df.head()
dtype={'ID_Operatore':int,'Data':str,'Operatore':str,'Ordine':str,'Codice_Parte':str,'Finitura':str,'Desc_Finitura':str,'Risorsa_Prevista':str,	'Reparto_effettivo':str,'Risorsa':str,'Somma_AttT':float,'Somma_Gpp':float,'Eff':float,'Somma_Pezzi_Buoni':int,'Pres_Totale_Giorn':float,'Incidenza':float,'Mese':str,'Ore_gg_utili':float,	'Gg_mese':float,'Ore_gg_utili_totali':float,'Gpp_totali':float,	'Pres_Totale_Giorn':float,'Servizio1':str,'Wk':str,'REPARTO':str,'VALUE_STREAM':str,'LINEA':str,'Operatore':str,'REPARTO_BASE':str,'VALUE_STREAM_BASE':str,'SQUADRA_DI_LAVORO':str,'Gruppi':str,'Tipo_Fase':str
       }

df['Somma_Pezzi_Buoni']=pd.to_numeric(df['Somma_Pezzi_Buoni'],errors='coerce')
df['Codice_Parte']=pd.to_numeric(df['Codice_Parte'],errors='coerce')
df['Finitura']=pd.to_numeric(df['Finitura'],errors='coerce')
df['Risorsa']=pd.to_numeric(df['Risorsa'],errors='coerce')

# Crea una variabile dummy per quantita < 10
df['quantita_dummy'] = (df['Somma_Pezzi_Buoni'] >= 10).astype(int)

# Raggruppa i dati per 'codice', 'finitura' e 'risorsa'
grouped = df.groupby(['Codice_Parte', 'Finitura', 'Risorsa'])

# Esegui una regressione per ogni gruppo
for name, group in grouped:
    Somma_Pezzi_Buoni, Finitura, Risorsa = name

    # Verifica se ci sono almeno due righe per fare la regressione
    if len(group) < 2:
        print(f"Non ci sono abbastanza dati per fare la regressione per Codice: {Somma_Pezzi_Buoni}, Finitura: {Finitura}, Risorsa: {Risorsa}")
        continue

    # Definisci le variabili indipendenti e dipendenti
    X = group[['Somma_Pezzi_Buoni', 'Somma_AttT', 'quantita_dummy']]
    y = group['Eff']
    
    # Aggiungi una costante (intercetta) al modello
    X = sm.add_constant(X)
    
    # Crea e adatta il modello di regressione
    model = sm.OLS(y, X).fit()
    
    # Stampa i risultati della regressione
    print(f"Risultati della regressione per Codice: {Somma_Pezzi_Buoni}, Finitura: {Finitura}, Risorsa: {Risorsa}")
    print(model.summary())
    print("\n" + "="*80 + "\n")