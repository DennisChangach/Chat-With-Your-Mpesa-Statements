few_shots = [
    {'Question': "What is the average balance after each transaction type, excluding transactions with negative balances?",
     'Answer': 'df[df["Balance"] >= 0].groupby("Transaction_Type")["Balance"].mean()',
     },
    {'Question': "Can you provide a breakdown of the total amounts withdrawn for each transaction type, for transactions with negative balances?",
     'Answer': 'df[df["Balance"] < 0].groupby("Transaction_Type")["Money_Out"].sum()',
     },
    {'Question': "Show me transactions where I received more than the average amount paid in.",
     'Answer': 'df[df["Money_In"] > df["Money_In"].mean()].sort_values(by="Money_In", ascending=False)',
     },
    {'Question': "What is the total amount withdrawn on Mondays?",
     'Answer': 'df[df["DayOfWeekName"] == "Monday"]["Money_Out"].sum()',
     },
    {'Question': "How much money did I spend on Tuesdays, excluding transactions with negative balances?",
     'Answer': 'df[(df["DayOfWeekName"] == "Tuesday") & (df["Money_Out"] >= 0)]["Money_Out"].sum()',
     },
    {'Question': "What was the highest balance I had after a transaction involving 'Bank Transfer'?",
     'Answer': 'df[df["Transaction_Type"] == "Bank Transfer"]["Balance"].max()',
     },
    {'Question': "Show me transactions where I withdrew more than twice the average amount withdrawn.",
     'Answer': 'df[df["Money_Out"] > 2 * df["Money_Out"].mean()].sort_values(by="Money_Out", ascending=False)',
     },
    {'Question': "How much money did I receive on weekends?",
     'Answer': 'df[df["DayOfWeekName"].isin(["Saturday", "Sunday"])]["Money_In"].sum()',
     },
    {'Question': "Show me transactions where the balance is greater than the sum of the amount paid in and withdrawn.",
     'Answer': 'df[df["Balance"] > df["Money_In"] + df["Money_Out"]]'
     },
     {'Question': "Visualize the distribution of Money Out based on transaction types using a pie chart.",
     'Answer': 'px.pie(df,values = "Money_Out", names="Transaction_Type", title="Transaction Type Distribution")',
     },
    {'Question': "Create a bar chart comparing the total amounts withdrawn for each transaction type.",
     'Answer': 'px.bar(df.groupby("Transaction_Type")["Money_Out"].sum().reset_index(), y="Transaction_Type", x="Money_Out",orientation="h", title="Total Amount Withdrawn by Transaction Type")',
     },
    {'Question': "Generate a scatter plot of the amounts I've received versus the amounts I've withdrawn.",
     'Answer': 'px.scatter(df, x="Money_In", y="Money_Out", title="Money In vs Money Out")',
     },
    {'Question': "Show the trend of my balance over time with a line graph.",
     'Answer': 'px.line(df, x="Completion Time", y="Balance", title="Balance Over Time")',
     },
    {'Question': "Visualize the trend of money in and out over time with a line graph.",
     'Answer': 'px.line(df, x="Completion Time", y=["Money_In", "Money_Out"], title="Money In vs Money Out Over Time")',
     },
    {'Question': "Create a box plot of the distribution of balances.",
     'Answer': 'px.box(df, y="Balance", title="Distribution of Balances")',
     },
    {'Question': "Visualize the trend of balance over time with a smoothed line graph.",
     'Answer': 'px.line(df, x="Completion Time", y="Balance", title="Smoothed Balance Over Time").update_traces(line=dict(smoothing=0.1))',
     },
    {'Question': "Generate a histogram of the amounts I've received.",
     'Answer': 'px.histogram(df, x="Money_In", title="Histogram of Money In")',
     },
    {'Question': "Create a scatter plot of money in versus money out colored by transaction type.",
     'Answer': 'px.scatter(df, x="Money_In", y="Money_Out", color="Transaction_Type", title="Money In vs Money Out by Transaction Type")',
     },
    {'Question': "Visualize the distribution of balances by day of the week using a violin plot.",
     'Answer': 'px.violin(df, x="DayOfWeekName", y="Balance", title="Distribution of Balances by Day of the Week")',
     },
     {'Question': "Which businesses have I spent the most money on? Show the top 5.",
     'Answer': 'df[df["Transaction_Type"].isin(["Till No", "Pay Bill"])].groupby("Account")["Money_Out"].sum().nlargest(5).reset_index()',
     },
    {'Question': "From which individuals have I received the most money? Show the top 5.",
     'Answer': 'df[df["Transaction_Type"] == "Receive Money"].groupby("Account")["Money_In"].sum().nlargest(5).reset_index()',
     },
     {'Question': "Show the trend in my average spend per day of week with the day of week organized from Monday to Sunday.",
     'Answer': 'px.line(df.groupby("DayOfWeekName")["Money_Out"].mean().reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]), title="Trend in Average Spend per Day of Week")',
     }
]