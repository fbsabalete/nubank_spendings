# nubank_spendings
Project meant to call Nubank's api and get credit-cards bills and debit statements for personal organization

# Initial setup

`pip install pynubank`, then `pynubank` (follow authentication instructions),
find the cert generated and put it in the project `/resources/`

# Running the script

Simply call the script, and it will ask for authentication if needed. 

Two folders will be generated, `/bills` and `/statements`, containing the excel files based on 
Nubank's response.


You can use the flags `-m` or `--mock` to test requests without calling the api and
 `-p` or `--path` to specify the root folder where you want to save the .xlsx files.