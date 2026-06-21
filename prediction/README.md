This is information on using the EI/ER files in the Uchicago Cluster. I no longer have access to these files, so here are my notes: 

1. Put the relevant CSV files in the proper folder under CSVs.

2. You need to generate settings. The generate_settings_copy file will help you do this; essentially what this does is that it generates the format of the EI/ER experiments that you are going to run.

3. Write your setting files names in a text file of the format ei_settings_files_batch#.txt. I do this with the following: ls settings_files/countytract/*.json > ei_settings_files_batch0.txt

4. Then all you need to do is, in the terminal, run bash slurm_array.sh YOUR_BATCH_NUMBER_HERE
