few_shots = [
    {'Question': "Can you show me the first 5 transactions I made on Mpesa?",
     'Answer': 'df.head(5)',
     },
    {'Question': "How about the last 10 transactions? Can you display those?",
     'Answer': 'df.tail(10)',
     },
    {'Question': "I want to know how many transactions I've made in total. Could you count them for me?",
     'Answer': 'len(df)',
     },
    {'Question': "What is the largest amount of money I've received in a single transaction?",
     'Answer': 'df["Paid In"].max()',
     },
    {'Question': "On average, how much do I withdraw per transaction?",
     'Answer': 'df["Withdrawn"].mean()',
     },
    {'Question': "What different types of transactions have I engaged in?",
     'Answer': 'df["Transaction_Type"].unique()',
     },
    {'Question': "Can you show me transactions where I received more than 1000 KES?",
     'Answer': 'df[df["Paid In"] > 1000]',
     },
    {'Question': "I'm curious about transactions involving the name 'John Doe'. Could you fetch those for me?",
     'Answer': 'df[df["Name"] == "John Doe"]',
     },
    {'Question': "How much money do I have in total after all these transactions?",
     'Answer': 'df["Balance"].head(1)',
     },
    {'Question': "Could you provide a breakdown of the number of transactions for each type?",
     'Answer': 'df["Transaction_Type"].value_counts()',
     },
    {'Question': "What is the total amount of money withdrawn for each transaction type?",
     'Answer': 'df.groupby("Transaction_Type")["Withdrawn"].sum()',
     },
    {'Question': "Which transaction was completed first?",
     'Answer': 'df[df["Completion Time"] == df["Completion Time"].min()]',
     },
    {'Question': "How does my average balance vary across different transaction types?",
     'Answer': 'df.groupby("Transaction_Type")["Balance"].mean()',
     },
    {'Question': "Show me transactions that involve a refund.",
     'Answer': 'df[df["Details"].str.contains("refund", case=False)]',
     },
    {'Question': "How many transactions have I conducted for each account name?",
     'Answer': 'df["Name"].value_counts()',
     },
    {'Question': "Can you plot a histogram of the amounts I've received?",
     'Answer': 'df["Paid In"].plot.hist()',
     },
    {'Question': "Can you show the distribution of transaction types using a pie chart?",
     'Answer': 'df["Transaction_Type"].value_counts().plot.pie()',
     },
    {'Question': "Could you visualize how my balance has changed over time?",
     'Answer': 'df.plot(x="Completion Time", y="Balance", kind="line")',
     },
    {'Question': "Create a bar chart comparing the total amounts withdrawn for each transaction type.",
     'Answer': 'df.groupby("Transaction_Type")["Withdrawn"].sum().plot(kind="bar")',
     },
    {'Question': "Could you generate a scatter plot of the amounts I've received versus the amounts I've withdrawn?",
     'Answer': 'df.plot(x="Paid In", y="Withdrawn", kind="scatter")',
     }
]