from answer import ask

questions = ["what is the penalty for late filing of GST returns in Maharashtra?",
             "what are the rules for cryptocurrency taxation in India?",
             "what is the procedure for adopting a child in Tamil Nadu?",
             "how do I get a divorce in Kerala?"]

for q in questions:
    out = ask(q)
    status = "REFUSED " if not out["cases"] else "ANSWERED"
    print(status, q)