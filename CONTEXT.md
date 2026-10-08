# Project context
MBA course project (Financial & Risk Analytics) on AI-based fraud monitoring
in digital payments.
## Data
- File: data/paysim_sample.csv (PaySim synthetic mobile-money transactions)
- 15% random sample, 954,393 rows, 1,201 frauds
- Columns: step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig,
  nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud
- Fraud occurs only in TRANSFER and CASH_OUT
- Do NOT open this file in the editor (too large). Read it with pandas.
## Rules
1. Do NOT use the balance columns; they leak the answer.
2. Split by time (step), not randomly.
3. Models and rules make decisions; the LLM only explains them from case-file facts.
4. Keep code simple and commented. I must explain every file in a viva.
5. Always show a plan before coding.