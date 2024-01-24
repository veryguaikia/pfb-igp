from pathlib import Path
import coh, profitloss, overheads

overheads.find_highest_overhead(Path(r"csv reports\overheads.csv"))
coh.analyze_cash_on_hand(Path(r"csv reports\cash-on-hand.csv"))
profitloss.analyze_netprofit(Path(r"csv reports\profit-and-loss.csv"))