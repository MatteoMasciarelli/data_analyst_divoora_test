# Data Analyst - Matteo Masciarelli
In questa repository si possono trovare tutti i necessari script necessari per lo sviluppo di report Excel sulle distanze e le tempistiche. 

Di seguito i file contenuti e il loro utilizzo 
1. models.py - contiene i modelli necessari per validare i dati forniti nel file Excel
2. ETLPipeline - contiene l'oggetto che sarà responsabile per il processo ETL del file Excel
3. data_loading.py - contiene un handler che permette di effettuare il processo di ETL
4. db_info.py - contiene le informazioni necessarie per accedere al DB
5. Divoora.db - un DB SQLite3 dove verranno caricati i dati dell'excel
6. tempisctiche.sql - contiene la query SQL usata per alimentare i dati richiesti per il report Excel
7. distanze.sql - contiene la query SQL usata per alimentare i dati richiesti per il report Excel
8. requirments.txt - contiene i pacchetti necessari per l'utilizzo di questi script

Dato che non stiamo in un abiente di produzione e non è possibile collegarsi ad un DB SQLlite, i seguenti file verrano aggiunti alla repository, i quali verranno usati nei report excel. 
1. data_extraction.py - contiene uno script python che legge le query, si interfaccia col DB, estrae i dati e li esporta in csv
2. tempistiche.csv - l'estrazione che risulta dalla query tempistiche.sql
3. distanze.csv - l'estrazione che risulta dalla query distanze.sql